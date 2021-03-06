# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum


class UpdateType(Enum):
    """
    Enumeration for informs the change type.

    See :class:`.UpdatesObserver` for more details
    """
    CREATED = 0
    """ Informs that the change is caused by the creation of an object"""
    UPDATED = 1
    """ Informs that the change is caused by the update of an object"""
    DELETED = 2
    """ Informs that the change is caused by the removal of an object"""


class CustomChange:
    """
    Enumeration for informs the change type of custom changes.

    See :class:`.UpdatesObserver` for more details
    """
    PEDALBOARD_NAME = 0
    PEDALBOARD_DATA = 1
    BANK_NAME = 2
