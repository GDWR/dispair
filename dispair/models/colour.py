from __future__ import annotations


class Colour:
    """Colour Utility to handle decimal, hex and rgb."""

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    @property
    def decimal(self) -> int:
        """Return the decimal representation of the colour."""
        return int(f"{self.r:0>3}{self.g:0>3}{self.b:0>3}")

    @property
    def hex(self) -> str:
        """Return the hex representation of the colour."""
        return f"{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}".upper()

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Return the (r,g,b) representation of the colour."""
        return self.r, self.g, self.b

    @classmethod
    def from_hex(cls, hex_string: str) -> Colour:
        """Create a Colour object from a hex string."""
        if hex_string[0] == '#':
            hex_string = hex_string[1:]

        assert len(hex_string) == 6, "Hex string does not match required size."

        r, g, b = hex_string[:2], hex_string[2:4], hex_string[4:]
        return cls(int(r, 16), int(g, 16), int(b, 16))

    @classmethod
    def from_decimal(cls, decimal: int) -> Colour:
        """Create a Colour object from a decimal value."""
        decimal = str(decimal).zfill(9)
        r, g, b = decimal[:3], decimal[3:6], decimal[6:]
        return cls(int(r), int(g), int(b))

    @classmethod
    def red(cls) -> Colour:
        """Pre-made Red Colour #FF0000, (255, 0, 0), 255000000."""
        return Colour(255, 0, 0)

    @classmethod
    def green(cls) -> Colour:
        """Pre-made Green Colour #00FF00, (0, 255, 0), 255000."""
        return Colour(0, 255, 0)

    @classmethod
    def blue(cls) -> Colour:
        """Pre-made Blue Colour #0000FF, (0, 0, 255), 255."""
        return Colour(0, 0, 255)
