"""Candidate Readiness-side motivation derivation; no authoritative writes.

All parameters are authored fixtures. The load projection below illustrates an
opt-in historical cause kernel; it is not a production consumption reducer.
"""
from math import exp, log, log1p, isfinite, isclose
import json
from target_interpretation_probe import evaluate, cues, facts

def resolve_motivation(reference, period_offset, consumption_load, sensitivity):
    values=(reference,period_offset,consumption_load,sensitivity)
    if any(v is None for v in values):
        return {"status":"Unknown"}
    if not all(isinstance(v,(int,float)) and isfinite(v) for v in values):
        return {"status":"Invalid"}
    if not 0 < reference < 1 or consumption_load < 0 or sensitivity < 0:
        return {"status":"Invalid"}
    eta=log(reference)-log1p(-reference)+period_offset-sensitivity*consumption_load
    if eta >= 0:
        h=1/(1+exp(-eta))
    else:
        e=exp(eta)
        h=e/(1+e)
    return {"status":"Resolved","H":h,"log_odds":eta}

def project_load(load,elapsed_hours,authoritative_increment,half_life_hours):
    """Decay first, then add an already accepted increment at the interval end.

    Call separately for distinct event times. This helper cannot verify event
    authority, attribution, scope or causal cut; production owns those upstream.
    """
    values=(load,elapsed_hours,authoritative_increment,half_life_hours)
    if any(v is None for v in values):
        return {"status":"Unknown"}
    if not all(isinstance(v,(int,float)) and isfinite(v) for v in values):
        return {"status":"Invalid"}
    if min(load,elapsed_hours,authoritative_increment)<0 or half_life_hours<=0:
        return {"status":"Invalid"}
    c=load*2**(-elapsed_hours/half_life_hours)+authoritative_increment
    return {"status":"Resolved","load":c}

def run_scenario(offset,load):
    motivation=resolve_motivation(.60,offset,load,1.50)
    if motivation["status"]!="Resolved":
        return motivation
    h=motivation["H"]
    swim=evaluate(cues(),facts(),1.0,h)
    pause=evaluate(cues(),facts(v=0,j=.6,age=.5),1.0,h)
    return {"H":h,"swim":swim["local_response"],"pause":pause["local_response"]}

def checks(results):
    assert results["strong_unfed"]["swim"] > results["strong_unfed"]["pause"]
    assert results["strong_recently_fed"]["swim"] < results["strong_recently_fed"]["pause"]
    assert results["strong_unfed"]["H"] > results["strong_recently_fed"]["H"]
    assert (results["strong_recently_fed"]["H"] <
            results["load_half"]["H"] < results["load_quarter"]["H"] <
            results["strong_unfed"]["H"])
    # Consuming a resolved motivation never changes prey interpretation or capacity.
    strong=evaluate(cues(),facts(),1.0,results["strong_unfed"]["H"])
    weak=evaluate(cues(),facts(),1.0,results["strong_recently_fed"]["H"])
    assert strong["targets"]["fish"]["presentation"]==weak["targets"]["fish"]["presentation"]
    assert strong["targets"]["fish"]["cost"]==weak["targets"]["fish"]["cost"]
    # The reference is identifiable at the named reference period and zero load.
    assert isclose(resolve_motivation(.6,0,0,1.5)["H"],.6)
    # An interval split does not invent extra consumption or recovery.
    a=project_load(1,2,0,4)["load"]
    assert isclose(project_load(a,2,0,4)["load"],project_load(1,4,0,4)["load"])
    assert isclose(project_load(1,4,.3,4)["load"],.8)
    assert resolve_motivation(.6,.8,None,1.5)["status"]=="Unknown"
    assert resolve_motivation(.6,.8,-1,1.5)["status"]=="Invalid"
    assert project_load(None,1,0,4)["status"]=="Unknown"
    # Strong motivation cannot create a prey interpretation unsupported by cues.
    unsupported=evaluate(cues(r=1),facts(v=0),1.0,1.0)
    assert unsupported["status"]=="UnsupportedTarget"
    assert "local_response" not in unsupported

if __name__=="__main__":
    half=project_load(1,4,0,4)["load"]
    quarter=project_load(1,8,0,4)["load"]
    results={
        "weak_period":run_scenario(-.8,0),
        "strong_unfed":run_scenario(.8,0),
        "strong_recently_fed":run_scenario(.8,1),
        "load_half":run_scenario(.8,half),
        "load_quarter":run_scenario(.8,quarter),
    }
    checks(results)
    print("All motivation and integration checks passed.")
    print(json.dumps(results,ensure_ascii=False,indent=2))
