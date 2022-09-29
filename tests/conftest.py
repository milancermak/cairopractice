import asyncio

import pytest

from starkware.starknet.business_logic.state.state_api_objects import BlockInfo
from starkware.starknet.testing.starknet import Starknet


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture
async def starknet() -> Starknet:
    return await Starknet.empty()


@pytest.fixture
async def block_info(starknet):
    class Mock:
        def __init__(self, sn: Starknet):
            self.block_info = sn.state.state.block_info

        def reset(self):
            starknet.state.state.block_info = self.block_info

        def set_block_number(self, num: int):
            bi = starknet.state.state.block_info.dump()
            bi["block_number"] = num
            starknet.state.state.block_info = BlockInfo.load(bi)

        def set_block_timestamp(self, ts: int):
            bi = starknet.state.state.block_info.dump()
            bi["block_timestamp"] = ts
            starknet.state.state.block_info = BlockInfo.load(bi)

        def set_gas_price(self, price: int):
            bi = starknet.state.state.block_info.dump()
            bi["gas_price"] = price
            starknet.state.state.block_info = BlockInfo.load(bi)

        def set_sequencer_address(self, addr: int):
            bi = starknet.state.state.block_info.dump()
            bi["sequencer_address"] = addr
            starknet.state.state.block_info = BlockInfo.load(bi)


    return Mock(starknet)
