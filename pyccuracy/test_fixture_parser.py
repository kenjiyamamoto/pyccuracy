# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from locator import *
from test_fixture import *
import pyoc.reflection as reflection

class FileTestFixtureParser(object):
    def __init__(self, browser_driver, language, all_actions, all_custom_actions):
        self.language = language
        self.story_lines = (language["as_a"], language["i_want_to"], language["so_that"],)
        self.scenario_starter_lines = (language["scenario"],)
        self.scenario_lines = (language["given"], language["when"], language["then"],)
        self.browser_driver = browser_driver
        self.all_actions = all_actions
        self.all_custom_actions = all_custom_actions

    #helper methods for defining special cases
    def __is_story_line(self, line):
        return self.__is_special_item(line, self.story_lines)

    def __is_scenario_starter_line(self, line):
        return self.__is_special_item(line, self.scenario_starter_lines)

    def __is_scenario_line(self, line):
        return self.__is_special_item(line, self.scenario_lines)

    def __is_special_item(self, line, collection):
        for item in collection:
            if line.startswith(item):
                return 1
        return 0

    def get_fixture(self, files):
        fixture = TestFixture(self.language)
        for file_path in files:
            self.__process_file(fixture, file_path)
        return fixture

    def __process_file(self, fixture, file_path):
        try:
            content = unicode(open(file_path).read(), encoding='utf-8')
            lines = [line.strip() for line in content.split("\n") if len(line)]
        except IOError:
            fixture.add_invalid_test_file(file_path)
            return

        compiled_conditions_file = os.path.join(os.path.split(file_path)[0], os.path.splitext(file_path)[0] + ".pyc")
        conditions_file = os.path.join(os.path.split(file_path)[0], os.path.splitext(file_path)[0] + ".py")
        if os.path.exists(compiled_conditions_file):
            conditions_module = reflection.get_module_from_path(compiled_conditions_file)
        elif os.path.exists(conditions_file):
            conditions_module = reflection.get_module_from_path(conditions_file)
        else:
            conditions_module = None

        self.__process_lines(fixture, file_path, [line.strip() for line in lines if line.strip()], conditions_module)

    def __process_lines(self, fixture, file_path, lines, conditions_module):
        if not self.__is_story_line(lines[0]) \
               and not self.__is_story_line(lines[1]) \
               and not self.__is_story_line(lines[2]):

            fixture.add_no_story_definition(file_path)
        else:

            story = self.__process_story_lines(fixture, lines[0], lines[1], lines[2])
            story.conditions_module = conditions_module
            scenario = None

            for line in lines:
                if (self.__is_story_line(line)):
                    pass
                elif (self.__is_scenario_starter_line(line)):
                    scenario = self.__process_scenario_starter_line(fixture, story, line)
                elif (self.__is_scenario_line(line)):
                    action_under = self.__process_given_when_then_line(line)
                else:
                    if not scenario:
                        raise RuntimeError(self.language["no_scenario_line_error"] % line)
                    self.__process_action_line(file_path, fixture, scenario, action_under, line)

    def __process_story_lines(self, fixture, as_a, i_want_to, so_that):
        return fixture.start_story(as_a.replace(self.story_lines[0],""),
                                   i_want_to.replace(self.story_lines[1],""),
                                   so_that.replace(self.story_lines[2],""))

    def __process_scenario_starter_line(self, fixture, story, line):
        reg = self.language["scenario_starter_regex"]
        match = reg.search(unicode(line))
        try:
            values = match.groups()
        except AttributeError, e:
            raise RuntimeError(self.language["scenario_regex_match_error"] % (line, unicode(e)))

        scenario_index = values[0]
        scenario_title = values[1]
        scenario = story.start_scenario(scenario_index, scenario_title)
        return scenario

    def __process_given_when_then_line(self, line):
        if (line == self.language["given"]): return "given"
        if (line == self.language["when"]): return "when"
        if (line == self.language["then"]): return "then"

    def __process_action_line(self, file_path, fixture, scenario, action_under, line):
        method = getattr(scenario, "add_" + action_under)
        action = self.__get_action(line)
        if (action != None):
            method(line, action[0], action[1])
        else:
            if line.strip().startswith("#"):
                method(line, self.blank_execute, self.blank_values_for)
            else:
                raise InvalidScenarioError(self.language["invalid_scenario_error"] % (line, scenario.index, scenario.title, file_path))

    def blank_values_for(self, line):
        return tuple([])

    def blank_execute(self, values, context):
        pass

    def __get_action(self, line):
        if self.all_custom_actions:
            for action in self.all_custom_actions:
                action_name = action.__class__.__name__
                if action_name != "ActionBase" and action.matches(line):
                    return (action.execute, action.values_for(line))
        for action in self.all_actions:
            action_name = action.__class__.__name__
            if action_name != "ActionBase" and action.matches(line):
                return (action.execute, action.values_for(line))

        return None
