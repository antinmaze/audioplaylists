#!/bin/bash
docker exec -it postgres-db psql -U postgres -d diwidb
\dt

