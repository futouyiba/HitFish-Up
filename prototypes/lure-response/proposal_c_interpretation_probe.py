"""Proposal C development probe: samples -> features -> local evidence -> prey map.
All evidence values, thresholds and applicability choices are authored assumptions.
Run: python prototypes/lure-response/proposal_c_interpretation_probe.py
This is not a production perception system or a calibrated biological classifier.
"""
from copy import deepcopy
from math import sqrt, sin, pi, isfinite, isclose
import json

TARGETS = ("small_baitfish", "crayfish", "frog")
DEFINITIONS = {
    "tube_fish": ("small_baitfish", .4, (("falling_sway", .75),)),
    "tube_cray": ("crayfish", .4, (("bottom_appendage", .75),)),
    "skirt_fish": ("small_baitfish", .4, (("falling_sway", .75),)),
    "skirt_cray": ("crayfish", .4, (("bottom_appendage", .75),)),
    "tail_fish": ("small_baitfish", .9, ()),
    "craw_cray": ("crayfish", .9, ()),
    "frog_shape": ("frog", .9, ()),
}

def binding(evidence, source, active=True):
    return dict(evidence=evidence, source=source, active=active)

def rig(parts, bindings, covered=TARGETS):
    return dict(length_m=.08, parts=parts, bindings=bindings, covered=covered)

RIGS = {
    "tube": rig(("body", "rear_bundle"), (
        binding("tube_fish", "rear_bundle"), binding("tube_cray", "rear_bundle"))),
    "tail": rig(("fish_body",), (binding("tail_fish", "fish_body"),)),
    "skirt_tail": rig(("skirt", "fish_body"), (
        binding("skirt_fish", "skirt"), binding("skirt_cray", "skirt"),
        binding("tail_fish", "fish_body"))),
    "skirt_craw": rig(("skirt", "craw_body"), (
        binding("skirt_fish", "skirt"), binding("skirt_cray", "skirt"),
        binding("craw_cray", "craw_body"))),
    "frog": rig(("frog_body",), (binding("frog_shape", "frog_body"),), ("frog",)),
}

def norm(v):
    return sqrt(sum(x*x for x in v))

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))

def sat(v):
    return min(1., max(0., v))

def complete_times(times, start, end):
    if not times:
        return False
    if any(not isfinite(t) for t in times):
        raise ValueError("Non-finite sample time")
    if any(b<=a for a,b in zip(times,times[1:])):
        raise ValueError("Sample times must increase")
    return len(times)>=2 and isclose(times[0],start,abs_tol=1e-12) and isclose(times[-1],end,abs_tol=1e-12)

def below_duration(a, b, dt, threshold):
    if a<=threshold and b<=threshold:
        return dt
    if a>threshold and b>threshold:
        return 0.
    crossing=(threshold-a)/(b-a)
    return dt*(crossing if a<=threshold else 1-crossing)

def extract(body, widths, length, window=(0.,1.)):
    """Piecewise-linear records, z upward; no absent stream is filled with zero."""
    start,end=window
    if length<=0 or not isfinite(length) or end<=start:
        raise ValueError("Invalid reference length/window")
    result=dict(D=None,W=None,B=None,X=None,O={})
    if body is not None and complete_times([s["t"] for s in body],start,end):
        points=[s["p"] for s in body]
        if any(len(p)!=3 or any(not isfinite(x) for x in p) for p in points):
            raise ValueError("Invalid position")
        chord=sub(points[-1],points[0])
        chord2=sum(x*x for x in chord)
        deviations=[]
        for p in points:
            offset=sub(p,points[0])
            if chord2<1e-24:
                deviations.append(norm(offset))
            else:
                projection=sum(a*b for a,b in zip(offset,chord))/chord2
                deviations.append(norm(tuple(a-projection*b for a,b in zip(offset,chord))))
        result["D"]=max(0.,points[0][2]-points[-1][2])/length
        result["W"]=max(deviations)/length
        result["X"]=sum(norm(sub(b[:2],a[:2])) for a,b in zip(points,points[1:]))/length
        gaps=[s.get("bottom_gap_m") for s in body]
        if all(g is not None for g in gaps):
            if any(not isfinite(g) or g<0 for g in gaps):
                raise ValueError("Invalid bottom gap")
            result["B"]=sum(below_duration(a,b,s2["t"]-s1["t"],.5*length)
                for a,b,s1,s2 in zip(gaps,gaps[1:],body,body[1:]))/(end-start)
    for source, samples in widths.items():
        if samples is None or not complete_times([s[0] for s in samples],start,end):
            result["O"][source]=None
            continue
        values=[s[1] for s in samples]
        if any(not isfinite(v) or v<0 for v in values):
            raise ValueError("Invalid width")
        result["O"][source]=(max(values)-min(values))/length
    return result

def ramp(value, lo, hi):
    if value is None:
        return (0.,1.)
    value=sat((value-lo)/(hi-lo))
    return (value,value)

def and_bounds(*bounds):
    return (min(b[0] for b in bounds), min(b[1] for b in bounds))

def pattern_bounds(pattern, features, source):
    if pattern=="falling_sway":
        return and_bounds(ramp(features["D"],0.,1.),ramp(features["W"],0.,.5))
    if pattern=="bottom_appendage":
        return and_bounds(ramp(features["B"],.2,.7),ramp(features["X"],0.,.5),
                          ramp(features["O"].get(source),0.,.15))
    raise ValueError("Unknown pattern")

def packet(lo,hi):
    if isclose(lo,hi,rel_tol=0.,abs_tol=1e-12):
        return dict(status="Resolved",support=lo)
    return dict(status="Unknown",lower=lo,upper=hi)

def evaluate(config, body=None, widths=None, window=(0.,1.)):
    covered=set(config["covered"])
    if not covered<=set(TARGETS):
        raise ValueError("Unknown target in coverage")
    features=extract(body,widths or {},config["length_m"],window)
    grouped={k:[] for k in covered}
    trace=[]
    for item in config["bindings"]:
        if not isinstance(item["active"],bool):
            raise ValueError("Applicability must be resolved at authoring")
        if not item["active"]:
            trace.append(dict(evidence=item["evidence"],status="NotApplicable"))
            continue
        if item["source"] not in config["parts"]:
            raise ValueError("Binding refers to absent part")
        target,base,routes=DEFINITIONS[item["evidence"]]
        if target not in covered or not 0<=base<=1:
            raise ValueError("Invalid evidence/coverage")
        lo=hi=base
        for pattern,ceiling in routes:
            if not base<=ceiling<=1:
                raise ValueError("Ceiling is local to this evidence")
            f_lo,f_hi=pattern_bounds(pattern,features,item["source"])
            lo=max(lo,base+(ceiling-base)*f_lo)
            hi=max(hi,base+(ceiling-base)*f_hi)
        grouped[target].append((lo,hi))
        trace.append(dict(evidence=item["evidence"],**packet(lo,hi)))
    output={}
    for target in TARGETS:
        if target not in covered:
            output[target]=dict(status="Uncovered")
        else:
            candidates=grouped[target] or [(0.,0.)]
            output[target]=packet(max(x[0] for x in candidates),max(x[1] for x in candidates))
    return dict(targets=output,features=features,evidence=trace)

def body_case(kind,n=20):
    result=[]
    for i in range(n+1):
        t=i/n
        if kind=="curved_fall":
            p=(.032*sin(pi*t),0.,-.16*t)
            gap=1.+p[2]
        elif kind=="straight_fall":
            p=(.064*t,0.,-.16*t)
            gap=1.+p[2]
        elif kind=="bottom":
            p=(.096*t,0.,.02)
            gap=.02
        elif kind=="cross_bottom":
            p=(.096*t,0.,.06)
            gap=.06-.04*t
        else:
            raise ValueError(kind)
        result.append(dict(t=t,p=p,bottom_gap_m=gap))
    return result

def width_case(delta=.02,n=20):
    return [(i/n,.008+delta*i/n) for i in range(n+1)]

def build_cases():
    return {
        "tube_curved_fall":evaluate(RIGS["tube"],body_case("curved_fall"),{"rear_bundle":width_case()}),
        "tube_straight_fall":evaluate(RIGS["tube"],body_case("straight_fall"),{"rear_bundle":width_case()}),
        "tube_bottom":evaluate(RIGS["tube"],body_case("bottom"),{"rear_bundle":width_case()}),
        "tube_bottom_weak":evaluate(RIGS["tube"],body_case("bottom"),{"rear_bundle":width_case(.0024)}),
        "tube_bottom_missing_width":evaluate(RIGS["tube"],body_case("bottom")),
        "tube_fall_missing_width":evaluate(RIGS["tube"],body_case("curved_fall")),
        "tube_bottom_crossing":evaluate(RIGS["tube"],body_case("cross_bottom"),{"rear_bundle":width_case()}),
        "skirt_tail_curved":evaluate(RIGS["skirt_tail"],body_case("curved_fall"),{"skirt":width_case()}),
        "skirt_craw_missing_width":evaluate(RIGS["skirt_craw"],body_case("bottom")),
        "tail_without_history":evaluate(RIGS["tail"]),
        "frog_without_history":evaluate(RIGS["frog"]),
    }

def checks(cases):
    assert isclose(cases["tube_curved_fall"]["features"]["W"],.4,abs_tol=1e-12)
    assert isclose(cases["tube_straight_fall"]["features"]["W"],0.,abs_tol=1e-12)
    # Time under a threshold is integrated, not counted as below-threshold samples.
    for n in (7,20,80):
        f=extract(body_case("cross_bottom",n),{},.08)
        assert isclose(f["B"],.5,abs_tol=1e-12)
    target=lambda name,k:cases[name]["targets"][k]
    assert isclose(target("tube_curved_fall","small_baitfish")["support"],.68)
    assert isclose(target("tube_bottom_weak","crayfish")["support"],.47)
    assert isclose(target("tube_bottom_crossing","crayfish")["support"],.61)
    assert target("tube_bottom_missing_width","crayfish")==dict(status="Unknown",lower=.4,upper=.75)
    assert target("tube_fall_missing_width","crayfish")==dict(status="Resolved",support=.4)
    assert target("skirt_craw_missing_width","crayfish")==dict(status="Resolved",support=.9)
    assert target("tail_without_history","small_baitfish")==dict(status="Resolved",support=.9)
    assert target("frog_without_history","crayfish")["status"]=="Uncovered"
    # An assembly's .9 does not alter or invalidate a skirt route capped at .75.
    trace=cases["skirt_tail_curved"]["evidence"]
    assert isclose(next(x for x in trace if x["evidence"]=="skirt_fish")["support"],.68)
    assert target("skirt_tail_curved","small_baitfish")["support"]==.9
    cfg=deepcopy(RIGS["skirt_tail"])
    cfg["bindings"][-1]["active"]=False
    hidden=evaluate(cfg,body_case("bottom"),{"skirt":width_case()})
    assert hidden["targets"]["small_baitfish"]["support"]==.4
    cfg=deepcopy(RIGS["tail"])
    cfg["bindings"][0]["source"]="absent"
    try:
        evaluate(cfg)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid binding must not become zero support")

if __name__=="__main__":
    results=build_cases()
    checks(results)
    print("Geometry, integration, binding and missing-data checks passed.")
    for name,result in results.items():
        print(json.dumps(dict(case=name,features=result["features"],targets=result["targets"]),
                         ensure_ascii=False))
