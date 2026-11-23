import json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from collections import defaultdict
rows = json.load(open('results/scores.json'))
SET = ['strict (no collar, overlap scored)','forgiving (0.25s/side, overlap scored)','legacy (0.25s/side, overlap skipped)']
NAMES = {'A_pyannoteSeg_wespeaker':'A: pyannote-seg + WeSpeaker','B_reverb_wespeaker':'B: Reverb-v1 + WeSpeaker',
         'C_pyannoteSeg_titanet':'C: pyannote-seg + TitaNet','Cc_pyannoteSeg_titanet_tuned':'C*: C, threshold tuned on dev'}
def pooled(rs, key, comp=None):
    tot = sum(r[key]['total'] for r in rs)
    return sum(r[key][comp or 'der']*r[key]['total'] for r in rs)/tot*100
g = defaultdict(list)
for r in rows: g[(r['system'], r['mode'], r['cond'])].append(r)
systems = [s for s in NAMES if any(k[0]==s for k in g)]
plt.rcParams.update({'font.family':'Helvetica','font.size':9})
# Fig 1: error breakdown, oracleK vs auto, IHM vs SDM (strict)
fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.2), sharey=True)
cols = {'miss':'#c9822b','fa':'#7f8fa6','conf':'#b4473a'}
for ax, cond in zip(axes, ['ihm','sdm']):
    labels, x = [], 0
    for s in systems:
        for mode in ['auto','autoTuned','oracleK']:
            rs = g.get((s, mode, cond));
            if not rs: continue
            bottom = 0
            for c in ['miss','fa','conf']:
                v = pooled(rs, SET[0], c); ax.bar(x, v, bottom=bottom, color=cols[c], width=0.75); bottom += v
            ax.text(x, bottom+1, f'{bottom:.0f}', ha='center', fontsize=8)
            labels.append(f"{s.split('_')[0]}\n{ {'auto':'default','autoTuned':'tuned','oracleK':'k=4'}[mode] }"); x += 1
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_title({'ihm':'Close-talk mix (IHM)','sdm':'Single far-field mic (SDM)'}[cond], fontsize=10)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Strict DER (%)')
from matplotlib.patches import Patch
fig.legend([Patch(color=v) for v in cols.values()], ['Missed speech','False alarm','Speaker confusion'], loc='upper center', ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.04))
fig.tight_layout(); fig.savefig('results/fig_breakdown.png', dpi=200, bbox_inches='tight')
# Fig 2: same outputs, three scoring settings
fig, ax = plt.subplots(figsize=(9, 2.8))
w = 0.26; xs = np.arange(len(systems)*2)
for i, st in enumerate(SET):
    vals = [pooled(g[(s,'oracleK',c)], st) for s in systems for c in ['ihm','sdm']]
    ax.bar(xs + (i-1)*w, vals, w, label=['Strict (my choice)','0.25 s collar','0.25 s collar + skip overlap'][i], color=['#2f5d8a','#8eaccc','#d6e0ec'][i])
    for xx, v in zip(xs + (i-1)*w, vals): ax.text(xx, v+0.6, f'{v:.0f}', ha='center', fontsize=7)
ax.set_xticks(xs); ax.set_xticklabels([f"{s.split('_')[0]} · {c.upper()}" for s in systems for c in ['ihm','sdm']], fontsize=8)
ax.set_ylabel('DER (%)'); ax.legend(frameon=False, fontsize=8, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.13)); ax.spines[['top','right']].set_visible(False)
ax.set_title('Same system outputs, three scoring settings (speaker count given)', fontsize=10); ax.set_ylim(0, 92)
fig.tight_layout(); fig.savefig('results/fig_settings.png', dpi=200, bbox_inches='tight')
print('figs ok')
