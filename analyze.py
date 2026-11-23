"""Tables + bootstrap for the mini eval. Reads runs/, writes results/*.md, results/*.png"""
import glob, json, os, random
import numpy as np
from collections import defaultdict
from score import load, score_file, SETTINGS, CROP, REF_DIR

random.seed(7); np.random.seed(7)
rows = json.load(open('results/scores.json'))
S0 = 'strict (no collar, overlap scored)'

def pooled(rs, key=S0):
    err = sum(r[key]['der']*r[key]['total'] for r in rs); tot = sum(r[key]['total'] for r in rs)
    return err/tot

lines = []
# 1) main table: pooled DER per system x mode x condition, three settings
by = defaultdict(list)
for r in rows: by[(r['system'], r['mode'], r['cond'])].append(r)
lines.append('| System | #spk given? | Mic | Strict DER | +0.25s collar | +collar, skip overlap | Miss | FA | Confusion | JER |')
lines.append('|---|---|---|---|---|---|---|---|---|---|')
for (s, m, c), rs in sorted(by.items()):
    tot = sum(r[S0]['total'] for r in rs)
    comp = {k: sum(r[S0][k]*r[S0]['total'] for r in rs)/tot for k in ['miss','fa','conf']}
    jer = np.mean([r['jer'] for r in rs])
    lines.append(f"| {s} | { {'oracleK':'yes (4)','auto':'no, default threshold','autoTuned':'no, dev-tuned threshold'}[m] } | {c.upper()} | {pooled(rs)*100:.1f} | {pooled(rs, list(SETTINGS)[1])*100:.1f} | {pooled(rs, list(SETTINGS)[2])*100:.1f} | {comp['miss']*100:.1f} | {comp['fa']*100:.1f} | {comp['conf']*100:.1f} | {jer*100:.1f} |")
lines.append('')
lines.append('Per-file strict DER and estimated speaker count (auto mode):')
lines.append('| System | Mode | File | Strict DER | spk ref | spk hyp |'); lines.append('|---|---|---|---|---|---|')
for r in sorted(rows, key=lambda r:(r['system'],r['meeting'],r['cond'])):
    if r['mode'] in ('auto','autoTuned'):
        lines.append(f"| {r['system']} | {r['mode']} | {r['meeting']}.{r['cond']} | {r[S0]['der']*100:.1f} | {r['spk_ref']} | {r['spk_hyp']} |")

# 2) paired bootstrap over 1-minute chunks, oracleK, A vs B per condition
refs = {os.path.basename(p)[:-5]: load(p) for p in glob.glob(f'{REF_DIR}/*.rttm')}
def chunks(system, mode, cond):
    out = []
    for p in sorted(glob.glob(f'runs/{system}/{mode}/*.{cond}.rttm')):
        meet = os.path.basename(p).split('.')[0]; hyp = load(p)
        for k in range(int(CROP//60)):
            c = score_file(refs[meet], hyp, start=60*k, end=60*(k+1))
            out.append((c['missed detection']+c['false alarm']+c['confusion'], c['total'], ['IS1009a','TS3003a','EN2002b'].index(meet)))
    return np.array(out)
lines.append('\nPaired bootstrap (1-min chunks, 10k resamples, oracle speaker count, strict setting):')
lines.append('| Comparison | Mic | DER diff (pp) | 95% CI, 1-min chunks | 95% CI, whole recordings | P(first better), chunks |'); lines.append('|---|---|---|---|---|---|')
pairs = [('A_pyannoteSeg_wespeaker','B_reverb_wespeaker'), ('A_pyannoteSeg_wespeaker','C_pyannoteSeg_titanet')]
for a, b in pairs:
    for cond in ['ihm','sdm']:
        A, B = chunks(a,'oracleK',cond), chunks(b,'oracleK',cond); n = len(A)
        idx = np.random.randint(0, n, (10000, n))
        da = A[idx,0].sum(1)/A[idx,1].sum(1); db = B[idx,0].sum(1)/B[idx,1].sum(1)
        d = (da-db)*100; point = (A[:,0].sum()/A[:,1].sum() - B[:,0].sum()/B[:,1].sum())*100
        lo, hi = np.percentile(d,[2.5,97.5])
        # recording-level: resample meetings (only 3 here, so this is mostly a demonstration)
        ra = np.array([[A[A[:,2]==m,0].sum(), A[A[:,2]==m,1].sum()] for m in range(3)]); rb = np.array([[B[B[:,2]==m,0].sum(), B[B[:,2]==m,1].sum()] for m in range(3)])
        ridx = np.random.randint(0, 3, (10000, 3))
        rd = (ra[ridx,0].sum(1)/ra[ridx,1].sum(1) - rb[ridx,0].sum(1)/rb[ridx,1].sum(1))*100
        rlo, rhi = np.percentile(rd,[2.5,97.5])
        lines.append(f"| {a.split('_')[0]} vs {b.split('_')[0]} | {cond.upper()} | {point:+.1f} | [{lo:+.1f}, {hi:+.1f}] | [{rlo:+.1f}, {rhi:+.1f}] | {(d<0).mean():.2f} |")
open('results/tables.md','w').write('\n'.join(lines)); print('\n'.join(lines))
