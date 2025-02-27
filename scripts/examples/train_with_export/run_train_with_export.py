# Copyright 2022 Huawei Technologies Co., Ltd
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
"""Run MindFormer."""
import argparse
import os
import shutil

import numpy as np

import mindspore as ms
from mindspore.common import set_seed

from mindformers.tools.register import MindFormerConfig, ActionDict
from mindformers.core.parallel_config import build_parallel_config
from mindformers.tools.utils import str2bool, set_remote_save_url, check_in_modelarts, parse_value
from mindformers.core.context import build_context, build_profile_cb
from mindformers.trainer import build_trainer
from mindformers.tools.cloud_adapter import cloud_monitor
from mindformers.tools.logger import logger
from mindformers.tools import get_output_root_path
from mindformers.mindformer_book import MindFormerBook


if check_in_modelarts():
    import moxing as mox

SUPPORT_MODEL_NAMES = MindFormerBook().get_model_name_support_list()


def update_checkpoint_config(config, is_train=True):
    """update checkpoint config depending on is_train"""
    if (is_train and config.resume_training) or config.auto_trans_ckpt or os.path.isdir(config.load_checkpoint):
        logger.info("Leave load_checkpoint may because: ")
        logger.info("1. resume training need resume training info. ")
        logger.info("2. need load distributed shard checkpoint. ")
        if not config.load_checkpoint:
            config.load_checkpoint = config.model.model_config.checkpoint_name_or_path
        config.model.model_config.checkpoint_name_or_path = None
    else:
        if config.run_mode in ('train', 'finetune'):
            config.model.model_config.checkpoint_name_or_path = config.load_checkpoint
        elif config.run_mode in ['eval', 'predict'] and config.load_checkpoint:
            config.model.model_config.checkpoint_name_or_path = config.load_checkpoint
        config.load_checkpoint = None


def clear_auto_trans_output(config):
    """clear transformed_checkpoint and strategy"""
    if check_in_modelarts():
        obs_strategy_dir = os.path.join(config.remote_save_url, "strategy")
        if mox.file.exists(obs_strategy_dir) and config.local_rank == 0:
            mox.file.remove(obs_strategy_dir, recursive=True)
        obs_transformed_ckpt_dir = os.path.join(config.remote_save_url, "transformed_checkpoint")
        if mox.file.exists(obs_transformed_ckpt_dir) and config.local_rank == 0:
            mox.file.remove(obs_transformed_ckpt_dir, recursive=True)
        mox.file.make_dirs(obs_strategy_dir)
        mox.file.make_dirs(obs_transformed_ckpt_dir)
    else:
        strategy_dir = os.path.join(get_output_root_path(), "strategy")
        if os.path.exists(strategy_dir) and config.local_rank % 8 == 0:
            shutil.rmtree(strategy_dir)
        transformed_ckpt_dir = os.path.join(get_output_root_path(), "transformed_checkpoint")
        if os.path.exists(transformed_ckpt_dir) and config.local_rank % 8 == 0:
            shutil.rmtree(transformed_ckpt_dir)
        os.makedirs(strategy_dir, exist_ok=True)
        os.makedirs(transformed_ckpt_dir, exist_ok=True)

def create_task_trainer(config):
    trainer = build_trainer(config.trainer)
    if config.run_mode == 'train' or config.run_mode == 'finetune':
        trainer.train(config, is_full_config=True)
    elif config.run_mode == 'eval':
        trainer.evaluate(config, is_full_config=True)
    elif config.run_mode == 'predict':
        trainer.predict(config, is_full_config=True)
    elif config.run_mode == 'export':
        trainer.export(config, is_full_config=True)

@cloud_monitor()
def main(config):
    """main."""
    # init context
    build_context(config)

    if config.seed and \
            ms.context.get_auto_parallel_context("parallel_mode") \
            not in ["semi_auto_parallel", "auto_parallel"]:
        set_seed(config.seed)
        np.random.seed(config.seed)

    # build context config
    logger.info(".........Build context config..........")
    if config.run_mode == 'predict':
        if config.use_parallel and \
                config.parallel.parallel_mode in ['semi_auto_parallel', 1] and \
                config.parallel_config.data_parallel != 1:
            raise ValueError("The value of data parallel can only be set to 1, since the batch size of input is 1. ")
    build_parallel_config(config)
    logger.info("context config is: %s", config.parallel_config)
    logger.info("moe config is: %s", config.moe_config)

    if config.run_mode == 'train':
        update_checkpoint_config(config)

    if config.run_mode == 'finetune':
        if not config.load_checkpoint:
            raise ValueError("if run status is finetune, "
                             "load_checkpoint must be input")
        update_checkpoint_config(config)

    if config.run_mode in ['eval', 'predict']:
        update_checkpoint_config(config, is_train=False)

    # remote save url
    if check_in_modelarts() and config.remote_save_url:
        logger.info("remote_save_url is %s, the output file will be uploaded to here.", config.remote_save_url)
        set_remote_save_url(config.remote_save_url)

    # define callback and add profile callback
    if config.profile:
        config.profile_cb = build_profile_cb(config)

    if config.auto_trans_ckpt:
        clear_auto_trans_output(config)

    create_task_trainer(config)



if __name__ == "__main__":
    work_path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default="configs/mae/run_mae_vit_base_p16_224_800ep.yaml",
        required=True,
        help='YAML config files')
    parser.add_argument(
        '--mode', default=None, type=int,
        help='Running in GRAPH_MODE(0) or PYNATIVE_MODE(1). Default: GRAPH_MODE(0).'
             'GRAPH_MODE or PYNATIVE_MODE can be set by `mode` attribute and both modes support all backends,'
             'Default: None')
    parser.add_argument(
        '--device_id', default=None, type=int,
        help='ID of the target device, the value must be in [0, device_num_per_host-1], '
             'while device_num_per_host should be no more than 4096. Default: None')
    parser.add_argument(
        '--device_target', default=None, type=str,
        help='The target device to run, support "Ascend", "GPU", and "CPU".'
             'If device target is not set, the version of MindSpore package is used.'
             'Default: None')
    parser.add_argument(
        '--run_mode', default=None, type=str,
        help='task running status, it support [train, finetune, eval, predict].'
             'Default: None')
    parser.add_argument(
        '--do_eval', default=None, type=str2bool,
        help='whether do evaluate in training process.'
             'Default: None')
    parser.add_argument(
        '--train_dataset_dir', default=None, type=str,
        help='dataset directory of data loader to train/finetune. '
             'Default: None')
    parser.add_argument(
        '--eval_dataset_dir', default=None, type=str,
        help='dataset directory of data loader to eval. '
             'Default: None')
    parser.add_argument(
        '--predict_data', default=None, type=str,
        help='input data for predict, it support real data path or data directory.'
             'Default: None')
    parser.add_argument(
        '--load_checkpoint', default=None, type=str,
        help="load model checkpoint to train/finetune/eval/predict, "
             "it is also support input model name, such as 'mae_vit_base_p16', "
             "please refer to https://gitee.com/mindspore/mindformers#%E4%BB%8B%E7%BB%8D."
             "Default: None")
    parser.add_argument(
        '--src_strategy_path_or_dir', default=None, type=str,
        help="The strategy of load_checkpoint, "
             "if dir, it will be merged before transform checkpoint, "
             "if file, it will be used in transform checkpoint directly, "
             "Default: None, means load_checkpoint is a single whole ckpt, not distributed")
    parser.add_argument(
        '--auto_trans_ckpt', default=None, type=str2bool,
        help="if true, auto transform load_checkpoint to load in distributed model. ")
    parser.add_argument(
        '--only_save_strategy', default=None, type=str2bool,
        help="if true, when strategy files are saved, system exit. ")
    parser.add_argument(
        '--resume_training', default=None, type=str2bool,
        help="whether to load training context info, such as optimizer and epoch num")
    parser.add_argument(
        '--strategy_load_checkpoint', default=None, type=str,
        help='path to parallel strategy checkpoint to load, it support real data path or data directory.'
             'Default: None')
    parser.add_argument(
        '--remote_save_url', default=None, type=str,
        help='remote save url, where all the output files will tansferred and stroed in here. '
             'Default: None')
    parser.add_argument(
        '--seed', default=None, type=int,
        help='global random seed to train/finetune.'
             'Default: None')
    parser.add_argument(
        '--use_parallel', default=None, type=str2bool,
        help='whether use parallel mode. Default: None')
    parser.add_argument(
        '--profile', default=None, type=str2bool,
        help='whether use profile analysis. Default: None')
    parser.add_argument(
        '--options',
        nargs='+',
        action=ActionDict,
        help='override some settings in the used config, the key-value pair'
             'in xxx=yyy format will be merged into config file')
    parser.add_argument(
        '--epochs', default=None, type=int,
        help='train epochs.'
             'Default: None')
    parser.add_argument(
        '--batch_size', default=None, type=int,
        help='batch_size of datasets.'
             'Default: None')
    parser.add_argument(
        '--sink_mode', default=None, type=str2bool,
        help='whether use sink mode. '
             'Default: None')
    parser.add_argument(
        '--num_samples', default=None, type=int,
        help='number of datasets samples used.'
             'Default: None')
    parser.add_argument(
        '--export_device', default=1, type=int,
        help='export mindir device num, range in [1,8]'
    )

    args_, rest_args_ = parser.parse_known_args()
    rest_args_ = [i for item in rest_args_ for i in item.split("=")]
    if len(rest_args_) % 2 != 0:
        raise ValueError(f"input arg key-values are not in pair, please check input args. ")

    if args_.config is not None:
        args_.config = os.path.join(work_path, args_.config)
    config_ = MindFormerConfig(args_.config)
    if args_.device_id is not None:
        config_.context.device_id = args_.device_id
    if args_.device_target is not None:
        config_.context.device_target = args_.device_target
    if args_.mode is not None:
        config_.context.mode = args_.mode
    if args_.run_mode is not None:
        config_.run_mode = args_.run_mode
    if args_.do_eval is not None:
        config_.do_eval = args_.do_eval
    if args_.seed is not None:
        config_.seed = args_.seed
    if args_.use_parallel is not None:
        config_.use_parallel = args_.use_parallel
    if args_.load_checkpoint is not None:
        config_.load_checkpoint = args_.load_checkpoint
    if args_.src_strategy_path_or_dir is not None:
        config_.src_strategy_path_or_dir = args_.src_strategy_path_or_dir
    if args_.auto_trans_ckpt is not None:
        config_.auto_trans_ckpt = args_.auto_trans_ckpt
    if args_.only_save_strategy is not None:
        config_.only_save_strategy = args_.only_save_strategy
    if args_.resume_training is not None:
        config_.resume_training = args_.resume_training
    if args_.strategy_load_checkpoint is not None:
        if os.path.isdir(args_.strategy_load_checkpoint):
            ckpt_list = [os.path.join(args_.strategy_load_checkpoint, file)
                         for file in os.listdir(args_.strategy_load_checkpoint) if file.endwith(".ckpt")]
            args_.strategy_load_checkpoint = ckpt_list[0]
        config_.parallel.strategy_ckpt_load_file = args_.strategy_load_checkpoint
    if args_.remote_save_url is not None:
        config_.remote_save_url = args_.remote_save_url
    if args_.profile is not None:
        config_.profile = args_.profile
    if args_.options is not None:
        config_.merge_from_dict(args_.options)
    assert config_.run_mode in ['train', 'eval', 'predict', 'finetune', 'export'], \
        f"run status must be in {['train', 'eval', 'predict', 'finetune', 'export']}, but get {config_.run_mode}"
    if args_.train_dataset_dir:
        config_.train_dataset.data_loader.dataset_dir = args_.train_dataset_dir
    if args_.eval_dataset_dir:
        config_.eval_dataset.data_loader.dataset_dir = args_.eval_dataset_dir
    if config_.run_mode == 'predict':
        if args_.predict_data is None:
            logger.info("dataset by config is used as input_data.")
        elif os.path.isdir(args_.predict_data) and os.path.exists(args_.predict_data):
            predict_data = [os.path.join(root, file)
                            for root, _, file_list in os.walk(os.path.join(args_.predict_data)) for file in file_list
                            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")
                            or file.endswith(".JPEG") or file.endswith("bmp")]
            args_.predict_data = predict_data
        config_.input_data = args_.predict_data
    if args_.epochs is not None:
        config_.runner_config.epochs = args_.epochs
    if args_.batch_size is not None:
        config_.runner_config.batch_size = args_.batch_size
    if args_.sink_mode is not None:
        config_.runner_config.sink_mode = args_.sink_mode
    if args_.num_samples is not None:
        if config_.train_dataset and config_.train_dataset.data_loader:
            config_.train_dataset.data_loader.num_samples = args_.num_samples
        if config_.eval_dataset and config_.eval_dataset.data_loader:
            config_.eval_dataset.data_loader.num_samples = args_.num_samples

    while rest_args_:
        key = rest_args_.pop(0)
        value = rest_args_.pop(0)
        if not key.startswith("--"):
            raise ValueError("Custom config key need to start with --.")
        dists = key[2:].split(".")
        dist_config = config_
        while len(dists) > 1:
            if dists[0] not in dist_config:
                raise ValueError(f"{dists[0]} is not a key of {dist_config}, please check input arg keys. ")
            dist_config = dist_config[dists.pop(0)]
        dist_config[dists.pop()] = parse_value(value)

    main(config_)

    rank_id = int(os.getenv("RANK_ID", "0"))
    config_.run_mode = "export"
    config_.parallel_config.model_parallel = args_.export_device
    os.system("export RANK_SIZE=" + str(args_.export_device))
    config_.load_checkpoint = os.path.join(config_.remote_save_url, "checkpoint")
    config_.src_strategy_path_or_dir = os.path.join(config_.remote_save_url, "strategy", "ckpt_strategy_rank_0.ckpt")
    config_.model.model_config.use_past = True

    if rank_id < args_.export_device:
        main(config_)
