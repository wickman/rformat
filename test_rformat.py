import string

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


def test_custom_formatter():
  def iterable_formatter(value, format_spec):
    if isinstance(value, (list, tuple, dict)):
      return ','.join(format(v) for v in value)
    else:
      return format(value, format_spec)

  subnets = {'subnet-one': 'one', 'subnet-two': 'two'}

  # unwraps iterable
  formatter = rformat.RecursiveFormatter(formatter=iterable_formatter)
  assert formatter.format('{subnets}', subnets=subnets) in (
      'subnet-one,subnet-two', 'subnet-two,subnet-one')

  # leaves iterable alone
  formatter = string.Formatter()
  assert formatter.format('{subnets}', subnets=subnets) == repr(subnets)
