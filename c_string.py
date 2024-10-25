from __future__ import annotations


class NulError(Exception):
    def __init__(self, nul_position: int, data: bytearray) -> None:
        super().__init__(f"{nul_position}, {[x for x in data]}")
        self.nul_position = nul_position
        self.data = data


class FromVecWithNulError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CString:
    def __init__(self, inner: bytearray) -> None:
        self._inner = inner

    @classmethod
    def new(cls, t: bytearray | bytes | str) -> CString:
        if isinstance(t, bytes):
            t = bytearray(t)
        elif isinstance(t, str):
            t = bytearray(t.encode())

        if 0 in t:
            raise (NulError(t.index(0), t))
        return cls.from_vec_unchecked(t)

    @classmethod
    def from_vec_unchecked(cls, v: bytearray) -> CString:
        v.append(0)
        return cls(v)

    def into_string(self) -> str:
        return self._inner[:-1].decode()

    def into_bytes(self) -> bytearray:
        return self.into_bytes_with_nul()[:-1]

    def into_bytes_with_nul(self) -> bytearray:
        return self._inner

    def as_bytes(self) -> bytes:
        return self.as_bytes_with_nul()[:-1]

    def as_bytes_with_nul(self) -> bytes:
        return bytes(self._inner)

    @classmethod
    def from_vec_with_nul_unchecked(cls, v: bytearray) -> CString:
        return cls(v)

    @classmethod
    def from_vec_with_nul(cls, v: bytearray) -> CString:
        if v[-1] != 0:
            raise FromVecWithNulError("the last element must be a nul byte")

        if v.count(0) > 1:
            raise FromVecWithNulError("there are more than one nul byte")

        return cls(v)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CString):
            return False
        return self.as_bytes_with_nul() == other.as_bytes_with_nul()

    def __repr__(self) -> str:
        return repr(self.into_string())


def main() -> None:
    a = CString(bytearray(b"foo\0"))
    b = CString.new("foo")
    c = CString.from_vec_unchecked(bytearray(b"foo"))
    d = CString.from_vec_with_nul_unchecked(bytearray(b"foo\0"))
    e = CString.from_vec_with_nul(bytearray(b"foo\0"))

    print(a._inner)
    print(b._inner)
    print(c._inner)
    print(d._inner)
    print(e._inner)


if __name__ == "__main__":
    main()
