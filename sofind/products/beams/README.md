# Beams

## Permissible `qid`(s)
| Config File (`subproduct`) | beam_name    | `qid`(s) |
| ----------- | --------| -------- |
| beams_nemo.yaml|  `beams_nemo` | __coadd__: `n150`, `n090` |
| beams_v3_20220817.yaml| `beams_v3_20220817` | __coadd__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __splits__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                                   
| beams_v4_20230130.yaml | `beams_v4_20230130` <br> <br> `beams_v4_20230130_snfit` <br> <br> |  __coadd__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __splits__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __coadd__: `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd`  |


## Code snippets


Get name of beam file:
```
get_beam_fn(qid, beam_name = None, split_num=0, coadd=False,  subproduct='default')
```

Read-in beam: 
```
read_beam(qid, beam_name = None, split_num=0, coadd=False, subproduct='default')
```