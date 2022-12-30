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
# This file was refer to project:
# https://huggingface.co/WinKawaks/vit-tiny-patch16-224/blob/main/config.json
# ============================================================================
"""labels of imagenet"""
labels = {"imagenet": [
    "tench", "goldfish", "great white shark", "tiger shark", "hammerhead",
    "goldfish", "great white shark", "tiger shark", "hammerhead", "electric ray",
    "great white shark", "tiger shark", "hammerhead", "electric ray", "stingray",
    "tiger shark", "hammerhead", "electric ray", "stingray", "cock",
    "hammerhead", "electric ray", "stingray", "cock", "hen",
    "electric ray", "stingray", "cock", "hen", "ostrich",
    "stingray", "cock", "hen", "ostrich", "brambling",
    "cock", "hen", "ostrich", "brambling", "goldfinch",
    "hen", "ostrich", "brambling", "goldfinch", "house finch",
    "ostrich", "brambling", "goldfinch", "house finch", "junco",
    "brambling", "goldfinch", "house finch", "junco", "indigo bunting",
    "goldfinch", "house finch", "junco", "indigo bunting", "robin",
    "house finch", "junco", "indigo bunting", "robin", "bulbul",
    "junco", "indigo bunting", "robin", "bulbul", "jay",
    "indigo bunting", "robin", "bulbul", "jay", "magpie",
    "robin", "bulbul", "jay", "magpie", "chickadee",
    "bulbul", "jay", "magpie", "chickadee", "water ouzel",
    "jay", "magpie", "chickadee", "water ouzel", "kite",
    "magpie", "chickadee", "water ouzel", "kite", "bald eagle",
    "chickadee", "water ouzel", "kite", "bald eagle", "vulture",
    "water ouzel", "kite", "bald eagle", "vulture", "great grey owl",
    "kite", "bald eagle", "vulture", "great grey owl", "European fire salamander",
    "bald eagle", "vulture", "great grey owl", "European fire salamander", "common newt",
    "vulture", "great grey owl", "European fire salamander", "common newt", "eft",
    "great grey owl", "European fire salamander", "common newt", "eft", "spotted salamander",
    "European fire salamander", "common newt", "eft", "spotted salamander", "axolotl",
    "common newt", "eft", "spotted salamander", "axolotl", "bullfrog",
    "eft", "spotted salamander", "axolotl", "bullfrog", "tree frog",
    "spotted salamander", "axolotl", "bullfrog", "tree frog", "tailed frog",
    "axolotl", "bullfrog", "tree frog", "tailed frog", "loggerhead",
    "bullfrog", "tree frog", "tailed frog", "loggerhead", "leatherback turtle",
    "tree frog", "tailed frog", "loggerhead", "leatherback turtle", "mud turtle",
    "tailed frog", "loggerhead", "leatherback turtle", "mud turtle", "terrapin",
    "loggerhead", "leatherback turtle", "mud turtle", "terrapin", "box turtle",
    "leatherback turtle", "mud turtle", "terrapin", "box turtle", "banded gecko",
    "mud turtle", "terrapin", "box turtle", "banded gecko", "common iguana",
    "terrapin", "box turtle", "banded gecko", "common iguana", "American chameleon",
    "box turtle", "banded gecko", "common iguana", "American chameleon", "whiptail",
    "banded gecko", "common iguana", "American chameleon", "whiptail", "agama",
    "common iguana", "American chameleon", "whiptail", "agama", "frilled lizard",
    "American chameleon", "whiptail", "agama", "frilled lizard", "alligator lizard",
    "whiptail", "agama", "frilled lizard", "alligator lizard", "Gila monster",
    "agama", "frilled lizard", "alligator lizard", "Gila monster", "green lizard",
    "frilled lizard", "alligator lizard", "Gila monster", "green lizard", "African chameleon",
    "alligator lizard", "Gila monster", "green lizard", "African chameleon", "Komodo dragon",
    "Gila monster", "green lizard", "African chameleon", "Komodo dragon", "African crocodile",
    "green lizard", "African chameleon", "Komodo dragon", "African crocodile", "American alligator",
    "African chameleon", "Komodo dragon", "African crocodile", "American alligator", "triceratops",
    "Komodo dragon", "African crocodile", "American alligator", "triceratops", "thunder snake",
    "African crocodile", "American alligator", "triceratops", "thunder snake", "ringneck snake",
    "American alligator", "triceratops", "thunder snake", "ringneck snake", "hognose snake",
    "triceratops", "thunder snake", "ringneck snake", "hognose snake", "green snake",
    "thunder snake", "ringneck snake", "hognose snake", "green snake", "king snake",
    "ringneck snake", "hognose snake", "green snake", "king snake", "garter snake",
    "hognose snake", "green snake", "king snake", "garter snake", "water snake",
    "green snake", "king snake", "garter snake", "water snake", "vine snake",
    "king snake", "garter snake", "water snake", "vine snake", "night snake",
    "garter snake", "water snake", "vine snake", "night snake", "boa constrictor",
    "water snake", "vine snake", "night snake", "boa constrictor", "rock python",
    "vine snake", "night snake", "boa constrictor", "rock python", "Indian cobra",
    "night snake", "boa constrictor", "rock python", "Indian cobra", "green mamba",
    "boa constrictor", "rock python", "Indian cobra", "green mamba", "sea snake",
    "rock python", "Indian cobra", "green mamba", "sea snake", "horned viper",
    "Indian cobra", "green mamba", "sea snake", "horned viper", "diamondback",
    "green mamba", "sea snake", "horned viper", "diamondback", "sidewinder",
    "sea snake", "horned viper", "diamondback", "sidewinder", "trilobite",
    "horned viper", "diamondback", "sidewinder", "trilobite", "harvestman",
    "diamondback", "sidewinder", "trilobite", "harvestman", "scorpion",
    "sidewinder", "trilobite", "harvestman", "scorpion", "black and gold garden spider",
    "trilobite", "harvestman", "scorpion", "black and gold garden spider", "barn spider",
    "harvestman", "scorpion", "black and gold garden spider", "barn spider", "garden spider",
    "scorpion", "black and gold garden spider", "barn spider", "garden spider", "black widow",
    "black and gold garden spider", "barn spider", "garden spider", "black widow", "tarantula",
    "barn spider", "garden spider", "black widow", "tarantula", "wolf spider",
    "garden spider", "black widow", "tarantula", "wolf spider", "tick",
    "black widow", "tarantula", "wolf spider", "tick", "centipede",
    "tarantula", "wolf spider", "tick", "centipede", "black grouse",
    "wolf spider", "tick", "centipede", "black grouse", "ptarmigan",
    "tick", "centipede", "black grouse", "ptarmigan", "ruffed grouse",
    "centipede", "black grouse", "ptarmigan", "ruffed grouse", "prairie chicken",
    "black grouse", "ptarmigan", "ruffed grouse", "prairie chicken", "peacock",
    "ptarmigan", "ruffed grouse", "prairie chicken", "peacock", "quail",
    "ruffed grouse", "prairie chicken", "peacock", "quail", "partridge",
    "prairie chicken", "peacock", "quail", "partridge", "African grey",
    "peacock", "quail", "partridge", "African grey", "macaw",
    "quail", "partridge", "African grey", "macaw", "sulphur-crested cockatoo",
    "partridge", "African grey", "macaw", "sulphur-crested cockatoo", "lorikeet",
    "African grey", "macaw", "sulphur-crested cockatoo", "lorikeet", "coucal",
    "macaw", "sulphur-crested cockatoo", "lorikeet", "coucal", "bee eater",
    "sulphur-crested cockatoo", "lorikeet", "coucal", "bee eater", "hornbill",
    "lorikeet", "coucal", "bee eater", "hornbill", "hummingbird",
    "coucal", "bee eater", "hornbill", "hummingbird", "jacamar",
    "bee eater", "hornbill", "hummingbird", "jacamar", "toucan",
    "hornbill", "hummingbird", "jacamar", "toucan", "drake",
    "hummingbird", "jacamar", "toucan", "drake", "red-breasted merganser",
    "jacamar", "toucan", "drake", "red-breasted merganser", "goose",
    "toucan", "drake", "red-breasted merganser", "goose", "black swan",
    "drake", "red-breasted merganser", "goose", "black swan", "tusker",
    "red-breasted merganser", "goose", "black swan", "tusker", "echidna",
    "goose", "black swan", "tusker", "echidna", "platypus",
    "black swan", "tusker", "echidna", "platypus", "wallaby",
    "tusker", "echidna", "platypus", "wallaby", "koala",
    "echidna", "platypus", "wallaby", "koala", "wombat",
    "platypus", "wallaby", "koala", "wombat", "jellyfish",
    "wallaby", "koala", "wombat", "jellyfish", "sea anemone",
    "koala", "wombat", "jellyfish", "sea anemone", "brain coral",
    "wombat", "jellyfish", "sea anemone", "brain coral", "flatworm",
    "jellyfish", "sea anemone", "brain coral", "flatworm", "nematode",
    "sea anemone", "brain coral", "flatworm", "nematode", "conch",
    "brain coral", "flatworm", "nematode", "conch", "snail",
    "flatworm", "nematode", "conch", "snail", "slug",
    "nematode", "conch", "snail", "slug", "sea slug",
    "conch", "snail", "slug", "sea slug", "chiton",
    "snail", "slug", "sea slug", "chiton", "chambered nautilus",
    "slug", "sea slug", "chiton", "chambered nautilus", "Dungeness crab",
    "sea slug", "chiton", "chambered nautilus", "Dungeness crab", "rock crab",
    "chiton", "chambered nautilus", "Dungeness crab", "rock crab", "fiddler crab",
    "chambered nautilus", "Dungeness crab", "rock crab", "fiddler crab", "king crab",
    "Dungeness crab", "rock crab", "fiddler crab", "king crab", "American lobster",
    "rock crab", "fiddler crab", "king crab", "American lobster", "spiny lobster",
    "fiddler crab", "king crab", "American lobster", "spiny lobster", "crayfish",
    "king crab", "American lobster", "spiny lobster", "crayfish", "hermit crab",
    "American lobster", "spiny lobster", "crayfish", "hermit crab", "isopod",
    "spiny lobster", "crayfish", "hermit crab", "isopod", "white stork",
    "crayfish", "hermit crab", "isopod", "white stork", "black stork",
    "hermit crab", "isopod", "white stork", "black stork", "spoonbill",
    "isopod", "white stork", "black stork", "spoonbill", "flamingo",
    "white stork", "black stork", "spoonbill", "flamingo", "little blue heron",
    "black stork", "spoonbill", "flamingo", "little blue heron", "American egret",
    "spoonbill", "flamingo", "little blue heron", "American egret", "bittern",
    "flamingo", "little blue heron", "American egret", "bittern", "crane",
    "little blue heron", "American egret", "bittern", "crane", "limpkin",
    "American egret", "bittern", "crane", "limpkin", "European gallinule",
    "bittern", "crane", "limpkin", "European gallinule", "American coot",
    "crane", "limpkin", "European gallinule", "American coot", "bustard",
    "limpkin", "European gallinule", "American coot", "bustard", "ruddy turnstone",
    "European gallinule", "American coot", "bustard", "ruddy turnstone", "red-backed sandpiper",
    "American coot", "bustard", "ruddy turnstone", "red-backed sandpiper", "redshank",
    "bustard", "ruddy turnstone", "red-backed sandpiper", "redshank", "dowitcher",
    "ruddy turnstone", "red-backed sandpiper", "redshank", "dowitcher", "oystercatcher",
    "red-backed sandpiper", "redshank", "dowitcher", "oystercatcher", "pelican",
    "redshank", "dowitcher", "oystercatcher", "pelican", "king penguin",
    "dowitcher", "oystercatcher", "pelican", "king penguin", "albatross",
    "oystercatcher", "pelican", "king penguin", "albatross", "grey whale",
    "pelican", "king penguin", "albatross", "grey whale", "killer whale",
    "king penguin", "albatross", "grey whale", "killer whale", "dugong",
    "albatross", "grey whale", "killer whale", "dugong", "sea lion",
    "grey whale", "killer whale", "dugong", "sea lion", "Chihuahua",
    "killer whale", "dugong", "sea lion", "Chihuahua", "Japanese spaniel",
    "dugong", "sea lion", "Chihuahua", "Japanese spaniel", "Maltese dog",
    "sea lion", "Chihuahua", "Japanese spaniel", "Maltese dog", "Pekinese",
    "Chihuahua", "Japanese spaniel", "Maltese dog", "Pekinese", "Shih-Tzu",
    "Japanese spaniel", "Maltese dog", "Pekinese", "Shih-Tzu", "Blenheim spaniel",
    "Maltese dog", "Pekinese", "Shih-Tzu", "Blenheim spaniel", "papillon",
    "Pekinese", "Shih-Tzu", "Blenheim spaniel", "papillon", "toy terrier",
    "Shih-Tzu", "Blenheim spaniel", "papillon", "toy terrier", "Rhodesian ridgeback",
    "Blenheim spaniel", "papillon", "toy terrier", "Rhodesian ridgeback", "Afghan hound",
    "papillon", "toy terrier", "Rhodesian ridgeback", "Afghan hound", "basset",
    "toy terrier", "Rhodesian ridgeback", "Afghan hound", "basset", "beagle",
    "Rhodesian ridgeback", "Afghan hound", "basset", "beagle", "bloodhound",
    "Afghan hound", "basset", "beagle", "bloodhound", "bluetick",
    "basset", "beagle", "bloodhound", "bluetick", "black-and-tan coonhound",
    "beagle", "bloodhound", "bluetick", "black-and-tan coonhound", "Walker hound",
    "bloodhound", "bluetick", "black-and-tan coonhound", "Walker hound", "English foxhound",
    "bluetick", "black-and-tan coonhound", "Walker hound", "English foxhound", "redbone",
    "black-and-tan coonhound", "Walker hound", "English foxhound", "redbone", "borzoi",
    "Walker hound", "English foxhound", "redbone", "borzoi", "Irish wolfhound",
    "English foxhound", "redbone", "borzoi", "Irish wolfhound", "Italian greyhound",
    "redbone", "borzoi", "Irish wolfhound", "Italian greyhound", "whippet",
    "borzoi", "Irish wolfhound", "Italian greyhound", "whippet", "Ibizan hound",
    "Irish wolfhound", "Italian greyhound", "whippet", "Ibizan hound", "Norwegian elkhound",
    "Italian greyhound", "whippet", "Ibizan hound", "Norwegian elkhound", "otterhound",
    "whippet", "Ibizan hound", "Norwegian elkhound", "otterhound", "Saluki",
    "Ibizan hound", "Norwegian elkhound", "otterhound", "Saluki", "Scottish deerhound",
    "Norwegian elkhound", "otterhound", "Saluki", "Scottish deerhound", "Weimaraner",
    "otterhound", "Saluki", "Scottish deerhound", "Weimaraner", "Staffordshire bullterrier",
    "Saluki", "Scottish deerhound", "Weimaraner", "Staffordshire bullterrier", "American Staffordshire terrier",
    "Scottish deerhound", "Weimaraner", "Staffordshire bullterrier", "American Staffordshire terrier",
    "Bedlington terrier",
    "Weimaraner", "Staffordshire bullterrier", "American Staffordshire terrier", "Bedlington terrier", "Border terrier",
    "Staffordshire bullterrier", "American Staffordshire terrier", "Bedlington terrier", "Border terrier",
    "Kerry blue terrier",
    "American Staffordshire terrier", "Bedlington terrier", "Border terrier", "Kerry blue terrier", "Irish terrier",
    "Bedlington terrier", "Border terrier", "Kerry blue terrier", "Irish terrier", "Norfolk terrier",
    "Border terrier", "Kerry blue terrier", "Irish terrier", "Norfolk terrier", "Norwich terrier",
    "Kerry blue terrier", "Irish terrier", "Norfolk terrier", "Norwich terrier", "Yorkshire terrier",
    "Irish terrier", "Norfolk terrier", "Norwich terrier", "Yorkshire terrier", "wire-haired fox terrier",
    "Norfolk terrier", "Norwich terrier", "Yorkshire terrier", "wire-haired fox terrier", "Lakeland terrier",
    "Norwich terrier", "Yorkshire terrier", "wire-haired fox terrier", "Lakeland terrier", "Sealyham terrier",
    "Yorkshire terrier", "wire-haired fox terrier", "Lakeland terrier", "Sealyham terrier", "Airedale",
    "wire-haired fox terrier", "Lakeland terrier", "Sealyham terrier", "Airedale", "cairn",
    "Lakeland terrier", "Sealyham terrier", "Airedale", "cairn", "Australian terrier",
    "Sealyham terrier", "Airedale", "cairn", "Australian terrier", "Dandie Dinmont",
    "Airedale", "cairn", "Australian terrier", "Dandie Dinmont", "Boston bull",
    "cairn", "Australian terrier", "Dandie Dinmont", "Boston bull", "miniature schnauzer",
    "Australian terrier", "Dandie Dinmont", "Boston bull", "miniature schnauzer", "giant schnauzer",
    "Dandie Dinmont", "Boston bull", "miniature schnauzer", "giant schnauzer", "standard schnauzer",
    "Boston bull", "miniature schnauzer", "giant schnauzer", "standard schnauzer", "Scotch terrier",
    "miniature schnauzer", "giant schnauzer", "standard schnauzer", "Scotch terrier", "Tibetan terrier",
    "giant schnauzer", "standard schnauzer", "Scotch terrier", "Tibetan terrier", "silky terrier",
    "standard schnauzer", "Scotch terrier", "Tibetan terrier", "silky terrier", "soft-coated wheaten terrier",
    "Scotch terrier", "Tibetan terrier", "silky terrier", "soft-coated wheaten terrier", "West Highland white terrier",
]}