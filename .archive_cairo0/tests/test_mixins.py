import pytest

from starkware.starknet.testing.contract import StarknetContract
from starkware.starkware_utils.error_handling import StarkException

from utils import ADMIN, compile_contract


@pytest.fixture
async def mixins(starknet) -> StarknetContract:
    contract = compile_contract("contracts/mixins/main.cairo")
    return await starknet.deploy(contract_class=contract, constructor_calldata=[ADMIN])


@pytest.mark.asyncio
async def test_contract(mixins):
    # check ADMIN is the owner, using the imported `owner` function
    assert (await mixins.owner().execute()).result.owner == ADMIN

    # check that the owner can call increase_counter
    assert (await mixins.increase_counter().execute(caller_address=ADMIN)).result.incremented == 1

    # renounce ownership
    # the renounce_ownership function is imported
    # into the final contract as a mixin
    await mixins.renounce_ownership().execute(caller_address=ADMIN)

    # calling the increase_counter function must fail now
    # after renouncing ownership
    with pytest.raises(StarkException, match="Ownable: caller is not the owner"):
        await mixins.increase_counter().execute(caller_address=ADMIN)
