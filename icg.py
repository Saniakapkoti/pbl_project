import re

temp_counter = 0
label_counter = 0
symbol_table = {}

# THis is get_temp
def get_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def get_label():
    global label_counter
    label = f"L{label_counter}"
    label_counter += 1
    return label

# ------------------ Phase 1: Lexical Analysis ------------------
def lexical_analysis(code):
    tokens = re.findall(r'\w+|[()+\-*/=;<>!]', code)
    with open("tokens.txt", "w") as f:
        f.write(" ".join(tokens))
    return tokens

# ------------------ Phase 2: Syntax Analysis ------------------
def infix_to_postfix(tokens):
    precedence = {'+':1, '-':1, '*':2, '/':2, '<':0, '>':0, '==':0, '!=':0}
    output, stack = [], []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isalnum():
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        i += 1
    while stack:
        output.append(stack.pop())

    with open("postfix.txt", "w") as f:
        f.write(" ".join(output))
    return output

# ------------------ Phase 3: Semantic Analysis ------------------
def semantic_analysis(tokens):
    undeclared = [t for t in tokens if t.isalpha() and t not in symbol_table]
    if undeclared:
        raise Exception(f"Semantic Error: Undeclared variables {undeclared}")

# ------------------ Phase 4: Intermediate Code Generation ------------------
def generate_TAC(postfix_tokens):
    code = []
    stack = []
    for token in postfix_tokens:
        if token not in "+-*/<>==!=":
            stack.append(token)
        else:
            b = stack.pop()
            a = stack.pop()
            temp = get_temp()
            code.append(f"{temp} = {a} {token} {b}")
            stack.append(temp)
    return code, stack.pop()

# ------------------ Phase 5: Optimization ------------------
def optimize_TAC(lines):
    optimized = []
    defined_vars = {}
    for line in lines:
        match = re.match(r"(t\d+) = (\d+) ([+\-*/]) (\d+)", line)
        if match:
            t, a, op, b = match.groups()
            result = str(eval(f"{a}{op}{b}"))
            optimized.append(f"{t} = {result}")
            defined_vars[t] = result
        else:
            lhs = line.split("=")[0].strip()
            if lhs in defined_vars:
                del defined_vars[lhs]
            optimized.append(line)
    return optimized

# ------------------ Main Compiler ------------------
def compile_code():
    with open("test.cpp", "r") as f:
        code_lines = [line.strip() for line in f if line.strip() and not line.startswith("//")]

    tac_code = []
    declared_vars = set()

    for line in code_lines:
        if line.startswith("int") and '(' not in line:
            line = line.replace("int", "").replace(";", "")
            vars_defs = [v.strip() for v in line.split(",")]
            for item in vars_defs:
                if '=' in item:
                    var, expr = item.split('=')
                    var = var.strip()
                    expr = expr.strip()
                    tokens = lexical_analysis(expr)
                    postfix = infix_to_postfix(tokens)
                    semantic_analysis(postfix)
                    tac, result = generate_TAC(postfix)
                    tac_code.extend(tac)
                    tac_code.append(f"{var} = {result}")
                    symbol_table[var] = "int"
                else:
                    symbol_table[item] = "int"

        elif "while" in line:
            condition = line[line.find("(")+1:line.find(")")]
            label_start = get_label()
            label_end = get_label()
            tac_code.append(f"{label_start}:")
            tokens = lexical_analysis(condition)
            postfix = infix_to_postfix(tokens)
            tac, result = generate_TAC(postfix)
            tac_code.extend(tac)
            tac_code.append(f"ifFalse {result} goto {label_end}")
        
        elif "}" in line:
            tac_code.append(f"goto {label_start}")
            tac_code.append(f"{label_end}:")

        elif "=" in line:
            var, expr = line.replace(";", "").split('=')
            var = var.strip()
            expr = expr.strip()
            tokens = lexical_analysis(expr)
            semantic_analysis(tokens)
            postfix = infix_to_postfix(tokens)
            tac, result = generate_TAC(postfix)
            tac_code.extend(tac)
            tac_code.append(f"{var} = {result}")
            symbol_table[var] = "int"

    optimized = optimize_TAC(tac_code)

    # Write to files
    with open("symbol_table.txt", "w") as f:
        for var, typ in symbol_table.items():
            f.write(f"{var} : {typ}\n")

    with open("intermediate_code.txt", "w") as f:
        for line in tac_code:
            f.write(line + "\n")

    with open("optimized_code.txt", "w") as f:
        for line in optimized:
            f.write(line + "\n")

    with open("output.txt", "w") as f:
        f.write("### Final Optimized Intermediate Code (TAC)\n")
        for line in optimized:
            f.write(line + "\n")

    print("✅ Compilation complete. Check output files.")

if __name__ == "__main__":
    compile_code()
