from smparser.utils.helpers import pdfparser, emailparser, goto_and_strip_html
import logging
import re


logger = logging.getLogger()


class StateMachine:
    states = {}
    data = []

    def __init__(self, states, debug=False, *args, **kwargs):
        self.states = states
        if debug:
            logger.setLevel('DEBUG')

    def __setattr__(self, key, value):
        if key == 'states':
            for v in value:
                self[v.name] = v
        else:
            super().__setattr__(key, value)

    def __setitem__(self, key, value):
        self.states[key] = value

    def __getitem__(self, item):
        if isinstance(item, State):
            return item
        return self.states[item]

    def runAll(self, first_state):
        return [m for m in self._runAll(first_state)]

    def _runAll(self, first_state):
        states = [first_state]
        for d in self.data:
            for state in states:
                state = self[state]
                logger.debug(f"STATE: '{state.name}' | DATA: '{d}'")
                match = state.match(d)
                if match is not None:
                    yield match
                    states = state.next()
                    break


class TextStateMachine(StateMachine):
    def __init__(self, states, *args, **kwargs):
        super(TextStateMachine, self).__init__(states, *args, **kwargs)
        self.data = self.data.split('\n')


class HTMLStateMachine(TextStateMachine):
    def __init__(self, states, filename=None, dom=None, xpath='.', *args, **kwargs):
        if all([filename, dom]) or not any([filename, dom]):
            raise ValueError("Only 'filename' or 'dom' needs to be passed as argument.")

        if filename:
            with open(filename, 'rb') as f:
                dom = f.read()
        self.data = goto_and_strip_html(dom, xpath)
        super(HTMLStateMachine, self).__init__(states, *args, **kwargs)


class PDFStateMachine(TextStateMachine):
    def __init__(self, states, data, *args, **kwargs):
        self.data = pdfparser(data)
        super(PDFStateMachine, self).__init__(states, *args, **kwargs)


class MailStateMachine(HTMLStateMachine):
    def __init__(self, states, email_file, *args, **kwargs):
        self._email = emailparser(email_file)
        super().__init__(states, dom=''.join(self._email.text_html), *args, **kwargs)


class State:
    def __init__(self, name, pattern, next_state=None):
        next_state = next_state or []
        self.name = name
        self.pattern = pattern
        self.next_state = next_state if isinstance(next_state, list) else [next_state]

    def match(self, text):
        logger.debug(f'PATTERN: {self.pattern} | DATA: {text}')
        matched = re.match(self.pattern, text)
        return matched.groups() if matched else None

    def next(self):
        return self.next_state
