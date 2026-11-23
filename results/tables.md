| System | #spk given? | Mic | Strict DER | +0.25s collar | +collar, skip overlap | Miss | FA | Confusion | JER |
|---|---|---|---|---|---|---|---|---|---|
| A_pyannoteSeg_wespeaker | no, default threshold | IHM | 58.3 | 52.0 | 43.4 | 11.7 | 4.4 | 42.2 | 65.3 |
| A_pyannoteSeg_wespeaker | no, default threshold | SDM | 60.5 | 56.9 | 55.9 | 13.6 | 5.2 | 41.8 | 73.2 |
| A_pyannoteSeg_wespeaker | no, dev-tuned threshold | IHM | 42.4 | 36.5 | 28.8 | 13.7 | 3.6 | 25.1 | 69.3 |
| A_pyannoteSeg_wespeaker | no, dev-tuned threshold | SDM | 41.4 | 35.5 | 31.0 | 15.9 | 4.0 | 21.6 | 75.5 |
| A_pyannoteSeg_wespeaker | yes (4) | IHM | 30.5 | 24.6 | 19.1 | 11.6 | 4.2 | 14.6 | 53.9 |
| A_pyannoteSeg_wespeaker | yes (4) | SDM | 54.5 | 51.5 | 52.9 | 13.6 | 5.1 | 35.9 | 71.0 |
| B_reverb_wespeaker | no, default threshold | IHM | 74.6 | 71.0 | 65.9 | 19.1 | 22.4 | 33.2 | 67.7 |
| B_reverb_wespeaker | no, default threshold | SDM | 81.3 | 81.0 | 83.3 | 19.8 | 23.6 | 37.9 | 77.8 |
| B_reverb_wespeaker | no, dev-tuned threshold | IHM | 58.8 | 55.5 | 49.3 | 19.7 | 22.1 | 17.0 | 71.5 |
| B_reverb_wespeaker | no, dev-tuned threshold | SDM | 66.4 | 65.1 | 63.6 | 19.8 | 23.1 | 23.5 | 81.0 |
| B_reverb_wespeaker | yes (4) | IHM | 56.0 | 53.1 | 48.7 | 19.2 | 22.2 | 14.7 | 63.3 |
| B_reverb_wespeaker | yes (4) | SDM | 79.4 | 80.1 | 83.3 | 19.7 | 23.5 | 36.2 | 78.8 |
| C_pyannoteSeg_titanet | no, default threshold | IHM | 61.3 | 54.5 | 46.7 | 11.6 | 4.4 | 45.3 | 69.2 |
| C_pyannoteSeg_titanet | no, default threshold | SDM | 82.9 | 77.9 | 73.0 | 13.7 | 5.2 | 64.1 | 77.7 |
| C_pyannoteSeg_titanet | no, dev-tuned threshold | IHM | 25.9 | 19.4 | 12.1 | 11.6 | 4.2 | 10.1 | 51.1 |
| C_pyannoteSeg_titanet | no, dev-tuned threshold | SDM | 34.5 | 28.1 | 22.8 | 13.6 | 5.1 | 15.8 | 56.9 |
| C_pyannoteSeg_titanet | yes (4) | IHM | 27.8 | 21.8 | 16.1 | 11.7 | 4.2 | 12.0 | 51.4 |
| C_pyannoteSeg_titanet | yes (4) | SDM | 34.9 | 29.3 | 24.0 | 13.5 | 5.2 | 16.2 | 60.6 |

Per-file strict DER and estimated speaker count (auto mode):
| System | Mode | File | Strict DER | spk ref | spk hyp |
|---|---|---|---|---|---|
| A_pyannoteSeg_wespeaker | auto | EN2002b.ihm | 78.1 | 4 | 40 |
| A_pyannoteSeg_wespeaker | autoTuned | EN2002b.ihm | 50.6 | 4 | 8 |
| A_pyannoteSeg_wespeaker | auto | EN2002b.sdm | 69.3 | 4 | 13 |
| A_pyannoteSeg_wespeaker | autoTuned | EN2002b.sdm | 54.7 | 4 | 4 |
| A_pyannoteSeg_wespeaker | auto | IS1009a.ihm | 45.7 | 4 | 6 |
| A_pyannoteSeg_wespeaker | autoTuned | IS1009a.ihm | 50.1 | 4 | 1 |
| A_pyannoteSeg_wespeaker | auto | IS1009a.sdm | 55.8 | 4 | 4 |
| A_pyannoteSeg_wespeaker | autoTuned | IS1009a.sdm | 50.4 | 4 | 1 |
| A_pyannoteSeg_wespeaker | auto | TS3003a.ihm | 43.6 | 4 | 14 |
| A_pyannoteSeg_wespeaker | autoTuned | TS3003a.ihm | 23.9 | 4 | 4 |
| A_pyannoteSeg_wespeaker | auto | TS3003a.sdm | 53.1 | 4 | 4 |
| A_pyannoteSeg_wespeaker | autoTuned | TS3003a.sdm | 15.0 | 4 | 1 |
| B_reverb_wespeaker | auto | EN2002b.ihm | 91.7 | 4 | 37 |
| B_reverb_wespeaker | autoTuned | EN2002b.ihm | 69.4 | 4 | 9 |
| B_reverb_wespeaker | auto | EN2002b.sdm | 85.6 | 4 | 11 |
| B_reverb_wespeaker | autoTuned | EN2002b.sdm | 79.8 | 4 | 3 |
| B_reverb_wespeaker | auto | IS1009a.ihm | 78.7 | 4 | 7 |
| B_reverb_wespeaker | autoTuned | IS1009a.ihm | 78.1 | 4 | 2 |
| B_reverb_wespeaker | auto | IS1009a.sdm | 84.9 | 4 | 4 |
| B_reverb_wespeaker | autoTuned | IS1009a.sdm | 89.6 | 4 | 2 |
| B_reverb_wespeaker | auto | TS3003a.ihm | 47.9 | 4 | 11 |
| B_reverb_wespeaker | autoTuned | TS3003a.ihm | 26.2 | 4 | 3 |
| B_reverb_wespeaker | auto | TS3003a.sdm | 72.1 | 4 | 3 |
| B_reverb_wespeaker | autoTuned | TS3003a.sdm | 26.6 | 4 | 2 |
| C_pyannoteSeg_titanet | auto | EN2002b.ihm | 72.7 | 4 | 44 |
| C_pyannoteSeg_titanet | autoTuned | EN2002b.ihm | 33.4 | 4 | 6 |
| C_pyannoteSeg_titanet | auto | EN2002b.sdm | 90.6 | 4 | 59 |
| C_pyannoteSeg_titanet | autoTuned | EN2002b.sdm | 37.8 | 4 | 7 |
| C_pyannoteSeg_titanet | auto | IS1009a.ihm | 70.2 | 4 | 32 |
| C_pyannoteSeg_titanet | autoTuned | IS1009a.ihm | 30.8 | 4 | 5 |
| C_pyannoteSeg_titanet | auto | IS1009a.sdm | 82.1 | 4 | 44 |
| C_pyannoteSeg_titanet | autoTuned | IS1009a.sdm | 39.6 | 4 | 8 |
| C_pyannoteSeg_titanet | auto | TS3003a.ihm | 37.4 | 4 | 11 |
| C_pyannoteSeg_titanet | autoTuned | TS3003a.ihm | 11.0 | 4 | 2 |
| C_pyannoteSeg_titanet | auto | TS3003a.sdm | 73.5 | 4 | 30 |
| C_pyannoteSeg_titanet | autoTuned | TS3003a.sdm | 25.3 | 4 | 4 |

Paired bootstrap (1-min chunks, 10k resamples, oracle speaker count, strict setting):
| Comparison | Mic | DER diff (pp) | 95% CI, 1-min chunks | 95% CI, whole recordings | P(first better), chunks |
|---|---|---|---|---|---|
| A vs B | IHM | -24.6 | [-36.8, -16.2] | [-31.8, -14.7] | 1.00 |
| A vs B | SDM | -22.3 | [-35.5, -12.4] | [-35.4, -5.1] | 1.00 |
| A vs C | IHM | +1.3 | [-0.0, +2.6] | [+0.4, +1.8] | 0.03 |
| A vs C | SDM | +11.7 | [+6.4, +17.3] | [+6.6, +19.9] | 0.00 |