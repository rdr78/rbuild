#
# Copyright (c) SAS Institute Inc.
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
#


"""
show command and related utilities.
"""
from rbuild import pluginapi
from rbuild.pluginapi import command

class ShowCommand(command.CommandWithSubCommands):
    help = 'Shows details about the result of rbuild operations'

    commands = ['show']

class Show(pluginapi.Plugin):
    name = 'show'

    def registerCommands(self):
        self.handle.Commands.registerCommand(ShowCommand)

    def showJobStatus(self, jobId):
        self.handle.facade.rmake.displayJob(jobId)
