"""System C (TitaNet) produced 32 speakers at the default threshold, so the default
clustering threshold clearly doesn't transfer across embedding models.
Fair fix: tune the threshold on a HELD-OUT meeting (ES2004c, first 10 min, not in my test files), then freeze it.
"""
import sherpa_onnx as so, soundfile as sf, sys
from run_systems import SEG, EMB, CROP
sys.argv=[sys.argv[0]]
from score import load, score_file
x, sr = sf.read('data/audio/ES2004c.ihm.wav', dtype='float32'); x = x[:int(CROP*sr)]
ref = load('data/ref_hf/ES2004c.rttm')
GRID = {'titanet-s': [0.6, 0.7, 0.8, 0.9, 1.0, 1.1], 'wespeaker-r34': [0.6, 0.7, 0.8, 0.9, 1.0]}
for emb, ths in GRID.items():
  for th in ths:
      cfg = so.OfflineSpeakerDiarizationConfig(
          segmentation=so.OfflineSpeakerSegmentationModelConfig(pyannote=so.OfflineSpeakerSegmentationPyannoteModelConfig(model=SEG['pyannote-seg3']), num_threads=4),
          embedding=so.SpeakerEmbeddingExtractorConfig(model=EMB[emb], num_threads=4),
          clustering=so.FastClusteringConfig(num_clusters=-1, threshold=th), min_duration_on=0.3, min_duration_off=0.5)
      res = so.OfflineSpeakerDiarization(cfg).process(x).sort_by_start_time()
      from pyannote.core import Annotation, Segment
      hyp = Annotation()
      for i, s in enumerate(res): hyp[Segment(s.start, s.end), i] = f'spk{s.speaker}'
      c = score_file(ref, hyp)
      print(f'{emb} threshold={th} speakers={len(hyp.labels())} DER={100*c["diarization error rate"]:.1f}', flush=True)
