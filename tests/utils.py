import os

from starkware.starknet.compiler.compile import compile_starknet_files
from starkware.starknet.services.api.contract_class import ContractClass


def str_to_felt(text: str) -> int:
    b_text = bytes(text, "ascii")
    return int.from_bytes(b_text, "big")


ADMIN = str_to_felt("admin")


def here() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def contract_path(rel_contract_path: str) -> str:
    return os.path.join(here(), "..", rel_contract_path)


def compile_contract(rel_contract_path: str, request) -> ContractClass:
    contract_src = contract_path(rel_contract_path)
    contract_cache_key = rel_contract_path + "/compiled"
    ctime_key = rel_contract_path + "/ctime"

    contract_ctime = int(os.path.getctime(contract_src))
    last_contract_ctime = request.config.cache.get(ctime_key, None)

    if contract_ctime == last_contract_ctime:
        # if last access time equals current and there's a cache-hit
        # return the compiled contract from cache
        serialized_contract = request.config.cache.get(contract_cache_key, None)
        if serialized_contract is not None:
            return ContractClass.loads(serialized_contract)

    compiled_contract = compile_starknet_files(
        [contract_src],
        debug_info=True,
        disable_hint_validation=True,
    )

    # write compiled contract to cache
    serialized_contract = ContractClass.dumps(compiled_contract)
    request.config.cache.set(contract_cache_key, serialized_contract)
    request.config.cache.set(ctime_key, contract_ctime)

    return compiled_contract
