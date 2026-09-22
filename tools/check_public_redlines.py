#!/usr/bin/env python3
"""Check public-repo red lines in added lines or whole files.

Red lines (per issue #43 line 44: public repo material must not carry
internal URLs, Notion page ids, Figma fileKey / node-id lists, or
credentials; public records keep publishable source names and verdicts
only).

Rules
  node_id     Figma node-id shape  <1-6 digits>:<1-6 digits>
              HH:MM:SS-shaped timestamps are stripped first; a bare
              HH:MM still matches on purpose (fail-closed: adjudicate).
  file_key    Figma fileKey shape: a 22-128 char alnum token that
              contains at least one digit AND one letter and is NOT
              pure hex (40-char git SHAs are legitimate public content;
              digitless camelCase domain terms are not fileKeys).
  notion_id   Notion page-id shape: exactly 32 lowercase hex chars.
  credential  Common token/key shapes: sk-/pk-/rk-<20+>, ghp_/gho_/
              github_pat_<20+>, PEM private-key header.

Probe-design rule baked in (learned the hard way, twice): a
length+charset probe MUST carry a discriminating test, otherwise it
sweeps up every long camelCase identifier in the naming convention.

Exit codes
  0  checked and clean
  1  red-line hits (each reported with source, line no., rule, text;
     adjudication belongs to the caller -- a hit is a lead, not a verdict)
  2  nothing matched the input (no commits in range / no readable files):
     "not checked", NOT "clean"
  3  self-test failed: the tool itself is broken, any 0 from such a run
     is unproven

Usage
  python3 tools/check_public_redlines.py --rev-range A..B   # added lines of the range diff
  python3 tools/check_public_redlines.py --files PATH [PATH ...]

Self-test runs first by default (asserts WHICH rule fires on each
fixture, and that negative fixtures do not fire); --no-self-test skips
it (only for debugging the tool itself).
"""

import argparse
import re
import subprocess
import sys

TS_RE = re.compile(r"\d{1,4}:\d{2}:\d{2}")  # no \b: must also strip inside ISO "T14:38:03"

RULES = [
    # (name, regex, extra predicate or None)
    ("node_id", re.compile(r"\b[0-9]{1,6}:[0-9]{1,6}\b"), None),
    ("file_key", re.compile(r"\b[0-9a-zA-Z]{22,128}\b"),
     lambda m: (any(c.isdigit() for c in m.group())
                and any(c.isalpha() for c in m.group())
                and not re.fullmatch(r"[0-9a-f]+", m.group()))),
    ("notion_id", re.compile(r"\b[0-9a-f]{32}\b"), None),
    ("credential", re.compile(
        r"\b(?:sk|pk|rk)-[A-Za-z0-9]{20,}\b"
        r"|\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}\b"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"), None),
]

# Fixtures are SYNTHETIC: shapes only, never real ids/keys.
SELFTEST_CASES = [
    # (line, rule expected to fire or None)
    ("see node 999:999 for details", "node_id"),
    ("logged at 2026-09-22T14:38:03 and 14:38:05 (timestamps, must not fire)", None),
    ("fileKey fixture FileKeyFixture12345678 here", "file_key"),
    ("long camelCase term SpatialOpportunityPolicy (digitless, must not fire)", None),
    ("merge commit 863522bf38d3be9cf6b645a24362755cc666f55b (git SHA, must not fire)", None),
    ("notion page 0123456789abcdef0123456789abcdef linked", "notion_id"),
    ("clean prose with normal words and 12:42-style times", "node_id"),  # bare HH:MM: fail-closed, fires
    ("token sk-abcdefghijklmnopqrst fired", "credential"),
    ("nothing suspicious here", None),
]


def scan_line(line):
    """Return [(rule, matched_text), ...] for one line."""
    hits = []
    stripped = TS_RE.sub(" ", line)
    for name, rx, pred in RULES:
        for m in rx.finditer(stripped):
            if pred is None or pred(m):
                hits.append((name, m.group()))
    return hits


def self_test():
    """Assert each rule fires on its fixture and negatives stay silent.

    Returns True on pass, False on any failure (message printed).
    """
    ok = True
    seen_rules = set()
    for line, expected in SELFTEST_CASES:
        got = scan_line(line)
        names = {n for n, _ in got}
        if expected is None:
            if names:
                ok = False
                print("SELFTEST FAIL: expected no rule, got %s for %r" % (sorted(names), line))
        else:
            if names != {expected}:
                ok = False
                print("SELFTEST FAIL: expected {%s}, got %s for %r" % (expected, sorted(names), line))
            else:
                seen_rules.add(expected)
    missing = {n for n, _, _ in RULES} - seen_rules
    if missing:
        ok = False
        print("SELFTEST FAIL: rules never exercised by fixtures: %s" % sorted(missing))
    return ok


def check_lines(lines, source_of_line):
    """lines: list[str]; source_of_line(i) -> printable source. Returns hit count."""
    total = 0
    for i, line in enumerate(lines, 1):
        for name, text in scan_line(line):
            total += 1
            print("%s:%d [%s] %s" % (source_of_line(i), i, name, text))
    return total


def run_rev_range(rng):
    """Scan added lines of `git diff --unified=0 <rng>`. Returns (checked, hits)."""
    proc = subprocess.run(
        ["git", "diff", "--unified=0", rng],
        capture_output=True, text=True)
    if proc.returncode != 0:
        print("git diff failed for range %r: %s" % (rng, proc.stderr.strip()), file=sys.stderr)
        return (False, 0)
    hits = 0
    checked = False
    cur_file = None
    new_line = 0
    for line in proc.stdout.splitlines():
        if line.startswith("+++ b/"):
            cur_file = line[6:]
            checked = True
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            new_line = int(m.group(1)) if m else 0
        elif line.startswith("+") and not line.startswith("+++"):
            for name, text in scan_line(line[1:]):
                hits += 1
                print("%s:%d [%s] %s" % (cur_file, new_line, name, text))
            new_line += 1
    return (checked, hits)


def run_files(paths):
    hits = 0
    checked = False
    for p in paths:
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError as e:
            print("cannot read %r: %s" % (p, e), file=sys.stderr)
            continue
        checked = True
        hits += check_lines(lines, lambda i, p=p: p)
    return (checked, hits)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rev-range", help="git range, e.g. main..head or HEAD^..HEAD")
    ap.add_argument("--files", nargs="+", help="files to scan whole")
    ap.add_argument("--no-self-test", action="store_true")
    args = ap.parse_args()

    if not args.no_self_test:
        if not self_test():
            print("SELF-TEST FAILED -- results below this line would be unproven", file=sys.stderr)
            return 3
        print("self-test: PASS (all rules exercised, negatives silent)")

    if not args.rev_range and not args.files:
        print("nothing to check: give --rev-range or --files", file=sys.stderr)
        return 2
    if args.rev_range and args.files:
        print("give either --rev-range or --files, not both", file=sys.stderr)
        return 2

    if args.rev_range:
        checked, hits = run_rev_range(args.rev_range)
    else:
        checked, hits = run_files(args.files)

    if not checked:
        print("NOT CHECKED: no input matched (empty diff / no readable files)", file=sys.stderr)
        return 2
    print("checked: clean" if hits == 0 else "hits: %d (adjudicate each; hit = lead, not verdict)" % hits)
    return 0 if hits == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
