# Catalogs


## Allowed models
| Config File (`subproduct`) | 
| ----------- | 
| inpaint_catalogs.yaml |  

| Name structures of catalogs (`cat_fn`) |  Catalog dates(`cat_date`) |
| ----------- | -------- |
| f'large_cluster_catalog_{cat_date}.csv' |  `20220316`, `20241002` | 
| f'regular_cluster_catalog_{cat_date}.csv' |  `20220316`, `20241002` | 
| f'union_catalog_large_{cat_date}.csv' |  `20220316`, `20241002` | 
| f'union_catalog_regular_{cat_date}.csv' |  `20220316`, `20241002` | 
                                

## Code snippets


Get full path to catalog product: 
```
get_catalog_fn(cat_fn='large_cluster_catalog_20220316.csv', subproduct='inpaint_catalogs')
```

Read catalog from disk:
```
read_catalog(cat_fn='large_cluster_catalog_20220316.csv', subproduct='inpaint_catalogs')
```

Note: `read_catalog()` expects RA, DEC columns (degrees), and returns DEC, RA rows (radians).