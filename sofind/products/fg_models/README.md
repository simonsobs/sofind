# Foreground models

Covariance cubes for generating Gaussian simulations of astrophysical foregrounds in temperature. The product should contain foreground-only cross-spectra C_ell (uK^2, beam-free) between every pair of qids. These may have been, for example, fit to the ACT and Planck auto and cross spectra inside the a mask for a given sky fraction.

## Allowed models
| `subproduct` | Fitted qids | Analysis mask |
| ----------- | ----------- | ------------- |
| fg_models_20261008 | `p03` to `p08`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` | `lensing_masks_20261008` night masks |

## Required Additional Keyword Arguments
| Keyword | Possible Values |
| ------- | --------------- |
| `fsky` | sky fraction tag of the analysis mask, e.g. `70` |

## File format

Each file is an npz written by `solenspipe.preprocessing.save_cross_spectra`. It holds one spectrum per unordered qid pair under the key `spec:{qid1}|{qid2}` (with `qid1 <= qid2`), on ell = 0, 1, 2, ... with ell < 2 set to zero, together with the stored qids (`meta:qids`) and the pair separator (`meta:sep`).

## Code snippets

Get the file name:
```
get_fg_model_fn(subproduct='fg_models_20261008', fsky=70)
```

Read the covariance cube, of shape (nqid, nqid, nell), for some qids:
```
read_fg_model(qids=['p05', 'pa5a', 'pa6a'], subproduct='fg_models_20261008', fsky=70)
```

Qids without their own model can take the spectra of another qid through `qid_aliases`, e.g. daytime qids with the model of the night qid of the same array and frequency:
```
read_fg_model(qids=['p05', 'pa5a', 'pa5a_dd'], subproduct='fg_models_20261008',
              qid_aliases={'pa5a_dd': 'pa5a'}, fsky=70)
```

Be aware that this aliasing gives you a singular covariance matrix, so one should be careful (as `pixell.curvedsky.rand_alm` is) to trim out negative eigenvalues. This will lead to near-perfect correlation of aliased qids with their aliases.