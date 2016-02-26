#!/bin/sh
C_FORCE_ROOT=1  celery -A scaner.tasks:celery worker -B
