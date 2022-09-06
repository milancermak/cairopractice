# Cairo conventions

This is a highly opinionated set of Cairo conventions. As code is read much more often than it is written, it should be written in an easy to understand fashion. We believe conventions like the following lead to more secure code, less cognitive load on the reader and improve collaboration.

## Use the official formatter

cairo-lang comes with the official formatter tool, `cairo-format`. Use it. We shouldn't be bike shedding about a contract's formatting, but rather spend our energy elsewhere. If you're using VSCode, every cairo-lang release contains a .vsix file. Install it and use it.

## Use felt over Uint256 whenever possible

The usage of `felt` for holding numerical values is preferrable to `Uint256`. Felts are cheaper and easier to use. There are exceptions to this rule - to conform with ERC standards or if the potential value of a variable doesn't fit a `felt`, use `Uint256`.

## Imports

Use fully qualified path when importing. The top-level module is always `contracts`:

```cairo
from contracts.module.submodule.file_name import function
```

This prevents any issues when compiling contracts.

## General naming conventions

We follow these conventions when naming things

| thing                     | convention                  | example                                                          |
|---------------------------|-----------------------------|------------------------------------------------------------------|
| directories and files     | snake_case                  | `module_name/module.cairo`                                       |
| functions                 | snake_case                  | `func open_account{...}(){}`                                     |
| namespaces                | PascalCase                  | `namespace Engine`                                               |
| contract interfaces       | PascalCase prepended with I | <pre>@contract_interface<br />namespace IAccount{<br />}</pre>   |
| structs                   | PascalCase                  | `struct Loan`                                                    |
| variables, struct members | snake_case                  | `let user_balance = 100;`                                        |
| events                    | PascalCase                  | <pre>@event<br />func ThingHappened(){<br />}</pre>              |
| constants                 | UPPER_SNAKE_CASE            | `const CAP_AMOUNT = 10**18;`                                     |

See sections below for further specific rules.

## @storage_var naming

To prevent [`@storage_var` conflicts](https://github.com/crytic/amarna/issues/10) and clearly distinguish between a local variable and a storage container, a `@storage_var` should be named using the following template: `modulename_variable_name_storage` - that is, the variable name is prefixed by the module name (lowercase, no separation) and suffixed by the string `storage`, separated by underscores.

An example of a variable named `balance` inside a module called `Treasury`:

```cairo
@storage_var
func treasury_balance_storage() -> (balance : felt) {
}
```

## Getters

A `@view` function that retrieves a `@storage_var` (essentially a getter) should be named `get_FOO`:

```cairo
@storage_var
func module_amount_storage() -> (amount: felt) {
}

@view
func get_amount{syscall_ptr: felt*, pedersen_ptr: HashBuiltin*, range_check_ptr}() -> (amount: felt) {
    let (amount: felt) = module_amount_storage.read();
    return (amount,);
}
```

## Events

Use Capitalized names (`Mint` 👍 / `mint` 👎) for [Events](https://www.cairo-lang.org/docs/hello_starknet/events.html) (note that the linked page doesn't follow this convention).

Prefer emitting events from `@external`, `@l1_handler` or `@constructor` functions, i.e. public functions that presumably change the state. It's ok to emit from internal helper functions as well if they change the state. Never emit from `@view` functions.

## Use module names in error messages

When using the `with_attr error_message()` pattern to do a check and raise an error if it fails, prepend the error message itself with the module name. It makes it easier for debugging, etc. An example from the `direct_deposit` module:

```cairo
with_attr error_message("direct_deposit: transferFrom failed") {
    assert was_transfered = TRUE;
}
```

## Address Variables

Add the `_address` suffix to any variable holding an address. Unlike Solidity, Cairo doesn't yet have an address type, and so adding this suffix makes it clearer to the reader what the variable is and does.

`const usdc = 0x...;` becomes `const usdc_address = 0x...;` and so on.

## Specifying variable and function argument types

If a variable or function type is a felt, don't specify its type with the `: felt` specifier. If a variable is any type but a felt, always specify its type.

Examples of what to do:

```cairo
func some_func(a) -> (b: felt) {
    return (y,);
}
```

```cairo
let (output) = some_func(5);
```

```cairo
func some_second_func(a: SomeStruct) -> (b: SomeStruct) {
    return (a);
}
```

```cairo
let (output: SomeStruct) = some_second_func(SomeStruct(4,5));
```

Example of what NOT to do:

```cairo
let (output) = some_second_func(SomeStruct(4,5)); // <-- The type of output isn't specified
```

## Naming of return values for functions and storage variables

Return variables should be named according to their 'type' rather than according to their purpose or function. This is because many different 'types' of variables are all represented by felts: booleans (0 or 1), fixed point numbers, negative numbers, etc.

The naming conventions are the following:

- `bool`: FALSE or TRUE (from bool.cairo, which are equal to 0 and 1 respectively)
- `wad`: 18 decimal fixed point number
- `ray`: 27 decimal fixed point number
- `ufelt`: "regular" felt. Equivalent to `uint` in other languages.
- `sfelt`: "signed" felt, or a felt that stores the prime-field arithmetic equivalent of negative numbers.
- `address`: a contract address
- `packed`: A felt that has had multiple values packed into it
- Structs: For return variables that are structs, their name should be the struct name in snake case. For example, `SomeStruct` becomes `some_struct`.

These names can be used as a standalone value (1), or as suffixes if you want to communicate the meaning of a value (2) or multiple return values of the same 'type' (3), as illustrated in the following example:

```cairo
# 1
func get_price() -> (wad: felt) {
}

# 2
func get_price() -> (price_wad: felt) {
}

# 3
func get_price_pair() -> (current_price_wad: felt, previous_price_wad: felt) {
}
```

## Using mixins

[Mixins](https://mirror.xyz/0xa37228277Ed21843c5F61F4Ed2928Af5Df2A81C9/Bm9YJK1mhdJPH7z3f5lY9Wu5wrL1tlUz4xaHGBPZ5oE) hold functions that can be reused in distinct smart contracts. These files must have the `_external.cairo` suffix in their name. When using mixins in a smart contract, simply import the required function using the `import` statement.

```cairo
from contracts.mixins.ownable.ownable_external import owner, transfer_ownership, renounce_ownership
```
