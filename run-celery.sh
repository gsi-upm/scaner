#!/bin/sh
sleep 10
C_FORCE_ROOT=1  celery -A scaner.tasks:celery worker -B
#C_FORCE_ROOT=1  celery flower -A scaner.tasks:celery --broker=redis://redis:6379/
