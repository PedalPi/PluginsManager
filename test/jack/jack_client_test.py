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

import os
import unittest

from pluginsmanager.jack.jack_client import JackClient


class JackClientTest(unittest.TestCase):

    @unittest.skipIf('TRAVIS' in os.environ, 'Travis not contains audio interface')
    def test_assert_not_raises_error(self):
        """Assert not raises error"""
        client1 = JackClient(no_start_server=False, name="Client")
        client2 = JackClient(name="Client")

        client2.close()
        client1.close()
