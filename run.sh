#!/bin/bash

set -x

mkdir -p ./out

for i in ./scenerarios/*; do sh "$i"; done > ./out/result.logs

