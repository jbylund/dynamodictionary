#!/usr/bin/env bash
set -eux
docker build -t jbylund/semci:latest .
docker push jbylund/semci:latest
