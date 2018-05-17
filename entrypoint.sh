#!/bin/bash
mkdir -p LOG_DIR
touch $ERROR_LOG
if [ -n "$COLLECTSTATIC" ];then
  echo 'start running python manage.py collectstatic...'
  python manage.py collectstatic
fi

if [ -z "$1" ];then
  exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --worker-class gevent \
    --timeout=$TIME_OUT \
    --bind $ADDRESS:$DJANGO_PORT \
    --log-level=debug \
    --log-file=$LOG_DIR/$ERROR_LOG \
    # --capture-output \
    --reload \
    --pid $PID_FILE
fi
exec "$@"
