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

import collections
import threading


class ManagerScopes(object):

    def __init__(self):
        self._scopes = {}

    @property
    def current(self):
        identifier = threading.current_thread().ident

        if identifier not in self._scopes:
            self._scopes[identifier] = Scope()

        return self._scopes[identifier]

    def enter(self, identifier):
        """
        Open a scope.

        Informs that changes occurs by the ``identifier`` and isn't necessary
        informs the changes for identifier

        :param identifier: Identifier for instance that causes changes
        """
        self.current.enter(identifier)

    def exit(self):
        """
        Closes the last scope added
        """
        self.current.exit()


class Scope(object):

    def __init__(self):
        self._scope = collections.deque()

    def enter(self, identifier):
        self._scope.append(identifier)

    def exit(self):
        self._scope.pop()

    @property
    def identifier(self):
        try:
            return self._scope[-1]
        except IndexError:
            return None
