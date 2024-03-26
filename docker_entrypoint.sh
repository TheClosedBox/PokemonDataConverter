#!/bin/bash

set -e

exec python3 scrapper.py &
exec python3 populate.py 