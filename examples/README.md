# Examples

- `process_purchases.py`

This assumes that the [docker hadoop cluster](https://github.com/usersina/docker-hadoop) is running and that a file named `purchases.txt` is already added to the root of the HDFS.

```bash
root@hadoop-shell:/# hadoop fs -put /data/purchases.txt /purchases.txt
```

- `process_ecommerce.py`
