# Beams

## Permissible `qid`(s)
| Config File (`subproduct`) | `qid`(s) |
| ----------- | -------- |
| beams_nemo.yaml|  __coadd__: `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd` |
| beams_v3_20220817.yaml|  __coadd__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __splits__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|
| beams_v4_20230130.yaml |    __coadd__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __splits__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>    |
| beams_v4_20230130_snfit.yaml|   __coadd__: `pa4a`, `pa4a_dw`, `pa4a_dd`, `pa4b`, `pa4b_dw`, `pa4b_dd`, `pa5a`, `pa5a_dw`, `pa5a_dd`, `pa5b`, `pa5b_dw`, `pa5b_dd`, `pa6a`, `pa6a_dw`, `pa6a_dd`, `pa6b`, `pa6b_dw`, `pa6b_dd`|     
| beams_v4_20230902.yaml |    __coadd__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>   __splits__: `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` <br>    |



## Code snippets


Get name of beam file per-split:
```
get_beam_fn(subproduct, qid, split_num=0, coadd=False)
```

Read-in coadd beam: 
```
read_beam(subproduct, qid, coadd=True)
```