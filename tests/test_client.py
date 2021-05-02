from json import loads
import pytest
from dispair import Router, Interaction, Option

from stubs.client_stub import ClientStub
from tests.stubs.request_stub import RequestStub


@pytest.fixture(scope="function")
async def client() -> ClientStub:
    client = ClientStub()
    client.run()
    yield client
    await client.kill()



@pytest.mark.asyncio
async def test_ack(client: ClientStub):
    await client.msg_in.put(RequestStub(type=1))

    msg = await client.msg_out.get()
    payload = loads(msg.text)
    assert payload["type"] == 1



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

    await client.msg_in.put(RequestStub(type=2, data={"name": "test"}))

    resp = await client.msg_out.get()
    payload = loads(resp.text)
    assert payload["type"] == 4 and payload["data"]["content"] == message



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
        RequestStub(
            type=2,
            data={
                "name": "test",
                "options": [{"name": "param", "value": message, "type": 3}]}
        ))

    resp = await client.msg_out.get()
    payload = loads(resp.text)
    assert payload["type"] == 4 and payload["data"]["content"] == message



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
        RequestStub(
            type=2,
            data={
                "name": "test",
                "options": [{"name": "param", "value": message, "type": 3}]}
        ))

    resp = await client.msg_out.get()
    payload = loads(resp.text)
    assert payload["type"] == 4 and payload["data"]["content"] == message



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
        RequestStub(
            type=2,
            data={
                "name": "test",
                "options": [{"name": "param", "value": number, "type": 4}]}
        ))

    resp = await client.msg_out.get()
    payload = loads(resp.text)
    assert payload["type"] == 4 and payload["data"]["content"] == str(number)



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
        RequestStub(
            type=2,
            data={
                "name": "test",
                "options": [{"name": "param", "value": bool_val, "type": 5}]}
        ))

    resp = await client.msg_out.get()
    payload = loads(resp.text)
    assert payload["type"] == 4 and payload["data"]["content"] == str(bool_val)
