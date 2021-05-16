from json import loads
import pytest
from dispair import Router
from dispair.models import Interaction, Option, Response

from stubs.client_stub import ClientStub


@pytest.fixture(scope="function")
async def client() -> ClientStub:
    client = ClientStub()
    client.run()
    yield client
    await client.kill()


@pytest.mark.asyncio
async def test_router(client: ClientStub):
    router = Router()
    client.attach_router(router)
    assert len(client._routers) > 0


@pytest.mark.asyncio
async def test_router_command(client: ClientStub):
    router = Router()
    message = "> This is working"

    @router.interaction("test", "Test command")
    async def test_command(inter: Interaction):
        return message

    client.attach_router(router)

    await client.msg_in.put(
        Interaction(
            _id=1,
            application_id=1,
            _type=2,
            data={
                "id": 123,
                "name": "test",
            },
            guild_id=1,
            channel_id=1,
            member={},
            user={},
            token="")
    )

    resp: Response = await client.msg_out.get()
    assert resp.json()["data"]["content"] == message


@pytest.mark.asyncio
async def test_router_parameter(client: ClientStub):
    router = Router()
    message = "> This is working"

    @router.interaction("test", "Test command")
    async def test_command(inter: Interaction, param: str):
        assert type(param) == str
        return param

    client.attach_router(router)

    await client.msg_in.put(
        Interaction(
            _id=1,
            application_id=1,
            _type=2,
            data={
                "id": 123,
                "name": "test",
                "options": [{"name": "param", "value": message, "type": 3}]
            },
            guild_id=1,
            channel_id=1,
            member={},
            user={},
            token=""
        )
    )

    resp: Response = await client.msg_out.get()
    assert resp.json()["data"]["content"] == message


@pytest.mark.asyncio
async def test_router_option_parameter(client: ClientStub):
    router = Router()
    message = "> This is working"

    @router.interaction("test", "Test command")
    async def test_command(inter: Interaction, param: str = Option(desc="An Example Description")):
        assert type(param) == str
        return param

    client.attach_router(router)

    await client.msg_in.put(
        Interaction(
            _id=1,
            application_id=1,
            _type=2,
            data={
                "id": 123,
                "name": "test",
                "options": [{"name": "param", "value": message, "type": 3}]
            },
            guild_id=1,
            channel_id=1,
            member={},
            user={},
            token=""
        )
    )

    resp: Response = await client.msg_out.get()
    assert resp.json()["data"]["content"] == message


@pytest.mark.asyncio
async def test_router_int_parameter(client: ClientStub):
    router = Router()
    number = 10

    @router.interaction("test", "Test command")
    async def test_command(inter: Interaction, param: int):
        assert type(param) == int
        return param

    client.attach_router(router)

    await client.msg_in.put(
        Interaction(
            _id=1,
            application_id=1,
            _type=2,
            data={
                "id": 123,
                "name": "test",
                "options": [{"name": "param", "value": number, "type": 4}]
            },
            guild_id=1,
            channel_id=1,
            member={},
            user={},
            token=""
        )
    )

    resp: Response = await client.msg_out.get()
    assert resp.json()["data"]["content"] == str(number) and resp.json()["type"] == 4



@pytest.mark.asyncio
async def test_router_bool_parameter(client: ClientStub):
    router = Router()
    bool_val = True

    @router.interaction("test", "Test command")
    async def test_command(inter: Interaction, param: bool):
        assert type(param) == bool
        return param

    client.attach_router(router)

    await client.msg_in.put(
        Interaction(
            _id=1,
            application_id=1,
            _type=2,
            data={
                "id": 123,
                "name": "test",
                "options": [{"name": "param", "value": bool_val, "type": 5}]
            },
            guild_id=1,
            channel_id=1,
            member={},
            user={},
            token=""
        )
    )

    resp: Response = await client.msg_out.get()
    assert resp.json()["data"]["content"] == str(bool_val) and resp.json()["type"] == 4
