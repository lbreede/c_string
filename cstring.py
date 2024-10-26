from __future__ import annotations

from result import Err, Ok, Result


class NulError(Exception):
    def __init__(self, nul_position: int, data: bytearray) -> None:
        super().__init__(f"{nul_position}, {[x for x in data]}")
        self.nul_position = nul_position
        self.data = data


class FromVecWithNulError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class IntoStringError(Exception):
    def __init__(self) -> None:
        super().__init__("")


class CString:
    def __init__(self, inner: bytearray) -> None:
        self._inner = inner

    @classmethod
    def new(cls, t: bytearray | bytes | str) -> Result[CString, NulError]:
        if isinstance(t, bytes):
            t = bytearray(t)
        elif isinstance(t, str):
            t = bytearray(t.encode())

        if 0 in t:
            return Err(NulError(t.index(0), t))
        return Ok(cls.from_vec_unchecked(t))

    @classmethod
    def from_vec_unchecked(cls, v: bytearray) -> CString:
        v.append(0)
        return cls(v)

    def into_string(self) -> Result[str, UnicodeDecodeError]:
        try:
            return Ok(self._inner[:-1].decode())
        except UnicodeDecodeError as e:
            return Err(e)

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
    def from_vec_with_nul(cls, v: bytearray) -> Result[CString, str]:
        # TODO: Properly wrap the error in Err
        if v[-1] != 0:
            return Err("FromVecWithNulError")

        if v.count(0) > 1:
            return Err("FromVecWithNulError")

        return Ok(cls(v))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CString):
            return False
        return self.as_bytes_with_nul() == other.as_bytes_with_nul()

    def __repr__(self) -> str:
        return repr(self.into_string().unwrap())


def main() -> None:
    c_string = CString.from_vec_with_nul(bytearray("foo\0".encode()))
    print(c_string)

    string = c_string.into_string()
    print(string)


if __name__ == "__main__":
    main()
