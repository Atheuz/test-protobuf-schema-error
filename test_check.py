from common.terms_pb2 import TermSource
from google.protobuf.internal import api_implementation


def test_term():
    print(api_implementation.Type())

    a = TermSource.TERM_SOURCE_UNSPECIFIED
    assert a == 0
