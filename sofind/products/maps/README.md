# maps
We give additional information for each `maps` config file, such as permissible `qid`(s) and additional keyword arguments, required for using `maps` methods.

## Permissible `qid`(s)
| Config File | `qid`(s) |
| ----------- | -------- |
| act_dr6.01.yaml| `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd`, `pa7a`, `pa7a_dw`, `pa7b`, `pa7b_dw` |
| act_dr6v3.yaml| `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd`, `pa7a`, `pa7a_dw`, `pa7b`, `pa7b_dw` |
| act_dr6v3_pwv_split.yaml | `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd` |
| so_scan_s0003.yaml | `lfa`, `lfb`, `mfa`, `mfb`, `uhfa`, `uhfb` |
| so_sat_v1_f1.yaml | `lfa`, `lfb`, `mfa`, `mfb`, `uhfa`, `uhfb` |
| act_dr6v4.yaml | `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd` |
| act_dr6v4_pwv_split.yaml | `pa4a`, `pa4b`, `pa5a`,`pa5b`, `pa6a`,  `pa6b` |
| act_dr6v4_inout_split.yaml | `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd` |
| act_dr6v4_el_split.yaml | `pa4a`, `pa4b`, `pa5a`,`pa5b`, `pa6a`,  `pa6b` |
| act_nemov3.yaml | `nemo_090`, `nemo_150` |

## Required Additional Keyword Arguments
| Config File | Additional Keywords | Possible Values |
| ----------- | ------------------- | --------------- |
| act_dr6.01.yaml| | |
| act_dr6v3.yaml| | |
| act_dr6v3_pwv_split.yaml | `null_split` | `low_pwv`, `high_pwv` |
| so_scan_s0003.yaml | |
| so_sat_v1_f1.yaml | |
| act_dr6v4.yaml| | |
| act_dr6v4_pwv_split.yaml | `pwv_split` | `pwv1`, `pwv2` |
| act_dr6v4_inout_split.yaml | `inout_split` | `inout1`, `inout2` |
| act_dr6v4_el_split.yaml | `el_split` | `el1`, `el2`, `el3` |
| act_nemov3.yaml| | |