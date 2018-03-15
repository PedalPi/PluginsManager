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

import asyncio
import json
import os


class Persistence(object):

    @staticmethod
    def read(path, create_file=False):
        """
        Reads the json data in path

        :param Path path: Path that json data will be readed
        :param create_file: Creates the file if it isn't exists

        :return: json data
        """
        if create_file:
            with open(str(path), 'a+') as data_file:
                data_file.seek(0)
                return json.load(data_file)

        else:
            with open(str(path)) as data_file:
                return json.load(data_file)

    @staticmethod
    def save(path, json_data):
        """
        Saves json_data in path

        :param Path path: Path that json_data will be persisted
        :param json_data: Data that will be persisted
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(Persistence._save(path, json_data), loop)
            else:
                loop.run_until_complete(Persistence._save(path, json_data))
        except AssertionError:
            Persistence._save(path, json_data)

    @staticmethod
    @asyncio.coroutine
    def _save(path, json_data):
        with open(str(path), "w+") as file:
            file.write(json.dumps(json_data))

    @staticmethod
    def delete(path):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(Persistence._delete(path), loop)
            else:
                loop.run_until_complete(Persistence._delete(path))
        except AssertionError:
            Persistence._delete(str(path))

    @staticmethod
    @asyncio.coroutine
    def _delete(path):
        os.remove(str(path))
