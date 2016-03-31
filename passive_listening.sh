#!/usr/bin/env bash
pocketsphinx_continuous -kws keyphrase.list -kws_threshold 1e-1 -inmic yes -logfn /dev/null | python alan.py
