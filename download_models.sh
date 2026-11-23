#!/usr/bin/env bash
# Grab the diarization models (sherpa-onnx releases) and the AMI test shards (HF mirror).
set -euo pipefail
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
mkdir -p models data/hf
cd models
for f in sherpa-onnx-pyannote-segmentation-3-0 sherpa-onnx-reverb-diarization-v1; do
  [ -d "$f" ] || { curl -fL -O "$R/speaker-segmentation-models/$f.tar.bz2" && tar xjf "$f.tar.bz2"; }
done
for f in wespeaker_en_voxceleb_resnet34_LM.onnx nemo_en_titanet_small.onnx; do
  [ -f "$f" ] || curl -fL -O "$R/speaker-recongition-models/$f"   # (sic) that's the real release tag
done
cd ../data/hf
H=https://huggingface.co/datasets/diarizers-community/ami/resolve/main
[ -f ami_ihm_test0.parquet ] || curl -fL -o ami_ihm_test0.parquet "$H/ihm/test-00000-of-00003.parquet"
[ -f ami_sdm_test0.parquet ] || curl -fL -o ami_sdm_test0.parquet "$H/sdm/test-00000-of-00003.parquet"
echo done
