# Masks

## Allowed models
| `subproduct` |  `mask_type` |
| ----------- | -------- |
| lensing_masks.yaml | `dr6v4_20240919`  `None` (user knows name of mask `mask_fn`) | 
| mnms_masks.yaml|  `None` (user knows name of mask `mask_fn`)|                                   

## Required Additional Keyword Arguments for `lensing_masks`
| `mask_type` | Additional Keywords | Possible Values |
| ----------- | ------------------- | --------------- |
| dr6v4_20240919  | `daynight` | `night`,`daywide`,`daydeep` | 
|| `skyfrac` | `60`,`70`,`80` | 

## Code snippets


Get mask name: 
```
get_mask_fn(mask_fn, subproduct='mnms_masks')
```

Read-in mask:
```
read_mask(subproduct='lensing_masks', mask_type = 'dr6v4_20240919', skyfrac = 60)
```