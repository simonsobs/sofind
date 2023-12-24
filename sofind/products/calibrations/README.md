# Calibrations


## Calibrations implemented
| Config File (`subproduct`) | calibration_type (`key`)    | `qid`(s) |
| ----------- | --------| -------- |
| dr6v3_cal_baseline.yaml |  `poleff` | `pa4a`, `pa5a`, `pa5b`, `pa6a`, `pa6b` | 
| dr6v4_cal_230523.yaml| `cal` | `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                                   

## Code snippets


Read-in calibrations: 
```
read_calibration(qid, subproduct='default', key = None)
```