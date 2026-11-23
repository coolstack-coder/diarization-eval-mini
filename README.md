# diarization-eval-mini

This is the small pilot for my Voice Arena take-home (Q1: design a speaker diarization eval). I wanted to check my scoring choices on real audio instead of only arguing for them, so this repo runs three open diarization pipelines on three public AMI meetings and scores them several ways.

## What's here

| File | What it does |
|---|---|
| `prepare_data.py` | Pulls audio and word-aligned references for the AMI test meetings from the HF mirror `diarizers-community/ami`, both the `ihm` (headset mix) and `sdm` (single far-field mic) subsets. The official AMI mirror was returning 503 when I tried it. |
| `run_systems.py` | Runs each system on the first 10 minutes of each file in two modes: blind (default threshold) and with the speaker count (4) given. `TUNED_ONLY=1` runs blind mode with the dev-tuned thresholds instead. Writes RTTMs to `runs/`. |
| `calibrate_threshold.py` | Sweeps the clustering threshold for each embedding model (WeSpeaker, TitaNet) on a held-out meeting (ES2004c, not in the test files). |
| `score.py` | pyannote.metrics DER/JER under three settings: strict, 0.25 s collar, and collar plus skip-overlap. |
| `analyze.py` | Summary tables, plus a paired bootstrap at both the 1-minute-chunk level and the recording level. |
| `plots.py` | Figures for the report. |

## Systems

All three are built with sherpa-onnx 2.0.3 on CPU (Apple M-series, 4 threads), with clustering threshold 0.5, `min_duration_on=0.3` and `min_duration_off=0.5`.

- **A**: `pyannote/segmentation-3.0` (ONNX export) + WeSpeaker ResNet34-LM (VoxCeleb). This is basically the pyannote 3.x recipe.
- **B**: Rev `reverb-diarization-v1` segmentation + WeSpeaker ResNet34-LM.
- **C**: `pyannote/segmentation-3.0` + NVIDIA TitaNet-small.

## Data

- AMI test meetings IS1009a, TS3003a and EN2002b. Only the first 600 s of each is scored, with a UEM of [0, 600].
- References are the word-aligned "only_words" RTTMs. I checked that they are identical to `pyannote/AMI-diarization-setup` for IS1009a and TS3003a (DER 0.0 between the two).

## Reproduce

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install sherpa-onnx pyannote.metrics soundfile numpy scipy pandas matplotlib pyarrow
# download models (see run_systems.py for names) into models/, AMI parquet shards into data/hf/
python prepare_data.py
python run_systems.py
python calibrate_threshold.py
TUNED_ONLY=1 python run_systems.py
python score.py && python analyze.py && python plots.py
```

## Notes to self

- pyannote.metrics `collar` is the **total** width, while dscore's `--collar` is **per side**. So "0.25 s collar" in most papers means `collar=0.5` here.
- Only 3 meetings, 30 min of audio per mic condition. This shows the method works; it doesn't rank these models.

## Results (strict DER %, first 10 min of 3 AMI test meetings)

| System | IHM default | IHM dev-tuned | IHM k=4 | SDM default | SDM dev-tuned | SDM k=4 | RTF (CPU) |
|---|---|---|---|---|---|---|---|
| A pyannote-seg + WeSpeaker | 58.3 | 42.4 | 30.5 | 60.5 | 41.4 | 54.5 | 0.12 |
| B Reverb-v1 + WeSpeaker | 74.6 | 58.8 | 56.0 | 81.3 | 66.4 | 79.4 | 0.16 |
| C pyannote-seg + TitaNet | 61.3 | 25.9 | 27.8 | 82.9 | 34.5 | 34.9 | 0.06 |

All tables, including per-file scores and the bootstrap, are in `results/tables.md`. The figures are in `results/`. Per-run outputs are in `runs/<system>/<mode>/*.rttm`.

The main takeaways are written up in my report. In short:
- The default clustering threshold over-counts speakers badly (up to 59 guessed for a 4-person meeting), and the default-vs-tuned choice flips the A/C ranking.
- Lumping everyone into one speaker scored 15% DER (but 78% JER) on a clip where one person talks 96.6% of the time.
- A 0.25 s collar removes 22% of the scored speech, and collar plus skip-overlap removes 41%.
