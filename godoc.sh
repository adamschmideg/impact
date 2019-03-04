#!/bin/sh

REFS=$(curl https://api.godoc.org/importers/github.com/ethereum/go-ethereum | jq ".results[].path" | grep -v 'go-ethereum' | cut -d'/' -f1-3 | uniq | wc -l)
python save.py --cell-range A:A --value $REFS
