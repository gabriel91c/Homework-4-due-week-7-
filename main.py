from itertools import product

def truth_function_to_formula(n, f_values):
    variables = [f"A{i+1}" for i in range(n)]
    minterms = []

    for bits, val in zip(product([0, 1], repeat=n), f_values):
        if val == 1:
            literals = []
            for var, bit in zip(variables, bits):
                literals.append(var if bit else f"¬{var}")
            minterms.append("(" + " ∧ ".join(literals) + ")")

    if not minterms:
        return "⊥"
    if len(minterms) == 2 ** n:
        return "⊤"
    return " ∨ ".join(minterms)


majority = [0, 0, 0, 1, 0, 1, 1, 1]
print("Majority formula:")
print(truth_function_to_formula(3, majority))
print()

prime = [0, 0, 1, 1, 0, 1, 0, 1]
print("Prime formula:")
print(truth_function_to_formula(3, prime))
print()

squares = [1, 1, 0, 0, 1, 0, 0, 0]
print("Squares formula:")
print(truth_function_to_formula(3, squares))
print()

even = [1, 0, 1, 0, 1, 0, 1, 0]
print("Even formula:")
print(truth_function_to_formula(3, even))
