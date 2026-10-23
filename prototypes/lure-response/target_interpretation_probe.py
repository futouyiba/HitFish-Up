"""Development probe: cue-supported prey interpretation, then conditional states.

All thresholds, prototypes, preferences and utilities are authored assumptions.
Not a biological classifier or production captureRetention implementation.
Run: python prototypes/lure-response/target_interpretation_probe.py
"""
from copy import deepcopy
from math import exp, log, log1p, isfinite
import json

# A route is a conjunction; routes are alternatives for target support only.
# False means this route supplies no support, not biological impossibility.
ROUTES = {
    "fish": [
        ("elongated_body", (("r", "ge", 3.0), ("filaments", "le", 0.30))),
        ("compact_oscillating", (("r", "le", 2.5), ("oscillation", "ge", 0.50))),
        ("moving_flash", (("flash", "ge", 0.50),)),
        ("filament_composite", (("filaments", "ge", 0.40),)),
    ],
    "crustacean": [
        ("filament_composite", (("filaments", "ge", 0.40),)),
        ("front_pair", (("front_pair", "ge", 0.50),)),
        ("compact_bottom_contact", (
            ("r", "le", 2.5), ("impact", "ge", 0.50), ("bottom", "le", 0.50))),
    ],
    "frog": [
        ("compact_rear_pair", (("r", "le", 2.5), ("rear_pair", "ge", 0.50))),
    ],
}

# State metric on [log1p(speed/length), log1p(recent_change/length),
# vertical_speed/length]. Positive vertical speed is downward.
SIGMA = (0.65, 1.0, 1.0)
# name, speed in bodylengths/s, effective recent change in bodylengths/s,
# downward speed in bodylengths/s, value multiplier, optional relative layer
STATES = {
    "fish": [
        ("swimming", 6.25, 0.0, 0.0, 1.865, None),
        ("post_burst_pause", 0.0, 7.5*exp(-0.5), 0.0, 1.517, None),
        ("still", 0.0, 0.0, 0.0, 1.0, None),
        ("falling", 2.0, 0.0, 2.0, 1.60, None),
    ],
    "crustacean": [
        ("bottom_crawl", 0.50, 0.0, 0.0, 1.60, ("bottom", 0.15, 0.60)),
        ("bottom_still", 0.0, 0.0, 0.0, 1.30, ("bottom", 0.15, 0.60)),
        ("near_bottom_escape", 5.0, 5.0, 0.0, 1.80, ("bottom", 0.50, 0.60)),
    ],
    "frog": [
        ("surface_swim", 1.50, 0.0, 0.0, 1.60, ("surface", 0.0, 0.50)),
        ("surface_pause", 0.0, 0.0, 0.0, 1.30, ("surface", 0.0, 0.50)),
        ("post_kick_surface_pause", 0.0, 3.0, 0.0, 1.80, ("surface", 0.0, 0.50)),
    ],
}
PREFERENCES = {"fish": (1.0, 0.08), "crustacean": (0.60, 0.04),
               "frog": (0.70, 0.06)}

def condition(cues, term):
    key, op, threshold = term
    value = cues.get(key)
    if value is None:
        return None
    return value >= threshold if op == "ge" else value <= threshold

def route_support(cues, terms):
    values = [condition(cues, term) for term in terms]
    if False in values:
        return False
    return None if None in values else True

def interpret_support(cues):
    result = {}
    for target, routes in ROUTES.items():
        flags = [(name, route_support(cues, terms)) for name, terms in routes]
        admitted = [name for name, flag in flags if flag is True]
        result[target] = {
            "status": "Supported" if admitted else (
                "Unknown" if any(flag is None for _,flag in flags) else "NoSupport"),
            "routes": admitted,
        }
    return result

def state_matches(target, facts, cues):
    keys = ("L", "v", "j", "age", "vertical_v")
    if any(facts.get(k) is None for k in keys):
        return {"status": "Unknown"}
    length = facts["L"]
    x = (log1p(facts["v"]/length),
         log1p(facts["j"]*exp(-facts["age"]/1.0)/length),
         facts["vertical_v"]/length)
    matched = []
    for name,u,e,w,gain,layer in STATES[target]:
        centre = (log1p(u),log1p(e),w)
        d2 = sum(((a-b)/s)**2 for a,b,s in zip(x,centre,SIGMA))
        if layer is not None:
            key,mean,sigma = layer
            if cues.get(key) is None:
                return {"status":"Unknown"}
            d2 += ((cues[key]-mean)/sigma)**2
        matched.append((d2,name,gain))
    matched.sort()
    best = matched[0]
    # No target switching and no zero response for an uncovered state.
    if best[0] > 9.0:
        return {"status":"UnsupportedState","best_distance2":best[0]}
    ties = [m for m in matched if abs(m[0]-best[0]) < 1e-9]
    if len(ties) > 1:
        return {"status":"AmbiguousState","states":[m[1] for m in ties]}
    return {"status":"Resolved","state":best[1],
            "fit":exp(-best[0]/2),"gain":best[2]}

def evaluate(cues, facts, capacity, feeding_motivation, preferences=None):
    preferences = PREFERENCES if preferences is None else preferences
    # Typed numeric inputs only; Unknown remains distinct from known absence.
    for value in list(cues.values()) + list(facts.values()) + [capacity, feeding_motivation]:
        if value is not None and (not isinstance(value,(float,int)) or not isfinite(value)):
            return {"status":"Invalid"}
    if facts.get("L") is not None and facts["L"] <= 0:
        return {"status":"Invalid"}
    if capacity is not None and capacity <= 0:
        return {"status":"Invalid"}
    if feeding_motivation is not None and not 0 <= feeding_motivation <= 1:
        return {"status":"Invalid"}
    if any(facts.get(k) is not None and facts[k] < 0
           for k in ("v","j","age","d","v_away")):
        return {"status":"Invalid"}
    if (facts.get("v") is not None and facts.get("v_away") is not None
            and facts["v_away"] > facts["v"]):
        return {"status":"Invalid"}
    support = interpret_support(cues)
    outputs = {}
    for target, entry in support.items():
        if entry["status"] != "Supported":
            outputs[target] = entry
            continue
        state = state_matches(target,facts,cues)
        out = dict(entry, presentation=state)
        if state["status"] != "Resolved":
            outputs[target] = out
            continue
        if (preferences.get(target) is None or capacity is None or feeding_motivation is None
                or facts.get("d") is None or facts.get("v_away") is None):
            out["evaluation_status"] = "Unknown"
            outputs[target] = out
            continue
        affinity, preferred_length = preferences[target]
        size = exp(-0.5*(log(facts["L"]/preferred_length)/0.70)**2)
        # Each fitted state has a conditional authored value. No global M bonus.
        # The current probe uses state fit once as the numeric support proxy.
        # A future joint support S must replace this proxy, not multiply it again.
        support_strength = state["fit"]
        benefit_before_motivation = affinity*size*support_strength*state["gain"]
        benefit = feeding_motivation*benefit_before_motivation
        demand = facts["d"]/1.0 + facts["v_away"]
        cost = 0.50*(demand/capacity)**2
        u = max(0.0,benefit-cost)
        out.update(evaluation_status="Resolved",benefit=benefit,cost=cost,
                   benefit_before_motivation=benefit_before_motivation,
                   feeding_motivation=feeding_motivation,
                   support_strength=support_strength,
                   local_response=u/(1+u))
        outputs[target] = out
    supported = [t for t,v in support.items() if v["status"]=="Supported"]
    incomplete = any(v["status"]=="Unknown" for v in support.values()) or any(
        outputs[t].get("evaluation_status")!="Resolved" for t in supported)
    if incomplete:
        status = "ResolutionIncomplete"
    elif not supported:
        status = "UnsupportedTarget"
    elif len(supported) > 1:
        status = "MultipleInterpretations"
    else:
        status = "SingleInterpretation"
    packet = {"status":status, "targets":outputs}
    if status == "SingleInterpretation":
        packet["local_response"] = outputs[supported[0]]["local_response"]
    # Multiple interpretations have no final scalar: aggregation remains open.
    return packet

def cues(r=4.0,filaments=0.0,front_pair=0.0,rear_pair=0.0,
         flash=0.0,oscillation=0.0,impact=0.0,bottom=2.0,surface=5.0):
    return dict(r=r,filaments=filaments,front_pair=front_pair,rear_pair=rear_pair,
                flash=flash,oscillation=oscillation,impact=impact,
                bottom=bottom,surface=surface)

def facts(L=.08,v=.5,j=0.0,age=0.0,vertical_v=0.0,d=.20,v_away=None):
    # Fixtures choose a radial component consistent with full 3D speed.
    return dict(L=L,v=v,j=j,age=age,vertical_v=vertical_v,d=d,
                v_away=v if v_away is None else v_away)

def build_cases():
    return {
        "minnow_swim":(cues(),facts(),1.0),
        "minnow_bottom_drag":(cues(bottom=.15,impact=.9),facts(v=.04),1.0),
        "minnow_pause":(cues(),facts(v=0,j=.6,age=.5),1.0),
        "minnow_swim_reduced":(cues(),facts(),.45),
        "minnow_pause_reduced":(cues(),facts(v=0,j=.6,age=.5),.45),
        "tube_falling":(cues(r=2.8,filaments=.8,bottom=2),facts(v=.16,vertical_v=.16,v_away=0),1.0),
        "tube_bottom_crawl":(cues(r=2.8,filaments=.8,bottom=.15),facts(v=.04),1.0),
        "compact_bottom_contact":(cues(r=2,oscillation=.8,impact=.9,bottom=.15),facts(v=.04),1.0),
        "frog_surface_pause":(cues(r=1.8,rear_pair=.8,surface=0,bottom=8),facts(L=.06,v=0),1.0),
        "frog_surface_swim":(cues(r=1.8,rear_pair=.8,surface=0,bottom=8),facts(L=.06,v=.09),1.0),
        "frog_deep_pause":(cues(r=1.8,rear_pair=.8,surface=8,bottom=2),facts(L=.06,v=0),1.0),
        "no_cue_support":(cues(r=1),facts(v=0),1.0),
        "unknown_filaments":(cues(filaments=None),facts(),1.0),
    }

def checks(results):
    def admitted(name):
        return {t for t,v in results[name]["targets"].items() if v["status"]=="Supported"}
    assert admitted("minnow_bottom_drag")=={"fish"}
    assert admitted("tube_falling")==admitted("tube_bottom_crawl")=={"fish","crustacean"}
    assert results["tube_falling"]["targets"]["fish"]["presentation"]["state"]=="falling"
    assert results["tube_bottom_crawl"]["targets"]["crustacean"]["presentation"]["state"]=="bottom_crawl"
    assert admitted("compact_bottom_contact")=={"fish","crustacean"}
    assert results["frog_surface_pause"]["local_response"] > 0
    assert results["frog_surface_swim"]["local_response"] > 0
    assert admitted("frog_deep_pause")=={"frog"}
    assert results["frog_deep_pause"]["status"]=="ResolutionIncomplete"
    assert results["no_cue_support"]["status"]=="UnsupportedTarget"
    assert results["unknown_filaments"]["status"]=="ResolutionIncomplete"
    assert results["minnow_swim"]["local_response"] > results["minnow_pause"]["local_response"]
    assert results["minnow_swim_reduced"]["local_response"] < results["minnow_pause_reduced"]["local_response"]
    assert "local_response" not in results["tube_falling"]
    changed = deepcopy(PREFERENCES)
    changed["fish"]=(0.0,.08)
    a=evaluate(cues(),facts(),1.0,1.0)
    b=evaluate(cues(),facts(),1.0,1.0,changed)
    assert a["targets"]["fish"]["presentation"]==b["targets"]["fish"]["presentation"]
    assert a["local_response"]>b["local_response"]
    missing=deepcopy(PREFERENCES)
    del missing["fish"]
    assert evaluate(cues(),facts(),1.0,1.0,missing)["status"]=="ResolutionIncomplete"
    weak=evaluate(cues(),facts(),1.0,0.3)
    weak_pause=evaluate(cues(),facts(v=0,j=.6,age=.5),1.0,0.3)
    assert weak["local_response"] < weak_pause["local_response"]
    assert weak["targets"]["fish"]["cost"] == a["targets"]["fish"]["cost"]
    assert weak["targets"]["fish"]["presentation"] == a["targets"]["fish"]["presentation"]
    assert evaluate(cues(),facts(),1.0,None)["status"]=="ResolutionIncomplete"
    zero=evaluate(cues(),facts(),1.0,0.0)
    assert zero["targets"]["fish"]["status"]=="Supported" and zero["local_response"]==0
    assert evaluate(cues(),facts(),1.0,1.1)["status"]=="Invalid"
    # Known false conjunct blocks a route even if another conjunct is missing.
    assert route_support({"r":4.0},(("r","le",2.5),("impact","ge",.5))) is False

if __name__=="__main__":
    results={name:evaluate(*inputs,feeding_motivation=1.0) for name,inputs in build_cases().items()}
    checks(results)
    brief={}
    for name,out in results.items():
        brief[name]={"status":out["status"],"targets":{}}
        for target,entry in out["targets"].items():
            if entry["status"]=="Supported":
                brief[name]["targets"][target] = {
                    "state":entry["presentation"].get("state"),
                    "state_status":entry["presentation"]["status"],
                    "fit":entry["presentation"].get("fit"),
                    "R":entry.get("local_response"),
                }
    print("All structural checks passed.")
    print(json.dumps(brief,ensure_ascii=False,indent=2))
