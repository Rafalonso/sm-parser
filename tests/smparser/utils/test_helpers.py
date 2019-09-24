import os
import unittest

from smparser.utils.helpers import goto_element, emailparser
from mailparser import MailParser


class GoToElementTest(unittest.TestCase):
    def setUp(self):
        self.html = "<html><body><div><b>test</b></div></body></html>"

    def test_gets_element_with_current_dir(self):
        dom = goto_element(".//div", self.html)
        self.assertEqual(dom, '<div><b>test</b></div>')

    def test_gets_element_without_current_dir(self):
        dom = goto_element("//div", self.html)
        self.assertEqual(dom, '<div><b>test</b></div>')


class EmailTest(unittest.TestCase):
    def setUp(self):
        self.email_file_path = os.path.dirname(__file__) + '/../fixtures/booking.eml'

    def test_email_bytes(self):
        with open(self.email_file_path, 'rb') as f:
            booking = f.read()
        mail = emailparser(booking)
        self.assertEqual(type(mail), MailParser)

    def test_email_filename(self):
        mail = emailparser(self.email_file_path)
        self.assertEqual(type(mail), MailParser)

    def test_email_cant_handle_other_types(self):
        with self.assertRaises(TypeError):
            emailparser(123)
