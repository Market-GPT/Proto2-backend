#!/bin/bash
celery -A Proto2 flower --port=5555 --basic_auth=user:$FLOWER_PASSWORD
