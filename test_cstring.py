import pytest

from cstring import CString, FromVecWithNulError, IntoStringError, NulError


def test_new():
    with pytest.raises(NulError):
        CString.new("foo\0")

    with pytest.raises(NulError):
        CString.new("fo\0o")

    with pytest.raises(NulError):
        CString.new("fo\0o\0")

    assert CString.new("foo") == CString.new(b"foo")
    assert CString.new(b"foo") == CString.new(bytearray(b"foo"))
    assert CString.new(bytearray(b"foo")) == CString.new("foo")


def test_into_string():
    c_string = CString.new(bytearray(b"foo"))
    assert c_string.into_string() == "foo"

    # hacking inner bytearray
    inner = c_string._inner
    inner.pop()
    inner.append(128)
    inner.append(0)
    c_string._inner = inner
    with pytest.raises(IntoStringError):
        c_string.into_string()


def test_into_bytes():
    assert CString.new("foo").into_bytes() == bytearray(b"foo")


def test_into_bytes_with_nul():
    bytearray_with_nul = CString.new("foo").into_bytes_with_nul()
    assert bytearray_with_nul == bytearray(b"foo\0")
    assert bytearray_with_nul[-1] == 0


def test_as_bytes():
    c_string_as_bytes = CString.new("foo").as_bytes()
    assert c_string_as_bytes == b"foo"
    assert len(c_string_as_bytes) == 3


def test_as_bytes_with_nul():
    bytes_with_nul = CString.new("foo").as_bytes_with_nul()
    assert bytes_with_nul == b"foo\0"
    assert bytes_with_nul[-1] == 0


def test_from_vec_with_nul_unchecked():
    assert CString.from_vec_with_nul_unchecked(
        bytearray(b"abc\0")
    ) == CString.from_vec_unchecked(bytearray(b"abc"))


def test_from_vec_with_nul():
    with pytest.raises(FromVecWithNulError):
        CString.from_vec_with_nul(bytearray(b"abc"))

    with pytest.raises(FromVecWithNulError):
        CString.from_vec_with_nul(bytearray(b"ab\0c\0"))

    with pytest.raises(FromVecWithNulError):
        CString.from_vec_with_nul(bytearray(b"ab\0c"))

    assert CString.from_vec_with_nul(bytearray(b"abc\0")) == CString.new(
        bytearray(b"abc")
    )
    assert CString.from_vec_with_nul(bytearray(b"abc\0")) == CString.new("abc")


def test_repr():
    assert repr(CString.new("foo")) == repr("foo")
