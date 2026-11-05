#!/usr/bin/env python3
"""Synthetic time-budget hypothesis, not fish counts or production Response."""
import argparse
import json
import math
from pathlib import Path
import unittest


def valid(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0:
        raise ValueError("finite nonnegative rate required")
    return x


def rates(food, hook=0.2, encounter_gain=2.0, free_rate=0.5, handling=1.0):
    for x in (food, hook, encounter_gain, free_rate, handling):
        valid(x)
    if handling == 0:
        raise ValueError("positive handling rate required")
    return dict(a=0.1 + encounter_gain * food / (1 + food), d=0.5,
                f=free_rate * food, c=handling, h=hook, k=1.0)


def stationary(r):
    if r['a'] <= 0 or r['c'] <= 0 or r['k'] <= 0:
        raise ValueError("positive return rates required")
    e = 1 / (1 + r['d']/r['a'] + r['f']/r['c'] + r['h']/r['k'])
    return dict(search=r['d']/r['a']*e, engaged=e,
                free_handling=r['f']/r['c']*e, hook_handling=r['h']/r['k']*e,
                hook_attempt_rate=r['h']*e)


def advance(p, r, dt):
    valid(dt)
    for x in r.values():
        valid(x)
    # Uniformization sums a Poisson mixture of stochastic transition matrices.
    q = max(r['a'], r['d']+r['f']+r['h'], r['c'], r['k'])
    if q == 0 or dt == 0:
        return list(p)
    if q * dt > 10:
        n = math.ceil(q * dt / 10)
        for _ in range(n):
            p = advance(p, r, dt/n)
        return p
    def transition(x):
        s,e,f,h = x
        return [s*(1-r['a']/q)+e*r['d']/q,
                e*(1-(r['d']+r['f']+r['h'])/q)+s*r['a']/q+f*r['c']/q+h*r['k']/q,
                f*(1-r['c']/q)+e*r['f']/q,
                h*(1-r['k']/q)+e*r['h']/q]
    weight = math.exp(-q*dt)
    term = list(p)
    out = [weight*x for x in term]
    cumulative = weight
    for i in range(1, 250):
        term = transition(term)
        weight *= q*dt/i
        cumulative += weight
        out = [a+weight*b for a,b in zip(out,term)]
        if i > q*dt and 1-cumulative < 1e-14:
            break
    return out


def report():
    rows=[]
    for food in (0,0.1,0.5,1,2,5,10,30):
        rows.append(dict(food=food, **stationary(rates(food))))
    histories=[]
    p=[1,0,0,0]
    for t in range(61):
        food = 1 if t < 20 else 0
        if t:
            p=advance(p,rates(1 if t <= 20 else 0),1)
        if t in (0,1,5,10,20,21,30,60):
            histories.append(dict(time=t,food=food,states=p,hook_attempt_rate=p[1]*0.2))
    return dict(status='UNADMITTED_BEHAVIORAL_TIME_BUDGET_FIXTURE',
                rows=rows, removal_history=histories,
                no_food_engagement_gain=stationary(rates(1,encounter_gain=0)),
                no_free_handling=stationary(rates(30,free_rate=0)))


class Tests(unittest.TestCase):
    def test_positive_food_value_and_excess(self):
        f=lambda x: stationary(rates(x))['hook_attempt_rate']
        self.assertGreater(f(1),f(0))
        self.assertLess(f(30),f(1))
        self.assertLess(stationary(rates(1,encounter_gain=0))['hook_attempt_rate'],f(0))
        self.assertGreater(stationary(rates(30,free_rate=0))['hook_attempt_rate'],f(1))

    def test_stationary_and_conservation(self):
        for food in (0,0.1,1,30):
            r=rates(food); s=stationary(r)
            p=[s[k] for k in ('search','engaged','free_handling','hook_handling')]
            self.assertAlmostEqual(sum(p),1)
            after=advance(p,r,5)
            for a,b in zip(p,after): self.assertAlmostEqual(a,b,places=12)
            self.assertTrue(all(x>=0 for x in after))

    def test_semigroup_and_restore(self):
        r=rates(1); a=advance([1,0,0,0],r,20)
        p=[1,0,0,0]
        for _ in range(20): p=advance(p,r,1)
        for x,y in zip(a,p): self.assertAlmostEqual(x,y,places=12)
        saved=json.loads(json.dumps(p))
        self.assertEqual(advance(saved,r,2),advance(p,r,2))

    def test_zero_hook_not_rescued(self):
        self.assertEqual(stationary(rates(1,hook=0))['hook_attempt_rate'],0)

    def test_recovery_without_condition_write(self):
        p=advance([1,0,0,0],rates(1),20)
        p=advance(p,rates(0),100)
        s=stationary(rates(0))
        self.assertAlmostEqual(p[1],s['engaged'],places=8)
        for x in (-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): rates(x)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--report',type=Path); args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    if not result.wasSuccessful(): raise SystemExit(1)
    text=json.dumps(report(),ensure_ascii=False,indent=2)+'\n'
    if args.report: args.report.write_text(text)
    else: print(text)
