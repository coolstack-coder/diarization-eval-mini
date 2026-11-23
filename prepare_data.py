import pyarrow.parquet as pq, io, soundfile as sf, sys, os
os.makedirs('data/audio',exist_ok=True); os.makedirs('data/ref_hf',exist_ok=True)
for cond in ['ihm','sdm']:
    t=pq.read_table(f'data/hf/ami_{cond}_test0.parquet').to_pylist()
    for r in t:
        path=r['audio']['path']; mid=path.split('.')[0].split('/')[-1][:7]
        x,sr=sf.read(io.BytesIO(r['audio']['bytes']))
        print(cond, path, mid, sr, round(len(x)/sr/60,1),'min', len(set(r['speakers'])),'spk')
        sf.write(f'data/audio/{mid}.{cond}.wav', x, sr, subtype='PCM_16')
        if cond=='ihm':
            with open(f'data/ref_hf/{mid}.rttm','w') as f:
                for s,e,spk in zip(r['timestamps_start'],r['timestamps_end'],r['speakers']):
                    f.write(f"SPEAKER {mid} 1 {s:.3f} {e-s:.3f} <NA> <NA> {spk} <NA> <NA>\n")
