#!/bin/bash

echo "Downloading goofys binary"
wget -nc https://github.com/kahing/goofys/releases/latest/download/goofys

echo "prepare directory"
mkdir -p storage

echo "Mounting minio - dev"
echo $MINIO_URL
echo $MINIO_BUCKET
./goofys -f --debug_fuse --debug_s3 --profile default --endpoint=$MINIO_URL $MINIO_BUCKET storage
