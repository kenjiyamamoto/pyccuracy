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

import unittest
import sys
import os
from os.path import abspath, join, split
sys.path.insert(0,os.path.abspath(__file__+"/../../"))
from pyccuracy.pyccuracy_core import *

class TestCustomActions(unittest.TestCase):

    def setUp(self):
        self.pyccuracy = PyccuracyCore()
                
    def test_search_google(self):
        custom_actions_dir = join(abspath(split(__file__)[0]), "custom_actions")
        self.pyccuracy.run_tests(custom_actions_dir=custom_actions_dir, file_pattern="test_custom_action.acc", should_throw=True, report_file_name = "customactionsreport.html")

if __name__ == "__main__":
    unittest.main()
