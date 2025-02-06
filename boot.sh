#!/bin/sh

while true; do
	flask db upgrade
	if [[ "$?" == "0" ]]; then
		break
	fi
	echo "Upgrade command failed, retrying in 5 secs..."
	sleep 5
done

if [[ "$MINIO_URL" != "" ]]; then
	echo "Mounting minio"
	goofys --profile default --endpoint=$MINIO_URL $MINIO_BUCKET /home/localoka/storage
fi

# update seed
python seed.py

exec gunicorn -b 0.0.0.0:5000 \
	--access-logfile - \
	--error-logfile - \
	--workers=$GUNICORN_WORKER_COUNT \
	--worker-class=$GUNICORN_WORKER_CLASS \
	--worker-connections=$GUNICORN_WORKER_CONNECTION \
	--worker-tmp-dir=$GUNICORN_WORKER_TMP_DIR \
	--max-requests=$GUNICORN_MAX_REQUEST \
	--max-requests-jitter=$GUNICORN_MAX_REQUEST_JITTER \
	$FLASK_APP
