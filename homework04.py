# bencoding
# http://www.bittorrent.org/beps/bep_0003.html

"""
Strings are length-prefixed base ten followed by a colon and the string.
For example 4:spam corresponds to 'spam'.

>>> encode(b'spam')
b'4:spam'

Integers are represented by an 'i' followed by the number in base 10 followed by an 'e'.
For example i3e corresponds to 3 and i-3e corresponds to -3.
Integers have no size limitation. i-0e is invalid.
All encodings with a leading zero, such as i03e, are invalid,
other than i0e, which of course corresponds to 0.

>>> decode(b'i3e')
3
>>> decode(b'i-3e')
-3
>>> decode(b'i0e')
0
>>> decode(b'i03e')
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 0: '03'
 

Lists are encoded as an 'l' followed by their elements (also bencoded) followed by an 'e'.
For example l4:spam4:eggse corresponds to ['spam', 'eggs'].

>>> decode(b'l4:spam4:eggse')
[b'spam', b'eggs']

Dictionaries are encoded as a 'd' followed by a list of alternating keys
and their corresponding values followed by an 'e'.
For example, d3:cow3:moo4:spam4:eggse corresponds to {'cow': 'moo', 'spam': 'eggs'}
Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics).

>>> decode(b'd3:cow3:moo4:spam4:eggse')
OrderedDict([(b'cow', b'moo'), (b'spam', b'eggs')])

"""
from collections import OrderedDict

def encode(val):

    if isinstance(val, str):
        return bytes(str(len(val)) + ':' + val, 'utf-8')
    elif isinstance(val, bytes):
        val = val.decode("utf-8")
        return bytes(str(len(val)) + ':' + val, 'utf-8')
    elif isinstance(val, int):
        return bytes('i:' + str(val) +'e', 'utf-8')
    elif isinstance(val, list):
        return bytes('l:' + ':'.join([item for item in val]), 'utf-8')
    elif isinstance(val, (dict, OrderedDict)):
        return bytes('d' + ''.join([str(len(k)) + ':' + k  + \
                                    str(len(v)) + ':' + v for k, v in val.items()]), 'utf-8')
    else:
        raise Exception('Unsupported data type')


def decode(val):
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    else:
        raise Exception('Unsupported data type')

    if val[0].lower() == 'i':
        return decode_int(val)

def decode_int(val):
    pos = 1
    pos2 = val.index('e', pos)
    num = int(val[pos:pos2])
    if val[pos] == '-':
        if val[pos + 1] == '0':
            raise ValueError
    elif val[pos] == '0' and pos2 != pos + 1:
        raise ValueError
    return num


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
