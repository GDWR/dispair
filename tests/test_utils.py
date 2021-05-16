from dispair.utils import Colour, Color, Embed


def test_embed():
    title = 'An example Embed'
    desc = 'This be a description'
    embed = Embed(title, desc)

    assert embed.json() == {"title": title, "type": "rich", "description": desc, "color": 0}


def test_colour():
    colour = Colour(255, 0, 0)
    color = Color(255, 0, 0)

    assert colour.hex == color.hex
    assert colour.decimal == color.decimal
    assert colour.hex == color.hex
    assert colour.rgb == color.rgb


def test_decimal_colour():
    colour = Colour.from_hex("00FF00")

    assert colour.rgb == (0, 255, 0)
    assert colour.hex == '00FF00'
    assert colour.decimal == 255000

    colour = Colour.from_hex("#0000FF")

    assert colour.rgb == (0, 0, 255)
    assert colour.hex == '0000FF'
    assert colour.decimal == 255


def test_hex_colour():
    colour = Colour.from_decimal(255000)

    assert colour.rgb == (0, 255, 0)
    assert colour.hex == '00FF00'
    assert colour.decimal == 255000
