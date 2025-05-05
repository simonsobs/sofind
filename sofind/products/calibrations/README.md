# Calibrations


## Calibrations & polarization efficiencies implemented
| Config File (`subproduct`) |  `qid`(s) |
| ----------- | --------| 
| act_dr6.02.yaml | `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`, gains and poleffs of published ACT maps
| dummy.yaml| all, gain and poleffs set to 1 |
| dr6v4_calday.yaml | `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`, calibrations for night that Sigurd used to create effective daytime beam
| dr6v4_cal_230523.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|         
| dr6v4_cal_240410.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|   
| dr6v4_poleff_231113.yaml| `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                        

## Code snippets


Read-in specific `qid` calibration for `subproduct`. Option to load either `cals` or `poleffs`, by default `cals`: 
```
read_calibration(qid, subproduct, which='cals')
```