import os
import unittest
from unittest.mock import Mock, MagicMock

from smparser.state_machines import StateMachine, HTMLStateMachine, PDFStateMachine, State, MailStateMachine


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


class EmailStateMachineTest(unittest.TestCase):
    def setUp(self):
        email_file = os.path.dirname(__file__) + '/fixtures/booking.eml'
        self.state_machine = MailStateMachine([], email_file)

    def test_pass_email_has_dom(self):
        self.assertTrue(len(self.state_machine.data) > 20)

    def test_meta_fields(self):
        email_headers = ['Delivered-To', 'Received', 'X-Google-Smtp-Source', 'X-Received', 'ARC-Seal',
                         'ARC-Message-Signature', 'ARC-Authentication-Results', 'Return-Path', 'Received-SPF',
                         'Authentication-Results', 'Content-Transfer-Encoding', 'DKIM-Signature', 'Content-Type',
                         'MIME-Version', 'Date', 'To', 'Sender', 'Reply-To', 'Subject', 'From', 'X-Bme-Id',
                         'Message-Id']

        self.assertEqual(self.state_machine._email.attachments, [])
        self.assertEqual(self.state_machine._email.from_, [('Orange Wings Wiener Neustadt',
                                                            'customer.service@booking.com')])
        self.assertEqual(self.state_machine._email.delivered_to, [('', 'rafalonso.almeida@gmail.com')])
        self.assertEqual(self.state_machine._email.to, [('', 'rafalonso.almeida@gmail.com')])
        self.assertListEqual(list(self.state_machine._email.headers.keys()), email_headers)
        self.assertEqual(self.state_machine._email.subject,
                         '🛄 Thanks! Your booking is confirmed at Orange Wings Wiener Neustadt')
        self.assertEqual(str(self.state_machine._email.date), '2019-08-31 16:05:09')

    def test_parse_email_fields(self):
        date_regex = r'.*?([0-9]{1,2}\s[A-Z][a-z]+\s[0-9]{4})'
        check_in_state = State('check_in', date_regex, next_state='check_out')
        check_out_state = State('check_out', date_regex)
        self.state_machine.states = [check_in_state, check_out_state]
        machine_run = self.state_machine.runAll('check_in')
        self.assertEqual(machine_run[0][0], '31 August 2019')
        self.assertEqual(machine_run[1][0], '1 September 2019')
