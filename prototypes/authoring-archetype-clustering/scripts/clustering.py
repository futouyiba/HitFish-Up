#!/usr/bin/env python3
"""Run the transparent Authoring Archetype clustering probe."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_cluster import (pairwise_l1, fcluster_average, kmedoids, greedy_cover,
                         adjusted_rand_index, normalized_mutual_info)
from lib_signature import TEMP_GRID, TIME_PERIODS, FEEDING_LAYERS, temperature_signature

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def f(v, default=np.nan):
    try: return float(str(v).strip())
    except (TypeError, ValueError): return default


def scale01(v, lo, hi):
    x = f(v)
    return 0.0 if np.isnan(x) else (x-lo)/(hi-lo)


def csv_rows(path, name_col):
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def main():
    rows = csv_rows(RAW / "feishu_v3_selected_fields.csv", "鱼种")
    # join Notion auxiliary rows by source record ID where needed
    ref = {r["源记录ID"]: r for r in csv_rows(RAW / "fish_reference_267.csv", "中文名")}
    n = len(rows)
    names = [r["鱼种"] for r in rows]

    temps, structures, times, layers = [], [], [], []
    missing = {k: 0 for k in ["temperature", "structure", "time", "feeding_layer"]}
    all_structures = sorted({s for r in rows for s in r["FG推荐结构体"].split("|") if s})
    for r in rows:
        a,b,c,d = [f(r[k]) for k in ["资料水温下限(°C)", "资料水温上限(°C)", "最喜欢的温度(°C)", "最喜欢的温度(°C)"]]
        # Derive comfort from favourite point; actual acceptable range is source.
        accept_lo, accept_hi = f(r["资料水温下限(°C)"]), f(r["资料水温上限(°C)"])
        fav = f(r["最喜欢的温度(°C)"])
        half = .15 * (accept_hi - accept_lo)
        fav_lo, fav_hi = max(accept_lo, fav-half), min(accept_hi, fav+half)
        temps.append(temperature_signature(accept_lo, fav_lo, fav_hi, accept_hi, "LINEAR"))
        ss = set(r["FG推荐结构体"].split("|")) - {""}
        if not ss: missing["structure"] += 1
        structures.append([1.0 if s in ss else 0.0 for s in all_structures])
        tv = [f(r[f"period{x}"]) for x in ["0_3","3_6","6_9","9_12","12_15","15_18","18_21","21_24"]]
        if any(np.isnan(tv)): missing["time"] += 1
        m = np.nanmax(tv) if not all(np.isnan(tv)) else 1.0
        times.append([0.0 if np.isnan(x) else x/m if m else 0.0 for x in tv])
        lv = [f(r["表层亲和系数"]), f(r["中层亲和系数"]), f(r["底层亲和系数"])]
        if any(np.isnan(lv)): missing["feeding_layer"] += 1
        layers.append([0.0 if np.isnan(x) else x/10.0 for x in lv])
    X = {"temperature": np.array(temps), "structure": np.array(structures),
         "time": np.array(times), "feeding_layer": np.array(layers)}
    D = {k: pairwise_l1(v) for k,v in X.items()}
    Dj = sum(D.values()) / 4.0
    # Ward-like interpretable cuts. epsilon is average effect difference.
    epsilons = [0.05, .10, .15, .20, .25, .30]
    curve=[]
    for e in epsilons:
        med, assignment = greedy_cover(Dj, e)
        nearest = Dj[:, med].min(axis=1)
        # Radius cover is exact by construction (singletons are allowed).
        # Report the non-singleton coverage separately: fish covered by an
        # archetype that also serves at least one other fish.
        member_counts = np.bincount(assignment, minlength=len(med))
        shared = member_counts[assignment] > 1
        curve.append({"allowed_error":e,"archetypes":len(med),
                      "coverage":float(np.mean(shared)),
                      "exact_radius_coverage":float(np.mean(nearest<=e)),
                      "median_override_ratio":float(np.median(nearest)),
                      "p90_override_ratio":float(np.quantile(nearest,.90)),
                      "fields_reused_per_species":float(4*(1-np.minimum(nearest/e,1)) .mean()) if e else 0,
                      "fields_modified_per_species":float(4-4*(1-np.minimum(nearest/e,1)).mean()) if e else 4})
    # Component cuts at a common 0.15 tolerance for consistency evidence.
    labels = {k:fcluster_average(D[k], .15) for k in D}
    labels["joint"] = fcluster_average(Dj, .15)
    consistency=[]
    for a in ["structure","time","feeding_layer"]:
        consistency.append({"a":"temperature","b":a,
            "ARI":adjusted_rand_index(labels["temperature"],labels[a]),
            "NMI":normalized_mutual_info(labels["temperature"],labels[a])})
    for a,b in [("structure","time"),("structure","feeding_layer"),("time","feeding_layer")]:
        consistency.append({"a":a,"b":b,"ARI":adjusted_rand_index(labels[a],labels[b]),"NMI":normalized_mutual_info(labels[a],labels[b])})
    # 3–5 outliers at 0.15 joint radius: highest nearest-medoid distance.
    med, ass = greedy_cover(Dj,.15); dist=Dj[:,med].min(axis=1)
    out_idx=np.argsort(-dist)[:5]
    assignments=[]
    for i,name in enumerate(names):
        assignments.append({"species":name, **{k:int(labels[k][i]) for k in labels},
                            "joint_nearest_distance":float(dist[i]),"outlier":bool(i in out_idx)})
    metrics={"status":"PROBE_ONLY_NOT_FORMAL_0_3_4_CONFIG","n_species":n,
      "sources":{"feishu_selected_fields":"SOURCE-LINKED, 267 rows","notion_reference":"SOURCE snapshot 2026-09-08, 267 rows"},
      "effect_signature":{"temperature_points":len(TEMP_GRID),"structure_dimensions":len(all_structures),"time_dimensions":8,"feeding_layer_dimensions":3},
      "missing_fields":missing,"distance_definition":"mean absolute difference per signature dimension; joint is equal-weight mean of four component distances",
      "component_cluster_counts_0_15":{k:int(len(np.unique(v))) for k,v in labels.items()},
      "component_outlier_ratio_0_15":{k:float(np.mean(D[k].min(axis=1) > .15)) for k in D},
      "cluster_within_mean_distance_0_15":{k:float(np.mean([D[k][labels[k]==c][:,labels[k]==c].mean() for c in np.unique(labels[k])])) for k in D},
      "compression_curve":curve,"cross_component_consistency":consistency,
      "outlier_species":[{"species":names[i],"distance":float(dist[i])} for i in out_idx],
      "caveats":["Structure signature is FG推荐结构体 presence, not formal 25-Type affinity profile.","Time signature uses old 8 period source values; 0.3.4 requires 5 periods and forbids automatic migration.","Temperature comfort band is derived from favourite point; falloff_shape and temp_threshold unavailable.","No ResolvedBakeSubjectConfig / Engagement Mode / FishQuality production snapshot was available."]}
    (OUT/"metrics.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding="utf-8")
    with (OUT/"metrics.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(curve[0]));w.writeheader();w.writerows(curve)
    with (OUT/"cluster_assignments.csv").open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(assignments[0]));w.writeheader();w.writerows(assignments)
    # human-readable case readback
    stable=np.argsort(dist)[:3]; boundary=np.argsort(np.abs(dist-.15))[:2]
    lines=["# Cluster case readback\n","> All clusters are probe labels, not biological families or Runtime identities.\n"]
    for title,idxs in [("Stable (nearest to a joint medoid)",stable),("Boundary (near epsilon=0.15)",boundary),("Outliers (farthest)",out_idx)]:
        lines += [f"## {title}\n"]
        for i in idxs:
            lines.append(f"- **{names[i]}** — joint distance `{dist[i]:.3f}`; clusters " + ", ".join(f"{k}={labels[k][i]}" for k in labels) + ".\n")
            lines.append(f"  - Temperature source range: {rows[i]['资料水温下限(°C)']}–{rows[i]['资料水温上限(°C)']}°C; favourite `{rows[i]['最喜欢的温度(°C)']}`; derived signature only.\n")
            lines.append(f"  - Structure tags: {rows[i]['FG推荐结构体'] or 'missing'}; time source: {rows[i]['时段偏好']}; layer: {rows[i]['候选水层']} / {rows[i]['表层亲和系数']},{rows[i]['中层亲和系数']},{rows[i]['底层亲和系数']}.\n")
            lines.append("  - Archetype override interpretation: replace the differing signature dimensions; this is a proxy, not a persisted Override count.\n")
    (OUT/"cases.md").write_text("".join(lines),encoding="utf-8")
    print(json.dumps({"n":n,"curve":curve,"cluster_counts":metrics["component_cluster_counts_0_15"],"outliers":metrics["outlier_species"]},ensure_ascii=False,indent=2))

if __name__ == "__main__": main()
