#!/bin/bash

echo "Waiting for everything else to startup"
sleep 15

export TG_TOKEN="5467190418:AAE0Y3bpqs91otka-Id3D9qdpSQ6ZXcxD2s"

exec "$@"
