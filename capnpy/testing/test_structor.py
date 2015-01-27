from capnpy.structor import structor, compute_format
from capnpy import field
from capnpy.type import Types

class FakeBlob(object):

    @classmethod
    def from_buffer(cls, buf, offset, segment_offsets):
        return buf



def test_compute_format_simple():
    fields = [field.Primitive(0, Types.int64),
              field.Primitive(8, Types.int64)]
    fmt = compute_format(data_size=2, ptrs_size=0, fields=fields)
    assert fmt == 'qq'

def test_compute_format_holes():
    fields = [field.Primitive(0, Types.int32),
              field.Primitive(8, Types.int64)]
    fmt = compute_format(data_size=2, ptrs_size=0, fields=fields)
    assert fmt == 'ixxxxq'


def test_simple():
    fields = [field.Primitive(0, Types.int64),
              field.Primitive(8, Types.int64)]
    ctor = structor('ctor', data_size=2, ptrs_size=0, fields=fields)
    buf = ctor(FakeBlob, 1, 2)
    assert buf == ('\x01\x00\x00\x00\x00\x00\x00\x00'  # 1
                   '\x02\x00\x00\x00\x00\x00\x00\x00') # 2

def test_string():
    fields = [field.Primitive(0, Types.int64),
              field.String(8)]
    ctor = structor('ctor', data_size=1, ptrs_size=1, fields=fields)
    buf = ctor(FakeBlob, 1, 'hello capnp')
    assert buf == ('\x01\x00\x00\x00\x00\x00\x00\x00'
                   '\x01\x00\x00\x00\x62\x00\x00\x00'
                   'h' 'e' 'l' 'l' 'o' ' ' 'c' 'a'
                   'p' 'n' 'p' '\x00\x00\x00\x00\x00')
