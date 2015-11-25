import rformat

import pytest


def test_basic_format():
  assert 'foo' == rformat.format('foo')

  lastnames = {'john': 'smith', 'jane': 'doe'}
  assert 'hello john smith' == rformat.format(
      'hello {name} {lastnames[{name}]}', name='john', lastnames=lastnames)
  assert 'hello jane doe' == rformat.format(
      'hello {name} {lastnames[{name}]}', name='jane', lastnames=lastnames)


def test_exceptions():
  with pytest.raises(KeyError):
    rformat.format('hello {name} {lastnames[{name}]}', name='frank', lastnames={})

  with pytest.raises(IndexError):
    rformat.format('hello {names[{index}]}', index=0, names=[])

  with pytest.raises(TypeError):
    rformat.format('hello {names[{index}]}', index="hello", names=[])


def test_cycles():
  with pytest.raises(rformat.DepthExceeded):
    rformat.format('{names[{index}]}', index='john', names={'john': '{names[{index}]}'})
