"""

ro.py  
A modern, asynchronous wrapper for the Roblox web API.

Copyright 2020-present anyastrophic  
License: MIT, see LICENSE

"""

__title__ = "roblox"
__author__ = "anyastrophic"
__license__ = "MIT"
__copyright__ = "Copyright 2023-present anyastrophic"
__version__ = "2.0.1"

import logging

from .client import Client
from .creatortype import CreatorType
from .thumbnails import ThumbnailState, ThumbnailFormat, ThumbnailReturnPolicy, AvatarThumbnailType
from .universes import UniverseGenre, UniverseAvatarType
from .utilities.exceptions import *
from .utilities.types import *

logging.getLogger(__name__).addHandler(logging.NullHandler())
