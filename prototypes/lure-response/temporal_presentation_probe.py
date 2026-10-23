"""Temporal development probe. Authored assumptions, not bite probabilities.
Run beside target_interpretation_probe.py. Reuses its state/response rules unchanged.
No fish pursuit. One horizontal radial-away presentation over two seconds.
"""
import math
import json
import target_interpretation_probe as m

def v_at(kind,t):
    if kind=="steady": return .1
    if kind=="walk_stop":
        if t<.25: return .2*t/.25
        if t<1: return .2
        if t<1.25: return .2*(1.25-t)/.25
        return 0.
    if kind=="repeated_jerk":
        phase=t%.5
        if phase<.05: return phase/.05
        if phase<.10: return (.10-phase)/.05
        return 0.
    if t<.1: return .8*t/.1
    if t<.25: return .8
    if t<.35: return .8*(.35-t)/.1
    return 0.
def simulate(kind,dt=.01,capacity=.45):
    assert dt>0 and abs(.05/dt-round(.05/dt))<1e-9
    assert abs(2/dt-round(2/dt))<1e-9
    d=.2; memory=0.; rows=[]; cue_prev=0.; last_v=v_at(kind,0.)
    for i in range(round(2/dt)+1):
        t=i*dt; v=v_at(kind,t)
        if i: d+=.5*(last_v+v)*dt; memory*=math.exp(-dt)
        if i%round(.05/dt)==0:
            memory=max(memory,abs(v-cue_prev)/.08)
            cue_prev=v
        out=m.evaluate(m.cues(),m.facts(v=v,j=memory*.08,age=0,d=d),capacity,.6)
        target=out["targets"]["fish"]
        rows.append(dict(t=t,v=v,d=d,M=memory,state=target["presentation"].get("state"),
                         status=out["status"],R=out.get("local_response"),
                         B=target.get("benefit"),E=target.get("cost")))
        last_v=v
    return rows


def diagnostic_mean(rows):
    # Time mean is a curve diagnostic only, not a sequence response or bite chance.
    return sum((a["R"]+b["R"])*.5*(b["t"]-a["t"])
               for a,b in zip(rows,rows[1:]))/(rows[-1]["t"]-rows[0]["t"])

def checks():
    kinds=("steady","walk_stop","jerk_pause","repeated_jerk")
    for kind in kinds:
        coarse=simulate(kind,.01)
        fine=simulate(kind,.005)
        assert all(r["status"]=="Resolved" for r in coarse+fine)
        assert abs(coarse[-1]["d"]-.4)<1e-12
        for a,b in zip(coarse,fine[::2]):
            for key in ("d","e","R"):
                assert abs(a[key]-b[key])<1e-10, (kind,key,a,b)
    jerk=simulate("jerk_pause")
    assert jerk[10]["R"]==0 and jerk[35]["R"]>0
    # Record known defects as reproductions, not as desired gameplay.
    assert jerk[165]["state"]=="post_burst_pause"
    assert jerk[166]["state"]=="still"
    assert jerk[165]["R"]-jerk[166]["R"]>.15
    assert diagnostic_mean(simulate("repeated_jerk"))>diagnostic_mean(jerk)

if __name__=="__main__":
    checks()
    print("Trajectory, shared-time convergence and defect reproductions passed.")
    for capacity in (.45,1.0):
        for kind in ("steady","walk_stop","jerk_pause","repeated_jerk"):
            rows=simulate(kind,capacity=capacity)
            print(json.dumps(dict(V=capacity,kind=kind,
                displacement=rows[-1]["d"]-.2,
                diagnostic_mean=diagnostic_mean(rows),
                peak=max(r["R"] for r in rows),
                samples=[rows[i] for i in (10,35,50,125,150,165,166,200)])))
