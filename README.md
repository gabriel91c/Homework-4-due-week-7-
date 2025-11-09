# Homework-4-due-week-7-
This project implements the core concepts from the Logic for Computer Science (Week 7) assignment:

Theorem 4.1 – Generate a propositional formula (DNF) from a truth function

Formula Simplification – Apply logical equivalences to transform less efficient circuits into simpler ones

Circuit Reduction – Normalize all formulas to use only unary (NOT) and binary (AND, OR) gates

Gate Counting – Compare the number of logic gates before and after simplification

Both tools are implemented in Python using SymPy.

Installation
1. Clone or Download

Download or clone the repository to your local computer:

git clone https://github.com/yourusername/LCS_Circuit_Design.git
cd LCS_Circuit_Design


Or simply copy the provided main_2.py into your project folder.

2. Create a Virtual Environment (recommended)
python -m venv .venv


Activate it:

Windows:

.venv\Scripts\activate


macOS/Linux:

source .venv/bin/activate

3. Install Dependencies

Install the required package:

pip install sympy


That’s all you need — the rest is pure Python.

Usage
Run the program

Simply execute:

python main_2.py


You’ll see the results printed directly in the console for all test cases.

Program Structure
1. truth_fn_to_dnf()

Generates the canonical DNF (sum of products) from a given truth table.

Example:

# Majority function of 3 variables
res = pipeline_from_truth_fn(3, [0,0,0,1,0,1,1,1], 'A')
print(res['dnf'])


Output:

(A1 & A2 & A3) | (A1 & A2 & ~A3) | (A1 & A3 & ~A2) | (A2 & A3 & ~A1)

2. pipeline_from_formula()

Takes a propositional formula (possibly inefficient) and:

Rewrites subformulas to equivalent ones

Reduces everything to {NOT, AND, OR}

Minimizes the formula using simplify_logic

Counts the number of gates before and after simplification

Example:

cout_str = "(A & B) | (Cin & (A ^ B))"
cout = pipeline_from_formula(cout_str, ['A','B','Cin'])
print(cout['minimized'])


Output:

(A & B) | (A & Cin) | (B & Cin)

3. Built-in Demonstrations

When running main_2.py, you’ll automatically see:

Majority Function (from truth function)

Prime(3) – binary representation of primes up to 7

Full Adder Carry-out – formula simplification with XOR

Full Adder Sum – canonical DNF from truth table

Each case prints:

Canonical formula (DNF)

Simplified/minimized formula

Gate counts before and after

Example Output
=== Majority Function ===
DNF       : (A1 & A2 & A3) | (A1 & A2 & ~A3) | (A1 & A3 & ~A2) | (A2 & A3 & ~A1)
Minimized : (A1 & A2) | (A1 & A3) | (A2 & A3)
Gates DNF : {'NOT': 3, 'AND': 8, 'OR': 3}
Gates Min : {'NOT': 0, 'AND': 3, 'OR': 2}

=== Full Adder Carry-out ===
Original  : (A & B) | (Cin & (A ^ B))
Basic only: (A & B) | (Cin & ((~A & B) | (A & ~B)))
Minimized : (A & B) | (A & Cin) | (B & Cin)
Gates Basic: {'NOT': 2, 'AND': 4, 'OR': 2}
Gates Min  : {'NOT': 0, 'AND': 3, 'OR': 2}

Features

Converts truth functions to propositional formulas

Simplifies formulas via logical equivalence
Rewrites all logic to NOT, AND, OR only

Counts logic gates for circuit complexity comparison

Works for arbitrary n-variable truth functions

Example Circuit Design Interpretation

The output formulas correspond directly to circuits:

¬ → NOT gate (inverter)

∧ → AND gate

∨ → OR gate

You can draw each minimized formula as a simplified logic circuit using Logisim, CircuitVerse, or by hand in your report.

License
This project is provided for academic and educational use (Logic for Computer Science – Week 7).


Author
Gabriel Chirinciuc
West University of Timișoara
Artificial Intelligence – Year 1
