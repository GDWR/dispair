from dispair import Client

import pytest


@pytest.fixture(scope="session")
def client() -> Client:
    yield Client()


@pytest.mark.asyncio
def test_discord_interaction(client: Client):
    client.run()
