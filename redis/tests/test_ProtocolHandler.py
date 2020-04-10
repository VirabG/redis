from .. import ProtocolHandler
from ..ProtocolHandler import LINE_SEPARATOR

handler = ProtocolHandler.ProtocolHandler()


def test():
    print(bytes)


def test_string_deserialization():
    serialized = "+OK" + LINE_SEPARATOR
    actual = handler.deserialize_string(serialized)
    expected = "OK"
    assert(actual == expected)


def test_string_serialization():
    input = "OK"
    actual = handler.serialize_string(input)
    expected = "+OK" + LINE_SEPARATOR
    assert(actual == expected)


def test_integer_deserialization():
    serialized = ":111" + LINE_SEPARATOR
    actual = handler.deserialize_integer(serialized)
    expected = 111
    assert(actual == expected)


def test_integer_serialization():
    input = 111
    actual = handler.serialize_integer(input)
    expected = ":111" + LINE_SEPARATOR
    assert(actual == expected)


# def test_error_deserialization():
#     serialized = "-I am an error" + LINE_SEPARATOR
#     actual = handler.deserialize_error(serialized)
#     expected = "I am an error"
#     assert (actual == expected)


# def test_error_serialization():
#     input = "I am an error"
#     actual = handler.serialize_error(input)
#     expected = "-I am an error" + LINE_SEPARATOR
#     assert (actual == expected)


def test_binary_serialization_deserialization():
    input = bytearray('abcd', 'ascii')
    serialized = handler.serialize_binary(input)
    deserialized = handler.deserialize_binary(serialized)
    assert (input == deserialized)

    input = bytearray([0, 10, 48, 97])
    serialized = handler.serialize_binary(input)
    deserialized = handler.deserialize_binary(serialized)
    assert (input == deserialized)


def test_array_serialization_deserialization():
    binary_string = bytearray("abcd", 'ascii')
    a = [2, "Hello World", 4, binary_string, 5]
    serialized = handler.serialize_array(a)
    deserialized = handler.deserialize_array(serialized)
    assert (a == deserialized)

    empty_array = []
    serialized_empty = handler.serialize_array(empty_array)
    deserialized_empty = handler.deserialize_array(serialized_empty)
    assert (empty_array == deserialized_empty)


def test_dictionary_serialization_deserialization():
    d = {}
    serialized_empty = handler.serialize_dictionary(d)
    deserialized_empty = handler.deserialize_dictionary(serialized_empty)
    assert (d == deserialized_empty)

    binary_string = bytearray('abcd', 'ascii')
    d['first_entry'] = 4
    d[2] = binary_string
    d['third_entry'] = [2, "Hello World", 4, binary_string, 5]
    serialized = handler.serialize_dictionary(d)
    deserialized = handler.deserialize_dictionary(serialized)
    assert (d == deserialized)
