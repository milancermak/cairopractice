%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin

from contracts.mixins.ownable.library import Ownable
// these public functions will be part of the compiled contract
from contracts.mixins.ownable.ownable_external import owner, transfer_ownership, renounce_ownership


@storage_var
func counter() -> (value: felt) {
}


@constructor
func constructor{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}(owner) {
    Ownable.initializer(owner);

    return ();
}

@external
func increase_counter{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (
    incremented: felt
) {
    with_attr error_message("Only owner can increase counter") {
        Ownable.assert_only_owner();
    }

    let (c) = counter.read();
    counter.write(c + 1);

    return (c + 1,);
}
