# mixins

Illustrating how [mixins](https://mirror.xyz/0xa37228277Ed21843c5F61F4Ed2928Af5Df2A81C9/Bm9YJK1mhdJPH7z3f5lY9Wu5wrL1tlUz4xaHGBPZ5oE) work in Cairo.

Working code can be found in [`contracts/mixins/main.cairo`](../contracts/mixins/main.cairo). It uses the OpenZeppeling implementation of the `ownable` library and declares the public to-be-imported functions in [`ownable/ownable_external.cairo`](../contracts/mixins/ownable/ownable_external.cairo). These are then imported in the main contracts. When compiled, they are part of the contract's ABI.

A simple test can be found in [`test_mixins.py`](../tests/test_mixins.py).
