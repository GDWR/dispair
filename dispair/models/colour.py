from __future__ import annotations


class Colour:

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    @property
    def decimal(self) -> int:
        return int(f"{self.r:0>3}{self.g:0>3}{self.b:0>3}")

    @property
    def hex(self) -> str:
        return f"{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}".upper()

    @property
    def rgb(self) -> tuple[int, int, int]:
        return self.r, self.g, self.b

    @classmethod
    def from_hex(cls, hex_string: str) -> Colour:
        if hex_string[0] == '#':
            hex_string = hex_string[1:]

        assert len(hex_string) == 6, "Hex string does not match required size."

        r, g, b = hex_string[:2], hex_string[2:4], hex_string[4:]
        return cls(int(r, 16), int(g, 16), int(b, 16))

    @classmethod
    def from_decimal(cls, decimal: int) -> Colour:
        decimal = str(decimal).zfill(9)
        r, g, b = decimal[:3], decimal[3:6], decimal[6:]
        return cls(int(r), int(g), int(b))

    @classmethod
    def red(cls) -> Colour:
        return Colour(255, 0, 0)

    @classmethod
    def green(cls) -> Colour:
        return Colour(0, 255, 0)

    @classmethod
    def blue(cls) -> Colour:
        return Colour(0, 0, 255)
