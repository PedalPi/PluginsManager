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

import logging
import jack


class JackClient(object):
    """
    Based in: http://jackclient-python.readthedocs.io/en/0.4.2/examples.html#chatty-client

    Through the :class:`jack.JackClient` it is possible to be notified when `x-run`
    occurs and when the Jack server is closed::

        >>> client = JackClient()
        >>> client.xrun_callback = lambda delay: print('x-run', delay)
        >>> client.shutdown_callback = lambda status, reason: print('shutdown: ', status, reason)

    When you don't use anymore, close it::

        >>> client.close()

    :param bool no_start_server: False if starts a new JACK server
                                 True if uses a already started jack (ex: using `jackdump`)
    :param name: Jack client name. Default: `JackClient`
    """
    def __init__(self, no_start_server=True, name=None):
        if name is None:
            name = self.__class__.__name__

        self.client = jack.Client(name=name, no_start_server=no_start_server)

        self.xrun_callback = lambda delay: ...
        self.shutdown_callback = lambda status, reason: ...

        if self.client.status.server_started:
            logging.info('JACK server was started')
        else:
            logging.info('JACK server was already running')

        if self.client.status.name_not_unique:
            logging.info('Unique client name generated {}'.format(self.client.name))

        @self.client.set_xrun_callback
        def xrun(delay):
            self.xrun_callback(delay)

        @self.client.set_shutdown_callback
        def shutdown(status, reason):
            self.shutdown_callback(status, reason)

        self.client.activate()

    @property
    def audio_inputs(self):
        """
        :return: A list of audio input :class:`Ports`.
        """
        return self.client.get_ports(is_audio=True, is_physical=True, is_input=True)

    @property
    def audio_outputs(self):
        """
        :return: A list of audio output :class:`Ports`.
        """
        return self.client.get_ports(is_audio=True, is_physical=True, is_output=True)

    @property
    def midi_inputs(self):
        """
        :return: A list of MIDI input :class:`Ports`.
        """
        return self.client.get_ports(is_midi=True, is_physical=True, is_input=True)

    @property
    def midi_outputs(self):
        """
        :return: A list of MIDI output :class:`Ports`.
        """
        return self.client.get_ports(is_midi=True, is_physical=True, is_output=True)

    def close(self):
        """
        Deactivate and closes the jack client
        """
        self.client.deactivate()
        self.client.close()
