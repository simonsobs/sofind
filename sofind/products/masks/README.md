# Masks

## Allowed models
| `subproduct` |  `mask_type` |
| ----------- | -------- |
| lensing_masks_20250318 | `dr6v4_20250318`, or `None` (user knows name of mask `mask_fn`) |
| lensing_masks_20250513 | `dr6v4_20250513`, or `None` (user knows name of mask `mask_fn`) |
| lensing_masks_20250318_galactic | `planck_galactic`, or `None` (user knows name of mask `mask_fn`) |
| other lensing_masks_*, mnms_masks |  `None` (user knows name of mask `mask_fn`)|

The `lensing_masks_20250318_galactic` subproduct provides the full-sky Planck Galactic masks. These are identical to those distributed with the 20240919b release, so the same subproduct can be used with either set of lensing masks. They share the pixelization of the corresponding lensing masks but cover the full sky.

## Required Additional Keyword Arguments
| `mask_type` | Additional Keywords | Possible Values |
| ----------- | ------------------- | --------------- |
| dr6v4_20250318 | `daynight` | `night` |
|| `skyfrac` | `40`,`60`,`70`,... |
| dr6v4_20250513 | `daynight` | e.g. `daydeep` |
|| `skyfrac` | `40`,`60`,`70`,... |
| planck_galactic | `skyfrac` | `40`,`60`,`70`,... |

## Code snippets

Get mask name:
```
get_mask_fn(mask_fn, subproduct='mnms_masks')
```

Read in a lensing mask:
```
read_mask(subproduct='lensing_masks_20250318', mask_type='dr6v4_20250318', daynight='night', skyfrac=60)
```

Read in the matching full-sky Planck Galactic mask:
```
read_mask(subproduct='lensing_masks_20250318_galactic', mask_type='planck_galactic', skyfrac=40)
```
