from dispair import Embed


def test_embed():
    title = 'An example Embed'
    desc = 'This be a description'
    embed = Embed(title, desc)

    assert embed.json() == {"title": title, "type": "rich", "description": desc, "color": 0}
