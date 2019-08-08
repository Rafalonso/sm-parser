import os
import unittest
from unittest.mock import Mock, MagicMock

from smparser.state_machines import StateMachine, HTMLStateMachine, PDFStateMachine, State


class StateMachineTest(unittest.TestCase):
    def setUp(self):
        self.state = State('state1', r'$')
        self.statemachine = StateMachine([self.state])

    def test_statemachine_get_state(self):
        self.assertEqual(self.statemachine['state1'], self.state)

    def test_statemachine_get_state_not_exists(self):
        with self.assertRaises(KeyError):
            self.statemachine[' ']

    def test_change_to_next_state(self):
        next_state = State('state2', r'$')
        next_state.match = MagicMock()
        self.statemachine['state2'] = next_state
        self.state.next_state = ['state2']
        self.statemachine.data = ['', '']

        self.statemachine.runAll(self.state)
        next_state.match.assert_called()

    def test_not_change_to_next_state(self):
        next_state = State('state2', r'$')
        next_state.match = MagicMock()
        self.statemachine['state2'] = next_state
        self.state.next_state = ['state2']
        self.statemachine.data = ['a', 'a']

        self.statemachine.runAll(self.state)
        next_state.match.assert_not_called()


class HTMLStateMachineTest(unittest.TestCase):
    def setUp(self):
        self.state = Mock()
        self.state.name = ''
        self.html_document = os.path.dirname(__file__) + '/fixtures/document.html'

    def test_pass_filename_and_dom(self):
        with self.assertRaises(ValueError):
            HTMLStateMachine([self.state], filename='', dom=b'')

    def test_pass_nothing(self):
        with self.assertRaises(ValueError):
            HTMLStateMachine([self.state])

    def test_dom_strips_html(self):
        state_machine = HTMLStateMachine([self.state], dom='<html><head></head><body>test</body></html>')
        self.assertEqual(state_machine.data, ['test'])

    def test_filename_strips_html(self):
        state_machine = HTMLStateMachine([self.state], filename=self.html_document)
        self.assertEqual(state_machine.data, ['test'])


class PDFStateMachineTest(unittest.TestCase):
    def setUp(self):
        self.state = Mock()
        self.state.name = ''
        self.pdf_document = os.path.dirname(__file__)+'/fixtures/document.pdf'

    def test_pass_filename(self):
        state_machine = PDFStateMachine([self.state], self.pdf_document)
        self.assertEqual(type(state_machine.data), list)

    def test_pass_bytes(self):
        with open(self.pdf_document, 'rb') as f:
            pdf_in_bytes = f.read()
        state_machine = PDFStateMachine([self.state], pdf_in_bytes)
        self.assertEqual(type(state_machine.data), list)

