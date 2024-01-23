# Calibrations


## Calibrations implemented
| Config File (`subproduct`) | calibration_type (`key`)    | `qid`(s) |
| ----------- | --------| -------- |
| dr6v3_cal_baseline.yaml |  `poleff` | `pa4a`, `pa5a`, `pa5b`, `pa6a`, `pa6b` | 
| dr6v4_cal_230523.yaml| `cal` | `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|         
| dr6v4_cal_231113.yaml| `cal` `poleff` | `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                             

## Code snippets


Read-in all calibrations for subproduct: 
```
read_calibration(qid, subproduct)
```

Read-in specific calibration for subproduct: 
```
read_calibration(qid, subproduct, key)
```