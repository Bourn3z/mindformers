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

"""mindformers init"""
from mindformers import common, auto_class, dataset, models, modules
from .dataset import MIMDataset, ImageCLSDataset
from .models import *
from .common import *
from .modules import *
from .pipeline import *
from .trainer import *
from .auto_class import *
from .wrapper import ClassificationMoeWrapper
from .tools import logger, MindFormerRegister, MindFormerModuleType, MindFormerConfig, CFTS
from .mindformer_book import MindFormerBook

__all__ = []
__all__.extend(common.__all__)
__all__.extend(auto_class.__all__)
__all__.extend(models.__all__)