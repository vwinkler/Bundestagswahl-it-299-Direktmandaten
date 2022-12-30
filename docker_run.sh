#!/bin/sh
echo "Building docker container.."
HASH=$(docker build --progress=plain . | tee /dev/tty | tail -1)
echo "Finished building docker container as $HASH"
echo "Running docker container $HASH.."
docker run --volume $(pwd):/data:z $HASH /data/votes.csv /data/seats.csv /data/output
echo "Docker container terminated"
