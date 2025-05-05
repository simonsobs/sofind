# Transfer functions


## Allowed models
| Config File (`subproduct`) |  `qid`(s) |
| ----------- | -------- |
| tf_dummy.yaml |  all | 
| tf_dr6v3_220701.yaml |  `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b` | 
| tf_dr6v4_230523.yaml|  `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|       
| tf_dr6v4_240416.yaml|  `pa4a`, `pa4b`, `pa5a`, `pa5b`, `pa6a`, `pa6b`|                                

## Code snippets


Get transfer function name: 
```
get_tf_fn(qid, subproduct='default')
```

Read-in transfer function:
```
read_tf(qid, subproduct='default')
```