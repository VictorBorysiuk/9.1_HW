# Redis Cluster (Realised)
Build master-slave redis cluster
Try all eviction strategies
Write a wrapper for Redis Client that implement probabilistic cache clearing 

## 1. Run docker container
`docker-compose up` 

## 2. Run several apps in different terminals
--id App ID
--key Key for getting value
--ttl TTL seconds
--sleep Sleep timeout for show refresh cache
```
python app.py -id 1 -sleep 1 -ttl 30
python app.py -id 2 -sleep 1
python app.py -id 3 -sleep 1
```
 