from math import exp, log, log1p, sqrt, isfinite

# Shared cue metric; all constants are authored probe assumptions.
SIGMA = (0.35, 0.25, 0.80, 0.80, 1.00)
PROTOTYPES = {
    "fish": [
        (4.0, 0.05, 2.0, 6.25, 0.0),
        (4.0, 0.05, 2.0, 0.0, 7.5 * exp(-0.5)),
        (4.0, 0.05, 2.0, 0.0, 0.0),
    ],
    "crustacean": [(2.0, 0.70, 0.15, 0.50, 0.0)],
    "nonfood": [(1.2, 0.0, 0.15, 0.0, 0.0)],
}
PREFERENCE = {"fish": (1.0, 0.08),
              "crustacean": (0.60, 0.04),
              "nonfood": (0.0, 0.08)}

def embed(raw):
    r, appendage, clearance_lengths, speed_lengths, recent_change_lengths = raw
    return (log(r), appendage, log1p(clearance_lengths),
            log1p(speed_lengths), log1p(recent_change_lengths))

CENTRES = {t: [embed(p) for p in ps] for t, ps in PROTOTYPES.items()}

def evaluate(data, capacity):
    required = ("L", "W", "A", "h", "v", "v_away", "j", "age", "d")
    if any(data.get(k) is None for k in required) or capacity is None:
        return {"status": "Unknown"}
    if not all(isfinite(data[k]) for k in required) or not isfinite(capacity):
        return {"status": "Invalid"}
    if (data["L"] <= 0 or data["W"] <= 0 or capacity <= 0 or
        any(data[k] < 0 for k in ("A", "h", "v", "v_away", "j", "age", "d")) or
        data["v_away"] > data["v"] + 1e-12):
        return {"status": "Invalid"}
    if any(t not in PREFERENCE or PREFERENCE[t] is None for t in CENTRES):
        return {"status": "Unknown"}
    recent = data["j"] * exp(-data["age"] / 1.0)
    x = embed((data["L"]/data["W"], data["A"]/data["L"], data["h"]/data["L"],
               data["v"]/data["L"], recent/data["L"]))
    ds = {t: [sum(((a-b)/s)**2 for a,b,s in zip(x,c,SIGMA)) for c in cs]
          for t,cs in CENTRES.items()}
    if min(min(vals) for vals in ds.values()) > 9.0:
        return {"status": "Unsupported", "D2": ds}
    score = {t: sum(exp(-0.5*d2) for d2 in vals)/len(vals) for t,vals in ds.items()}
    weights = {t: score[t]/sum(score.values()) for t in score}
    motion = 1-exp(-(data["v"]/0.25 + recent/0.50))
    demand = data["d"]/1.0 + data["v_away"]
    effort = 0.50*(demand/capacity)**2
    result = {}
    for t,(affinity,preferred_length) in PREFERENCE.items():
        size = exp(-0.5*(log(data["L"]/preferred_length)/0.70)**2)
        benefit = affinity*size*(1+motion)
        u = max(0.0,benefit-effort)
        result[t] = {"F":size,"B":benefit,"R":u/(1+u)}
    return {"status":"Resolved","weights":weights,"M":motion,"q":demand,"E":effort,
            "targets":result,"R":sum(weights[t]*result[t]["R"] for t in weights)}

def fixture(L=.08,r=4.0,appendage=.05,h=.16,v=.5,j=0.0,age=0.0,d=.2):
    return dict(L=L,W=L/r,A=appendage*L,h=h,v=v,v_away=v,j=j,age=age,d=d)

cases = [
    ("fish_swim_normal",fixture(),1.0),
    ("fish_pause_normal",fixture(v=0,j=.6,age=.5),1.0),
    ("fish_swim_reduced",fixture(),.45),
    ("fish_pause_reduced",fixture(v=0,j=.6,age=.5),.45),
    ("crustacean_crawl",fixture(L=.04,r=2,appendage=.7,h=.006,v=.02),1.0),
    ("nonfood_rest",fixture(r=1.2,appendage=0,h=.012,v=0),1.0),
    ("ambiguous_crawl",fixture(r=2.7,appendage=.35,h=.04,v=.04),1.0),
    ("ambiguous_swim",fixture(r=2.7,appendage=.35,h=.04,v=.50),1.0),
    ("perturbed_fish",fixture(r=3.5,appendage=.10,h=.12,v=.40),1.0),
    ("out_of_support",fixture(r=40),1.0),
    ("missing_appendage",dict(fixture(),A=None),1.0),
]

if __name__ == "__main__":
    import json
    results = {name:evaluate(data,cap) for name,data,cap in cases}
    assert results["fish_swim_normal"]["R"] > results["fish_pause_normal"]["R"]
    assert results["fish_swim_reduced"]["R"] < results["fish_pause_reduced"]["R"]
    assert results["fish_swim_normal"]["weights"] == results["fish_swim_reduced"]["weights"]
    assert results["ambiguous_crawl"]["weights"]["crustacean"] > results["ambiguous_crawl"]["weights"]["fish"]
    assert results["ambiguous_swim"]["weights"]["fish"] > results["ambiguous_swim"]["weights"]["crustacean"]
    assert results["out_of_support"]["status"] == "Unsupported"
    assert results["missing_appendage"]["status"] == "Unknown"
    assert evaluate(dict(fixture(), W=0),1)["status"] == "Invalid"
    assert all(0 <= r["R"] < 1 for r in results.values() if r["status"]=="Resolved")
    assert all(abs(sum(r["weights"].values())-1) < 1e-12 for r in results.values() if r["status"]=="Resolved")
    # Preference changes valuation, not target interpretation.
    before = results["ambiguous_crawl"]["weights"]
    PREFERENCE["crustacean"] = (0.0, 0.04)
    zero_preference = evaluate(cases[6][1],1.0)
    assert zero_preference["weights"] == before
    assert zero_preference["R"] < results["ambiguous_crawl"]["R"]
    print("Checks passed: ranking, geometry/motion interpretation, missing and unsupported inputs, diet/recognition separation.")
    PREFERENCE["crustacean"] = (0.60, 0.04)
    original_fish = PREFERENCE.pop("fish")
    assert evaluate(fixture(),1.0)["status"] == "Unknown"
    PREFERENCE["fish"] = original_fish
    print(json.dumps({n: {"status": r["status"], "weights": r.get("weights"), "R": r.get("R")} for n,r in results.items()}, ensure_ascii=False, indent=2))
