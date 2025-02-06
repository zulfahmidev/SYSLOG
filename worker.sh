!/bin/sh

if [[ "$MINIO_URL" != "" ]]; then
	echo "Mounting minio"
	goofys --profile default --endpoint=$MINIO_URL $MINIO_BUCKET /home/localoka/storage
fi


exec celery -A $CELERY_APP worker \
	-Q syslog,syslog_schedule \
	-P $CELERY_POOL \
	-c $CELERY_CONCURRENCY \
	-n ${CELERY_NODE_NAME}@${CELERY_NODE_HOST} \
	--prefetch-multiplier=$CELERY_PREFECT_MULTIPLIER \
	--loglevel=$CELERY_LOG_LEVEL
