from pyccuracy.errors import *
from pyccuracy.actions.element_selector import *
from pyccuracy.actions.action_base import *
from pyccuracy.actions.element_is_visible_base import *

class ImageClickAction(ActionBase):
    def __init__(self, browser_driver, language):
        super(ImageClickAction, self).__init__(browser_driver, language)

    def matches(self, line):
        reg = self.language["image_click_regex"]
        self.last_match = reg.search(line)
        return self.last_match

    def values_for(self, line):
        return self.last_match and (self.last_match.groups()[1],) or tuple([])

    def execute(self, values, context):
        image_name = values[0]
        image = ElementSelector.image(image_name)

        self.assert_element_is_visible(image, self.language["image_is_visible_failure"] % image_name)		
        self.browser_driver.click_element(image)
