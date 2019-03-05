#!/bin/sh

curl https://api.godoc.org/importers/github.com/ethereum/go-ethereum | jq ".results[].path" | cut -d'/' -f1-3 | uniq > urls
DATE=$(date -I)
ALL=$(cat urls | wc -l)
NOFORK=$(cat urls | grep -v 'go-ethereum'| wc -l)
python save.py --cell-range A2:C $DATE $ALL $NOFORK
