from collections import namedtuple
import pytest

from starkware.starknet.testing.contract import StarknetContract
from starkware.starkware_utils.error_handling import StarkException

from utils import compile_contract, str_to_felt


Person = namedtuple("Person", "age height countries_visited")


@pytest.fixture
async def tips(starknet) -> StarknetContract:
    contract = compile_contract("contracts/testing_tips/tips.cairo")
    return await starknet.deploy(contract_class=contract)


@pytest.mark.asyncio
async def test_using_pytest_raises(tips):
    # checks that the call to assert_lt_10 raises a StarkException
    # the test would fail otherwise
    with pytest.raises(StarkException):
        await tips.assert_lt_10(20).execute()

    # test execution continues, we can use pytest.raises
    # multiple times in a single test case

    # we can even check if the error message is as expected
    with pytest.raises(StarkException, match=r"value \d+ is not less than 10"):
        await tips.assert_lt_10(42).execute()


@pytest.mark.asyncio
async def test_using_caller_address(tips):
    # using ADMIN as the caller
    await tips.only_admin().execute(caller_address=str_to_felt("ADMIN"))

    # using any other address failes
    with pytest.raises(StarkException):
        await tips.only_admin().execute(caller_address=0xdeadbeef)


@pytest.mark.asyncio
async def test_using_structs(tips):
    # this test demonstrates various uses of Cairo structs in
    # a Python enviornment

    # creating a namedtuple instance and using that to compare the returned "struct"
    baby = Person(1, 75, 2)
    assert (await tips.build_person(1, 75, 2).execute()).result.person == baby
    assert (await tips.build_person(*baby).execute()).result.person == baby

    # using the compiled contract to build a Python representation of a struct directly,
    # notice we're using the name "Person" which comes from Cairo
    sumo_fighter = tips.Person(34, 267, 18)
    assert (await tips.build_person(34, 267, 18).execute()).result.person == sumo_fighter
    assert (await tips.build_person(*sumo_fighter).execute()).result.person == sumo_fighter

    # we can use the structs member names to get to each value
    adventurer = (await tips.build_person(43, 77, 112).execute()).result.person
    assert adventurer.age == 43
    assert adventurer.height == 77
    assert adventurer.countries_visited == 112


@pytest.mark.asyncio
async def test_using_block_info_mock(tips, block_info):
    original_block_state = (await tips.get_block_state().execute()).result

    new_bn = 999
    new_ts = 16_000_000
    new_seq_addr = "0xc0ffee"

    # here we're using the block_info fixture to set custom
    # block state values

    block_info.set_block_number(new_bn)
    block_info.set_block_timestamp(new_ts)
    block_info.set_sequencer_address(new_seq_addr)

    new_block_state = (await tips.get_block_state().execute()).result

    assert new_block_state.block_number == new_bn
    assert new_block_state.block_timestamp == new_ts
    assert new_block_state.sequencer_address == int(new_seq_addr, 16)

    # reseting the block state to its original values

    block_info.reset()

    assert (await tips.get_block_state().execute()).result == original_block_state
