# Builder Image
FROM python:3.9-alpine as builder

WORKDIR /app

RUN apk update && \
	apk add --virtual build-deps build-base postgresql-dev --no-cache && \
	pip install --upgrade pip

COPY requirements.txt requirements.txt

ARG CI_PACKAGE_USER \
	CI_PACKAGE_PASS \
	CI_GROUP_ID
ENV PIP_INDEX_URL="https://localoka-package-token:g39dNxupgVmyUFspPY25@gitlab.com/api/v4/groups/55767535/-/packages/pypi/simple"

RUN pip install --user --no-warn-script-location -r requirements.txt && \
	apk del build-deps

FROM python:3.9-alpine

RUN adduser -D localoka

WORKDIR /home/localoka

# Install goofys s3 client
RUN apk add fuse && \
	wget https://github.com/kahing/goofys/releases/latest/download/goofys && \
	chmod +x goofys && \
	mv goofys /usr/local/bin/

COPY --from=builder --chown=localoka:localoka /root/.local /home/localoka/.local

ENV \
	PATH=/home/localoka/.local/bin:$PATH \
	FLASK_APP="service:syslog" \
	FLASK_WORKER=1

COPY --chown=localoka:localoka service.py seed.py worker.py boot.sh worker.sh ./
RUN chmod +x boot.sh \
	&& chmod +x worker.sh \
	&& mkdir storage && chmod -R 755 /home/localoka/storage\
	&& chown -R localoka:localoka storage \
	&& mkdir data && chmod -R 755 /home/localoka/data \
	&& chown -R localoka:localoka data

COPY --chown=localoka:localoka migrations migrations
COPY --chown=localoka:localoka seed seed
COPY --chown=localoka:localoka app app

USER localoka

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
