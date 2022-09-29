%lang starknet

from starkware.cairo.common.bool import TRUE
from starkware.cairo.common.math import assert_lt_felt
from starkware.starknet.common.syscalls import (
    get_block_timestamp,
    get_block_number,
    get_caller_address,
    get_sequencer_address,
)

struct Person {
    age: felt,
    height: felt,
    countries_visited: felt,
}

@view
func assert_lt_10{range_check_ptr}(a: felt) {
    with_attr error_message("value {a} is not less than 10") {
        assert_lt_felt(a, 10);
    }
    return ();
}

@view
func only_admin{syscall_ptr: felt*, range_check_ptr}() -> (bool: felt) {
    let (caller) = get_caller_address();
    with_attr error_message("caller is not admin") {
        assert caller = 'ADMIN';
    }
    return (TRUE,);
}

@view
func build_person(age, height, countries_visited) -> (person: Person) {
    return (Person(age, height, countries_visited),);
}

@view
func get_block_state{syscall_ptr: felt*}() -> (
    block_number: felt, block_timestamp: felt, sequencer_address: felt
) {
    let (block_number) = get_block_number();
    let (block_timestamp) = get_block_timestamp();
    let (sequencer_address) = get_sequencer_address();
    return (block_number, block_timestamp, sequencer_address);
}
