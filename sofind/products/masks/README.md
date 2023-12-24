# Transfer functions


## Allowed models
| `subproduct` |  `mask_type` |
| ----------- | -------- |
| lensing_masks.yaml |  `wide_v3_20220316`, `wide_v4_20220316`, `deep_v4`, `deep_v4` | 
| mnms_masks.yaml|  `None` (user knows name of mask `mask_fn`)|                                   


## Code snippets


Get mask name: 
```
get_mask_fn(mask_fn, subproduct='default', mask_type = None)
```

Read-in mask:
```
read_mask(mask_fn, subproduct='default', mask_type = None)
```