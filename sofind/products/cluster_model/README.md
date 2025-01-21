
# Cluster Model

## Allowed Models
| `subproduct` |  `model_type` |
| ------------ | ------------- |
| cluster_model.yaml | `dr6v4` |

## Required Additional Keyword Arguments for `cluster_model`
| `model_type` | Additional Keywords | Possible Values |
| ------------ | ------------------- | --------------- |
| dr6v4        | `frequency`         | `90`, `150`|
|              | `SNR`               | Integer values (e.g., `5`, `10`) |
|              | `downgrade`         | `down1`, `down2`, `down4` |

## Code Snippets

### Get Cluster Model Filename:
```python
get_cluster_model_fn(subproduct='default', frequency='150', SNR=5, downgrade='down2')
```

### Read Cluster Model:
```python
read_cluster_model(subproduct='default', frequency='150', SNR=5, downgrade='down2')
```
