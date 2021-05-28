import random
from typing import Optional

from dispair import Router
from dispair.models import Interaction, Option, Member
from dispair.utils import Embed

router = Router()


@router.interaction(name="8ball", description="Let the 8ball take the wheel", _global=False,
                    guilds=[566407576686952480])
async def _8ball(inter: Interaction):
    answer = random.choice(["Yes", "No", "Maybe"])
    return f"> {answer}"


@router.interaction(name="uwuify", description="Uwuify a Message.", _global=False, guilds=[566407576686952480])
async def uwuify(inter: Interaction, text: str):
    UWU_WORDS = {
        "fi": "fwi",
        "l": "w",
        "r": "w",
        "some": "sum",
        "th": "d",
        "thing": "fing",
        "tho": "fo",

        "you're": "yuw'we",
        "your": "yur",
        "you": "yuw",
    }

    for find, convert in UWU_WORDS.items():
        try:
            if i := text.index(find):
                text = text[:i] + convert + text[i + len(find):]
        except ValueError:
            continue

    return f">>> {text}"


@router.interaction(name="owoify", description="Owoify a Message.", _global=False, guilds=[566407576686952480])
async def owoify(inter: Interaction, text: str = Option(desc='Text to Owoify')):
    OWO_WORDS = {
        "m": "mw",
        "your": "ywour",
        "of": "owf",
        "cute": "cwute",
        "as": "aws",
        "this": "dis",
        "may": "mway",
        "wanna": "wawna",
    }

    for find, convert in OWO_WORDS.items():
        try:
            if i := text.index(find):
                text = text[:i] + convert + text[i + len(find):]
        except ValueError:
            continue

    return f">>> {text}"


@router.interaction(name="embed", description="Embed your message.", _global=False, guilds=[566407576686952480])
async def embed(inter: Interaction,
                title: str = Option(desc="Title for the embed"),
                description: Optional[str] = Option(desc="Embed Description")):
    return Embed(title=title, description=description)


@router.interaction(name="GuessTheNumber", description="See if you can guess the number, Between (1 - 20)",
                    _global=False, guilds=[566407576686952480])
async def guess_the_number(inter: Interaction, guess: int = Option(desc="Guess the number")):
    if 0 >= guess or guess >= 20:
        return "> Please make your guess between 1 - 20"

    random_num = random.randint(1, 21)
    if random_num == guess:
        return "> You guessed the number!"
    else:
        return f"> You didn't guess the number, it was {random_num}"


@router.interaction(name="Boolean", description="Example of a boolean Input", _global=False,
                    guilds=[566407576686952480])
async def boolean_example(inter: Interaction, guess: bool = Option(desc="Input")):
    return guess


@router.interaction(name="Mention", description="Mention a user", _global=False, guilds=[566407576686952480])
async def mention(inter: Interaction, user: Optional[Member] = Option(desc="Member to get the ID of")):
    user = user or inter.author
    return user.mention
