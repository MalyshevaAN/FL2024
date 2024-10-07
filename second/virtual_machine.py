def compile_regex(regex):
    instructions = []
    pc = 0  # program counter

    def add_instruction(op, *args):
        nonlocal pc
        instructions.append((pc, op, *args))
        pc += 1

    def compile_expr(expr):
        nonlocal pc
        if not expr:
            return

        i = 0
        while i < len(expr):
            char = expr[i]

            if char == 'a' or char == 'b':
                add_instruction(f'char {char}')
            elif char == '+':
                last_inst = instructions[-1][0]  # Get last char instruction index
                add_instruction(f'split {last_inst}, {pc + 1}')
            elif char == '|':
                left_expr = expr[:i]
                right_expr = expr[i+1:]
                L1 = pc
                add_instruction(f'split {pc + 1}, {None}')  # Placeholder for right expr
                L2 = pc
                compile_expr(left_expr)
                jmp_after_left = pc
                add_instruction(f'jmp {None}')  # Placeholder for jumping after right expr
                compile_expr(right_expr)
                instructions[L1] = (L1, f'split {L1 + 1}, {L2 + len(instructions)}')
                instructions[jmp_after_left] = (jmp_after_left, f'jmp {pc}')
                return
            elif char == '*':
                L1 = pc
                add_instruction(f'split {pc + 1}, {None}')  # Placeholder for after star expr
                L2 = pc
                compile_expr(expr[:i])
                add_instruction(f'jmp {L1}')
                instructions[L1] = (L1, f'split {L2}, {pc}')
            i += 1

    compile_expr(regex)
    add_instruction('match')
    return instructions


# Пример использования:
regex = "a|b*"
instructions = compile_regex(regex)

# Выводим инструкции:
for instr in instructions:
    print(instr)
