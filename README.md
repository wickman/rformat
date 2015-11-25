rformat is a recursive version of str.format

for example:
```python

import rformat

lastnames = {
  'john': 'smith',
  'jane': 'doe',
}

print(rformat.format('hello {name} {lastnames[{name}]}', name='john', lastnames=lastnames))
hello john smith
```
