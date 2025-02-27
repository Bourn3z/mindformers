#!/bin/bash
# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

if [ $# != 4 ] && [ $# != 5 ] && [ $# != 6 ]
then
  echo "Usage Help: bash run_distribute.sh [RANK_TABLE_FILE] [CONFIG_PATH] [DEVICE_RANGE] [RUN_STATUS] For Multiple Devices In Single Machine"
  echo "Usage Help: bash run_distribute.sh [RANK_TABLE_FILE] [CONFIG_PATH] [DEVICE_RANGE] [RUN_STATUS] [RANK_SIZE] For Multiple Devices In Multiple Machines"
  echo "Usage Help: bash run_distribute.sh [RANK_TABLE_FILE] [CONFIG_PATH] [DEVICE_RANGE] predict [PREDICT_DATA] For Multiple Devices Predict In Single Machine"
  echo "Usage Help: bash run_distribute.sh [RANK_TABLE_FILE] [CONFIG_PATH] [DEVICE_RANGE] predict [RANK_SIZE] [PREDICT_DATA] For Multiple Devices Predict In Multiple Machines"
  exit 1
fi

check_real_path(){
  if [ "${1:0:1}" == "/" ]; then
    echo "$1"
  else
    echo "$(realpath -m $PWD/$1)"
  fi
}

PATH1=$(check_real_path $1)
CONFIG_FILE=$(check_real_path $2)
DEVICE_RANGE=$3
RUN_STATUS=$4
DEVICE_RANGE_LEN=${#DEVICE_RANGE}
DEVICE_RANGE=${DEVICE_RANGE:1:DEVICE_RANGE_LEN-2}
PREFIX=${DEVICE_RANGE%%","*}
INDEX=${#PREFIX}
START_DEVICE=${DEVICE_RANGE:0:INDEX}
END_DEVICE=${DEVICE_RANGE:INDEX+1:DEVICE_RANGE_LEN-INDEX}

if [ ! -f $PATH1 ]
then
    echo "error: RANK_TABLE_FILE=$PATH1 is not a file"
exit 1
fi

if [ ! -f $CONFIG_FILE ]
then
    echo "error: config_path=$CONFIG_FILE is not a file"
exit 1
fi

if [[ ! $START_DEVICE =~ ^[0-9]+$ ]]; then
    echo "error: start_device=$START_DEVICE is not a number"
exit 1
fi

if [[ ! $END_DEVICE =~ ^[0-9]+$ ]]; then
    echo "error: end_device=$END_DEVICE is not a number"
exit 1
fi

ulimit -u unlimited
if [ $RUN_STATUS != "predict" ]
then
  if [ $# == 4 ]
  then
    export RANK_SIZE=$(($END_DEVICE - $START_DEVICE))
  else
    export RANK_SIZE=$5
  fi
else
  if [ $# == 5 ]
  then
    export RANK_SIZE=$(($END_DEVICE - $START_DEVICE))
    PREDICT_DATA=$5
  else
    export RANK_SIZE=$5
    PREDICT_DATA=$6
  fi
fi

export RANK_TABLE_FILE=$PATH1

output_dir=$(cat $CONFIG_FILE | grep output_dir)
if [ ! -n "$output_dir" ]; then
  echo "Error: No output_dir in $CONFIG_FILE"
  exit 1
fi
if [[ ! $output_dir =~ "'" ]]&&[[ ! $output_dir =~ "\"" ]]; then
  echo "Error: Please use ' or \" to enclose output_dir"
  exit 1
elif [[ $output_dir =~ "'" ]]; then
  output_dir=${output_dir#*\'}
  output_dir=${output_dir%\'*}
else
  output_dir=${output_dir#*\"}
  output_dir=${output_dir%\"*}
fi
if [[ $output_dir == "./output" ]]
then
  echo "output_dir is ./output"
  export LOCAL_DEFAULT_PATH="../../output"
else
  echo "output_dir is $output_dir"
  export LOCAL_DEFAULT_PATH=$output_dir
fi

export CHECKPOINT_DOWNLOAD_FOLDER="../../checkpoint_download"
export CHECKPOINT_SAVE_FOLDER="../../checkpoint_save"

shopt -s extglob
if [ $RUN_STATUS != "predict" ]
then
  if [ $# == 4 ]
  then
    for((i=${START_DEVICE}; i<${END_DEVICE}; i++))
    do
        export DEVICE_ID=${i}
        export RANK_ID=$((i-START_DEVICE))
        rm -rf ./mf_parallel$i/!(rank_*)
        test -d ./mf_parallel$i || mkdir ./mf_parallel$i
        cp ../*.py ./mf_parallel$i
        cp -r ../configs ./mf_parallel$i
        cp -r ../mindformers ./mf_parallel$i
        cd ./mf_parallel$i || exit
        echo "start training for rank $RANK_ID, device $DEVICE_ID"
        env > env.log
        mkdir -p $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID
        python run_mindformer.py --config=$CONFIG_FILE --use_parallel=True --run_mode=$RUN_STATUS \
               --output_dir=$LOCAL_DEFAULT_PATH \
               &> $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID/mindformer.log &
        cd ..
    done
  else
    for((i=${START_DEVICE}; i<${END_DEVICE}; i++))
    do
        export RANK_ID=${i}
        export DEVICE_ID=$((i-START_DEVICE))
        rm -rf ./mf_parallel$i/!(rank_*)
        test -d ./mf_parallel$i || mkdir ./mf_parallel$i
        cp ../*.py ./mf_parallel$i
        cp -r ../configs ./mf_parallel$i
        cp -r ../mindformers ./mf_parallel$i
        cd ./mf_parallel$i || exit
        echo "start training for rank $RANK_ID, device $DEVICE_ID"
        env > env.log
        mkdir -p $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID
        python run_mindformer.py --config=$CONFIG_FILE --use_parallel=True --run_mode=$RUN_STATUS \
               --output_dir=$LOCAL_DEFAULT_PATH \
               &> $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID/mindformer.log &
        cd ..
    done
  fi
else
  if [ $# == 5 ]
  then
    for((i=${START_DEVICE}; i<${END_DEVICE}; i++))
    do
        export DEVICE_ID=${i}
        export RANK_ID=$((i-START_DEVICE))
        rm -rf ./mf_parallel$i/!(rank_*)
        test -d ./mf_parallel$i || mkdir ./mf_parallel$i
        cp ../*.py ./mf_parallel$i
        cp -r ../configs ./mf_parallel$i
        cp -r ../mindformers ./mf_parallel$i
        if [ -f "$PREDICT_DATA" ]
        then
          cp "$PREDICT_DATA" ./mf_parallel$i
        fi
        cd ./mf_parallel$i || exit
        echo "start training for rank $RANK_ID, device $DEVICE_ID"
        env > env.log
        mkdir -p $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID
        python run_mindformer.py --config=$CONFIG_FILE --use_parallel=True --run_mode=$RUN_STATUS \
               --output_dir=$LOCAL_DEFAULT_PATH --predict_data "$PREDICT_DATA" \
               &> $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID/mindformer.log &
        cd ..
    done
  else
    for((i=${START_DEVICE}; i<${END_DEVICE}; i++))
    do
        export RANK_ID=${i}
        export DEVICE_ID=$((i-START_DEVICE))
        rm -rf ./mf_parallel$i/!(rank_*)
        test -d ./mf_parallel$i || mkdir ./mf_parallel$i
        cp ../*.py ./mf_parallel$i
        cp -r ../configs ./mf_parallel$i
        cp -r ../mindformers ./mf_parallel$i
        if [ -f "$PREDICT_DATA" ]
        then
          cp "$PREDICT_DATA" ./mf_parallel$i
        fi
        cd ./mf_parallel$i || exit
        echo "start training for rank $RANK_ID, device $DEVICE_ID"
        env > env.log
        mkdir -p $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID
        python run_mindformer.py --config=$CONFIG_FILE --use_parallel=True --run_mode=$RUN_STATUS \
               --output_dir=$LOCAL_DEFAULT_PATH --predict_data "$PREDICT_DATA" \
               &> $LOCAL_DEFAULT_PATH/log/rank_$RANK_ID/mindformer.log &
        cd ..
    done
  fi
fi
shopt -u extglob


#cd ./pretrain_parallel${START_DEVICE} || exit
#tail -f mindformer.log

# if you want kill current job, you can use as follow:
# kill -9 $(ps aux | grep "python run_mindformer.py" | grep -v grep | awk '{print $2}')
