"""Score runs/ against AMI references with pyannote.metrics.
Note: pyannote's `collar` is the TOTAL width removed around each boundary,
dscore's --collar is per side. So dscore 0.25 == pyannote collar=0.5. Took me a while to notice.
"""
import glob, os, json, random, sys
import numpy as np
from pyannote.core import Annotation, Segment, Timeline
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate

CROP = 600.0
REF_DIR = 'data/ref_hf'

def load(path, uri=None):
    ann = Annotation(uri=uri)
    for i, line in enumerate(open(path)):
        p = line.split()
        s, d = float(p[3]), float(p[4])
        if d > 0: ann[Segment(s, s + d), i] = p[7]
    return ann

SETTINGS = {  # name -> (pyannote collar total width, skip_overlap)
    'strict (no collar, overlap scored)': (0.0, False),
    'forgiving (0.25s/side, overlap scored)': (0.5, False),
    'legacy (0.25s/side, overlap skipped)': (0.5, True),
}

def score_file(ref, hyp, start=0.0, end=CROP, collar=0.0, skip=False):
    uem = Timeline([Segment(start, end)])
    der = DiarizationErrorRate(collar=collar, skip_overlap=skip)
    comp = der(ref, hyp, uem=uem, detailed=True)
    return comp

def main():
    out = []
    refs = {os.path.basename(p)[:-5]: load(p, os.path.basename(p)[:-5]) for p in glob.glob(f'{REF_DIR}/*.rttm')}
    for hyp_path in sorted(glob.glob('runs/*/*/*.rttm')):
        _, system, mode, fn = hyp_path.split('/')
        meeting, cond = fn.split('.')[:2]
        ref, hyp = refs[meeting], load(hyp_path, meeting)
        row = dict(system=system, mode=mode, meeting=meeting, cond=cond)
        for sname, (collar, skip) in SETTINGS.items():
            c = score_file(ref, hyp, collar=collar, skip=skip)
            row[sname] = dict(der=c['diarization error rate'], miss=c['missed detection']/c['total'],
                              fa=c['false alarm']/c['total'], conf=c['confusion']/c['total'], total=c['total'])
        jer = JaccardErrorRate()(ref, hyp, uem=Timeline([Segment(0, CROP)]))
        row['jer'] = jer
        ref_spk = len(ref.crop(Segment(0, CROP)).labels()); hyp_spk = len(hyp.labels())
        row['spk_ref'], row['spk_hyp'] = ref_spk, hyp_spk
        out.append(row)
    json.dump(out, open('results/scores.json', 'w'), indent=1)
    print(f'scored {len(out)} runs')

if __name__ == '__main__':
    os.makedirs('results', exist_ok=True); main()
