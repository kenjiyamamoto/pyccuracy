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

class Page(object):
    '''Class that defines a page model.'''

    Button = "button"
    Checkbox = "checkbox"
    Div = "div"
    Image = "image"
    Link = "link"
    Page = "page"
    RadioButton = "radio_button"
    Select = "select"
    Textbox = "textbox"

    def __init__(self):
        '''Initializes the page with the given url.'''
        self.registered_elements = {}
        if hasattr(self, "register"): self.register()

    def get_registered_element(self, element_type, element_key):
        if not element_type in self.registered_elements: 
            return None
        if not element_key in self.registered_elements[element_type]: 
            return None
        return self.registered_elements[element_type][element_key]

    def get_registered_element_by_key_only(self, element_key):
        for element_type in self.registered_elements.keys():
            if element_key in self.registered_elements[element_type]:
                return self.registered_elements[element_type][element_key]
        
        return None

    def register_button(self, button_key, button_locator):
        self.register_element(Page.Button, button_key, button_locator)

    def register_checkbox(self, checkbox_key, checkbox_locator):
        self.register_element(Page.Checkbox, checkbox_key, checkbox_locator)

    def register_div(self, div_key, div_locator):
        self.register_element(Page.Div, div_key, div_locator)

    def register_image(self, image_key, image_locator):
        self.register_element(Page.Image, image_key, image_locator)

    def register_link(self, link_key, link_locator):
        self.register_element(Page.Link, link_key, link_locator)

    def register_radio_button(self, radio_button_key, radio_button_locator):
        self.register_element(Page.RadioButton, radio_button_key, radio_button_locator)

    def register_select(self, select_key, select_locator):
        self.register_element(Page.Select, select_key, select_locator)

    def register_textbox(self, textbox_key, textbox_locator):
        self.register_element(Page.Textbox, textbox_key, textbox_locator)

    def register_element(self, element_type, element_key, element_locator):
        if not element_type in self.registered_elements: 
            self.registered_elements[element_type] = {}
            
        self.registered_elements[element_type][element_key] = element_locator

