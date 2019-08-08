import unittest

from smparser.utils.helpers import goto_element


class GoToElementTest(unittest.TestCase):
    def setUp(self):
        self.html = "<html><body><div><b>test</b></div></body></html>"

    def test_gets_element_with_current_dir(self):
        dom = goto_element(".//div", self.html)
        self.assertEqual(dom, '<div><b>test</b></div>')

    def test_gets_element_without_current_dir(self):
        dom = goto_element("//div", self.html)
        self.assertEqual(dom, '<div><b>test</b></div>')
