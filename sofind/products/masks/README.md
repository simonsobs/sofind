# Transfer functions


## Allowed models
| `subproduct` |  `mask_type` |
| ----------- | -------- |
| lensing_masks.yaml |  `wide_v3_20220316`, `deep_v3` | 
| mnms_masks.yaml|  `None` (user knows name of mask `mask_fn`)|                                   


## Required Additional Keyword Arguments for `lensing_masks`
| `mask_type` | Additional Keywords | Possible Values |
| ----------- | ------------------- | --------------- |
| wide_v3_20220316| `skyfrac` | `GAL020`, `GAL040`,`GAL060`,`GAL070`,`GAL080` | 



## Code snippets


Get mask name: 
```
get_mask_fn(mask_fn, subproduct='mnms_masks')
```

Read-in mask:
```
read_mask(subproduct='lensing_masks', mask_type = 'wide_v3_20220316', skyfrac = 'GAL060')
```