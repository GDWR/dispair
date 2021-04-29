import random
from dispair import Router, Response, Interaction


router = Router()


@router.interaction("8ball", "Let the 8ball take the wheel")
async def _8ball(inter: Interaction) -> Response:
    answer = random.choice(["Yes", "No", "Maybe"])
    return Response(content=f"> {answer}")
