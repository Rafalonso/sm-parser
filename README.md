# STATE MACHINE PARSER

Parser that searches data rather than fields.

## Examples 

Parse by HTML

```html
<html>
    <head>
    </head>
    <body>
        <p>Saturday, 31 August 2019</p>
        $33.8
        <br/>
        Rafael Alonso
        <a>Rating: 7/10</a>
    </body>
</html>
```

Parsing html page:

```python
from smparser import HTMLStateMachine, State

states = [
    State('date', r'.*?([0-9]{1,2}\s[A-Z][a-z]+\s[0-9]{4})', next_state='price'),
    State('price', r'.*?\$?\s*((\d{1,3}(,\d{3})+|\d+)(\.(\d\d?)))', next_state='rating'),
    State('rating', r'.*?Rating:\s*(\d+)/10'),
]
print(HTMLStateMachine(states, html_code).runAll('date'))
```

Output:
```text
[
    ('31 August 2019',), 
    ('33.8', '33', None, '.8', '8'), 
    ('7',)
]
```