
# Cluster Model

## Allowed Models
| `subproduct` |  `model_type` |
| ------------ | ------------- |
| dr6_nemo_cluster_model_snr5.yaml | `dr6v4` |

## Required Additional Keyword Arguments for `cluster_model`
| `model_type` | Additional Keywords | Possible Values |
| ------------ | ------------------- | --------------- |
| dr6v4        | `frequency`         | `090`, `150`|
|              | `SNR`               | Integer values (e.g., `5`, `10`) |
|              | `downgrade`         | Integer values (default `2`) |

## Code Snippets

Create instance of the datamodel
```
from sofind import DataModel 
dm = DataModel.from_config('act_dr6v4')
```

Read Cluster Model:
```
dm.read_cluster_model(subproduct='default', frequency = '090',downgrade=2)
```
