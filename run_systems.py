"""Run a few open diarization pipelines (sherpa-onnx builds) on cropped AMI clips.
Usage: python run_systems.py  -> writes runs/<system>/<mode>/<file>.rttm + runs/timing.csv
"""
import sherpa_onnx as so, soundfile as sf, time, os, csv, sys

CROP = 600.0  # seconds; I only score the first 10 min of each meeting (see UEM)
M = 'models'
SEG = {'pyannote-seg3': f'{M}/sherpa-onnx-pyannote-segmentation-3-0/model.onnx',
       'reverb-v1':     f'{M}/sherpa-onnx-reverb-diarization-v1/model.onnx'}
EMB = {'wespeaker-r34': f'{M}/wespeaker_en_voxceleb_resnet34_LM.onnx',
       'titanet-s':     f'{M}/nemo_en_titanet_small.onnx',
       'eres2net-zh':   f'{M}/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx'}
SYSTEMS = {  # name -> (segmentation, embedding)
    'A_pyannoteSeg_wespeaker': ('pyannote-seg3', 'wespeaker-r34'),
    'B_reverb_wespeaker':      ('reverb-v1',     'wespeaker-r34'),
    'C_pyannoteSeg_titanet':   ('pyannote-seg3', 'titanet-s'),
}
FILES = sys.argv[1:] or ['IS1009a.ihm','IS1009a.sdm','TS3003a.ihm','TS3003a.sdm','EN2002b.ihm','EN2002b.sdm']

# Picked on held-out ES2004c (calibrate_threshold.py): titanet 0.9 (0.9-1.0 tie), wespeaker 0.8 (0.7-0.9 tie, took the middle)
TUNED = {'wespeaker-r34': 0.8, 'titanet-s': 0.9}

def make(seg, emb, n, th=0.5):
    cfg = so.OfflineSpeakerDiarizationConfig(
        segmentation=so.OfflineSpeakerSegmentationModelConfig(
            pyannote=so.OfflineSpeakerSegmentationPyannoteModelConfig(model=SEG[seg]), num_threads=4),
        embedding=so.SpeakerEmbeddingExtractorConfig(model=EMB[emb], num_threads=4),
        clustering=so.FastClusteringConfig(num_clusters=n, threshold=th),
        min_duration_on=0.3, min_duration_off=0.5)
    assert cfg.validate(), cfg
    return so.OfflineSpeakerDiarization(cfg)

if __name__ == '__main__':
    rows = []
    for f in FILES:
        x, sr = sf.read(f'data/audio/{f}.wav', dtype='float32')
        x = x[:int(CROP*sr)]
        for name, (seg, emb) in SYSTEMS.items():
            if os.environ.get('ONLY') and not name.startswith(tuple(os.environ['ONLY'].split(','))): continue
            modes = [('auto', -1, 0.5), ('oracleK', 4, 0.5)]
            if os.environ.get('TUNED_ONLY'): modes = [('autoTuned', -1, TUNED[emb])]
            for mode, n, th in modes:
                out = f'runs/{name}/{mode}'; os.makedirs(out, exist_ok=True)
                sd = make(seg, emb, n, th); t = time.time()
                res = sd.process(x).sort_by_start_time(); dt = time.time() - t
                uri = f.split('.')[0]
                with open(f'{out}/{f}.rttm', 'w') as fh:
                    for s in res:
                        fh.write(f'SPEAKER {uri} 1 {s.start:.3f} {s.end-s.start:.3f} <NA> <NA> spk{s.speaker} <NA> <NA>\n')
                rows.append([name, mode, f, round(dt,2), round(CROP/dt,1), len({s.speaker for s in res})])
                print(rows[-1], flush=True)
    with open('runs/timing.csv','a') as fh: csv.writer(fh).writerows(rows)
