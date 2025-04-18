# Calibrations


## Calibrations & polarization efficiencies implemented
| Config File (`subproduct`) |  `qid`(s) |
| ----------- | --------| 
| dr6v4_cal_230523.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|         
| dr6v4_cal_240410.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|   
| dr6v4_poleff_231113.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                        

## Code snippets


Read-in specific `qid` calibration for `subproduct`: 
```
read_calibration(qid, subproduct)
```