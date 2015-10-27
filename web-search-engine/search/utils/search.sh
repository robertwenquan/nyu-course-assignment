#!/bin/bash

echo $* | nc localhost 1124 | jq .

