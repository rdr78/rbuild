#
# Copyright (c) 2008 rPath, Inc.
#
# This program is distributed under the terms of the Common Public License,
# version 1.0. A copy of this license should have been distributed with this
# source file in a file called LICENSE. If it is not present, the license
# is always available at http://www.rpath.com/permanent/licenses/CPL-1.0.
#
# This program is distributed in the hope that it will be useful, but
# without any warranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the Common Public License for
# full details.
#

from rbuild import pluginapi
from rbuild.pluginapi import command

from rbuild_plugins.build import groups

class BuildGroupsCommand(command.BaseCommand):
    docs = {'no-watch' : 'do not watch the job after starting the build',
            'no-commit' : 'do not automatically commit successful builds',}
    help = 'build groups for this stage'

    def addParameters(self, argDef):
        argDef['no-watch'] = command.NO_PARAM
        argDef['no-commit'] = command.NO_PARAM

    #pylint: disable-msg=R0201,R0903
    # could be a function, and too few public methods
    def runCommand(self, handle, argSet, args):
        watch = not argSet.pop('no-watch', False)
        commit = not argSet.pop('no-commit', False)
        _, groupList, = self.requireParameters(args, allowExtra=True)
        if not groupList:
            jobId = handle.BuildGroups.buildAllGroups()
        else:
            jobId = handle.BuildGroups.buildGroups(groupList)
        if watch and commit:
            handle.Build.watchAndCommitJob(jobId)
        elif watch:
            handle.Build.watchJob(jobId)


class BuildGroups(pluginapi.Plugin):

    def initialize(self):
        self.handle.Commands.getCommandClass('build').registerSubCommand(
                                    'groups', BuildGroupsCommand)

    def buildAllGroups(self):
        job = self.createJobForAllGroups()
        jobId = self.handle.facade.rmake.buildJob(job)
        self.handle.getProductStore().setGroupJobId(jobId)
        return jobId

    def buildGroups(self, groupList):
        job = self.createJobForGroups(groupList)
        jobId = self.handle.facade.rmake.buildJob(job)
        self.handle.getProductStore().setGroupJobId(jobId)
        return jobId

    def createJobForAllGroups(self):
        return groups.createRmakeJobForAllGroups(self.handle)

    def createJobForGroups(self, groupList):
        return groups.createRmakeJobForGroups(self.handle, groupList)
