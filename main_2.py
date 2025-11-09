from itertools import product
from functools import reduce
from sympy import symbols, And, Or, Not, Xor, Implies, Equivalent, sympify
from sympy.logic.boolalg import BooleanFunction, simplify_logic
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def truth_fn_to_dnf(n, f_values, var_prefix='A'):
    vars_ = [symbols(f"{var_prefix}{i+1}") for i in range(n)]
    minterms = []
    for bits, val in zip(product([0,1], repeat=n), f_values):
        if val in (1, True):
            lits = [(v if b == 1 else Not(v)) for v, b in zip(vars_, bits)]
            minterms.append(And(*lits))
    if not minterms:
        return sympify(False)
    return Or(*minterms) if len(minterms) > 1 else minterms[0]

def parse_formula(formula_str, var_names):
    local = {name: symbols(name) for name in var_names}
    s = (formula_str
         .replace('¬', '~')
         .replace('∧', '&')
         .replace('∨', '|')
         .replace('⊕', '^'))
    import re
    xor_pattern = r'\(?\s*([A-Za-z_]\w*)\s*\^\s*([A-Za-z_]\w*)\s*\)?'
    while re.search(xor_pattern, s):
        s = re.sub(xor_pattern, r'Xor(\1, \2)', s)
    transformations = standard_transformations + (implicit_multiplication_application,)
    expr = parse_expr(
        s,
        local_dict={**local, 'Xor': Xor},
        evaluate=False,
        transformations=transformations
    )
    return expr

def rewrite_to_basic(expr):
    if not isinstance(expr, BooleanFunction):
        return expr
    args = [rewrite_to_basic(a) for a in expr.args]
    if expr.func is Not:
        return Not(args[0])
    if isinstance(expr, Xor):
        def xor2(p, q):
            return Or(And(Not(p), q), And(p, Not(q)))
        return reduce(xor2, args)
    if isinstance(expr, Implies):
        a, b = args
        return Or(Not(a), b)
    if isinstance(expr, Equivalent):
        a, b = args
        return Or(And(a, b), And(Not(a), Not(b)))
    return expr.func(*args)

def local_cleanup(expr):
    if not isinstance(expr, BooleanFunction):
        return expr
    args = [local_cleanup(a) for a in expr.args]
    if expr.func is Not:
        x = args[0]
        if isinstance(x, BooleanFunction) and x.func is Not:
            return x.args[0]
        return Not(x)
    if expr.func is And:
        flat = list(args)
        keep = []
        for a in flat:
            absorbed = False
            for b in flat:
                if b is a: continue
                if (isinstance(b, BooleanFunction) and b.func is Or and a in b.args):
                    absorbed = True; break
            if not absorbed:
                keep.append(a)
        keep = list({str(k): k for k in keep}.values())
        return And(*keep) if len(keep) > 1 else keep[0]
    if expr.func is Or:
        flat = list(args)
        keep = []
        for a in flat:
            absorbed = False
            for b in flat:
                if b is a: continue
                if (isinstance(b, BooleanFunction) and b.func is And and a in b.args):
                    absorbed = True; break
            if not absorbed:
                keep.append(a)
        keep = list({str(k): k for k in keep}.values())
        return Or(*keep) if len(keep) > 1 else keep[0]
    return expr.func(*args)

def minimize(expr, form='dnf'):
    try:
        return simplify_logic(expr, form=form, force=True)
    except Exception:
        return expr

def gate_count(expr):
    if not isinstance(expr, BooleanFunction):
        return {'NOT': 0, 'AND': 0, 'OR': 0}
    if expr.func is Not:
        sub = gate_count(expr.args[0])
        sub['NOT'] += 1
        return sub
    if expr.func in (And, Or):
        counts = {'NOT': 0, 'AND': 0, 'OR': 0}
        for a in expr.args:
            c = gate_count(a)
            for k in counts:
                counts[k] += c[k]
        counts['AND' if expr.func is And else 'OR'] += max(0, len(expr.args) - 1)
        return counts
    counts = {'NOT': 0, 'AND': 0, 'OR': 0}
    for a in expr.args:
        c = gate_count(a)
        for k in counts:
            counts[k] += c[k]
    return counts

def pipeline_from_truth_fn(n, f_values, var_prefix='A', target_form='dnf'):
    dnf_expr = truth_fn_to_dnf(n, f_values, var_prefix)
    basic = rewrite_to_basic(dnf_expr)
    cleaned = local_cleanup(basic)
    minimized = minimize(cleaned, form=target_form)
    return {
        'dnf': dnf_expr,
        'minimized': minimized,
        'gates_dnf': gate_count(dnf_expr),
        'gates_min': gate_count(minimized)
    }

def pipeline_from_formula(formula_str, var_names, target_form='dnf'):
    expr0 = parse_formula(formula_str, var_names)
    basic = rewrite_to_basic(expr0)
    cleaned = local_cleanup(basic)
    minimized = minimize(cleaned, form=target_form)
    return {
        'original': expr0,
        'basic_only': cleaned,
        'minimized': minimized,
        'gates_basic': gate_count(cleaned),
        'gates_min': gate_count(minimized)
    }

if __name__ == "__main__":
    res = pipeline_from_truth_fn(3, [0,0,0,1,0,1,1,1], 'A')
    print("=== Majority Function ===")
    print("DNF       :", res['dnf'])
    print("Minimized :", res['minimized'])
    print("Gates DNF :", res['gates_dnf'])
    print("Gates Min :", res['gates_min'])
    print()
    prime = pipeline_from_truth_fn(3, [0,0,1,1,0,1,0,1], 'A')
    print("=== Prime(3) ===")
    print("DNF       :", prime['dnf'])
    print("Minimized :", prime['minimized'])
    print("Gates DNF :", prime['gates_dnf'])
    print("Gates Min :", prime['gates_min'])
    print()
    cout_str = "(A & B) | (Cin & (A ^ B))"
    cout = pipeline_from_formula(cout_str, ['A','B','Cin'])
    print("=== Full Adder Carry-out ===")
    print("Original  :", cout['original'])
    print("Basic only:", cout['basic_only'])
    print("Minimized :", cout['minimized'])
    print("Gates Basic:", cout['gates_basic'])
    print("Gates Min  :", cout['gates_min'])
    print()
    sum_ = pipeline_from_truth_fn(3, [0,1,1,0,1,0,0,1], 'X')
    print("=== Full Adder Sum ===")
    print("DNF       :", sum_['dnf'])
    print("Minimized :", sum_['minimized'])
    print("Gates DNF :", sum_['gates_dnf'])
    print("Gates Min :", sum_['gates_min'])
