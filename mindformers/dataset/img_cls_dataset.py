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
"""Image Classification Dataset."""
import os

from mindspore.dataset.transforms import TypeCast
import mindspore.common.dtype as mstype

from mindformers.tools.register import MindFormerRegister, MindFormerModuleType
from mindformers.tools.logger import logger
from mindformers.version_control import get_dataset_map

from .dataloader import build_dataset_loader
from .transforms import build_transforms
from .sampler import build_sampler
from .base_dataset import BaseDataset


@MindFormerRegister.register(MindFormerModuleType.DATASET)
class ImageCLSDataset(BaseDataset):
    """
    Image Classification Dataset API.

    Args:
        dataset_config (dict): Config for dataset.

    Returns:
        A dataset for ImageCLSDataset.

    Examples:
        >>> from mindformers.tools.register import MindFormerConfig
        >>> from mindformers import MindFormerBook
        >>> from mindformers.dataset import ImageCLSDataset
        >>> from mindformers.dataset import build_dataset, check_dataset_config
        >>> config_dict_list = MindFormerBook.get_trainer_support_task_list()
        >>> config_path = config_dict_list['image_classification']['vit_base_p16']
        >>> # Initialize a MindFormerConfig instance with a specific config file of yaml.
        >>> config = MindFormerConfig(config_path)
        >>> config.train_dataset.data_loader.dataset_dir = "The required task dataset path"
        >>> # Note:
        >>> #     The detailed data setting could refer to
        >>> #     https://gitee.com/mindspore/mindformers/blob/dev/docs/model_cards/vit.md
        >>> check_dataset_config(config)
        >>> # use class to build dataset
        >>> dataset_from_class = ImageCLSDataset(config.train_dataset_task.dataset_config)
    """
    def __new__(cls, dataset_config: dict = None):
        logger.info("Now Create Image Classification Dataset.")
        cls.init_dataset_config(dataset_config)
        rank_id = int(os.getenv("RANK_ID", "0"))
        device_num = int(os.getenv("RANK_SIZE", "1"))

        dataset = build_dataset_loader(
            dataset_config.data_loader, default_args={'num_shards': device_num, 'shard_id': rank_id})
        transforms = build_transforms(dataset_config.transforms)
        sampler = build_sampler(dataset_config.sampler)
        type_cast_op = TypeCast(mstype.int32)

        if sampler is not None:
            dataset = dataset.use_sampler(sampler)

        if transforms is not None:
            dataset = get_dataset_map(dataset, transforms,
                                      input_columns=dataset_config.input_columns[0],
                                      num_parallel_workers=dataset_config.num_parallel_workers,
                                      python_multiprocessing=dataset_config.python_multiprocessing)

        dataset = get_dataset_map(dataset, type_cast_op,
                                  input_columns=dataset_config.input_columns[1],
                                  num_parallel_workers=dataset_config.num_parallel_workers)

        dataset = dataset.batch(dataset_config.batch_size, drop_remainder=dataset_config.drop_remainder,
                                num_parallel_workers=dataset_config.num_parallel_workers)
        if not dataset_config.do_eval and dataset_config.mixup_op is not None:
            mixup_op = build_transforms(class_name="Mixup", **dataset_config.mixup_op)
            dataset = get_dataset_map(dataset, mixup_op,
                                      input_columns=dataset_config.input_columns,
                                      output_columns=dataset_config.output_columns,
                                      num_parallel_workers=dataset_config.num_parallel_workers)
        dataset = dataset.project(columns=dataset_config.output_columns)
        dataset = dataset.repeat(dataset_config.repeat)
        return dataset
