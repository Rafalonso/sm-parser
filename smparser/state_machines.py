from smparser.utils.helpers import pdfparser, strip_html_tags, goto_element
import re


class StateMachine:
    states = {}
    data = []

    def __init__(self, states, *args, **kwargs):
        for state in states:
            self[state.name] = state

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
                match = state.match(d)
                if match:
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
        dom = goto_element(xpath, dom)
        self.data = strip_html_tags(dom)
        super(HTMLStateMachine, self).__init__(states, *args, **kwargs)


class PDFStateMachine(TextStateMachine):
    def __init__(self, states, data, *args, **kwargs):
        self.data = pdfparser(data)
        super(PDFStateMachine, self).__init__(states, *args, **kwargs)


class State:
    def __init__(self, name, pattern, next_state=None):
        next_state = next_state or []
        self.name = name
        self.pattern = pattern
        self.next_state = next_state if isinstance(next_state, list) else [next_state]

    def match(self, text):
        return re.match(self.pattern, text)

    def next(self):
        return self.next_state
