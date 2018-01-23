#!/bin/sh
python /workdir/script/load_lmdb.py
python /workdir/script/train.py
python /workdir/script/save_caffe_model.py