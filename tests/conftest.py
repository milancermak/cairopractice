import asyncio

import pytest
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet

from utils import compile_contract, ADMIN


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture
async def starknet() -> Starknet:
    return await Starknet.empty()


@pytest.fixture
async def mixins(request, starknet: Starknet) -> StarknetContract:
    contract = compile_contract("contracts/mixins/main.cairo", request)
    return await starknet.deploy(contract_class=contract, constructor_calldata=[ADMIN])
