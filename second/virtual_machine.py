class Virtual_Machine:
    def __init__(self, reqular_expression):
        self.expression = reqular_expression
        self.commands = []
        self.alphabeth = ['a', 'b']
        self.special_signs = ['|', '?', '*', '+']


    def build_commands(self):
        parts, commands_count = self.get_all_parts()
        index = 0
        used_commands = 0
        parts_count = len(parts)
        while parts_count - index != 1:
            next_part_index = used_commands + len(parts[index]) + 2
            self.commands.append(f'split {used_commands + 1} {next_part_index}')
            self.commands.extend(parts[index])
            self.commands.append(f'jmp {commands_count}')
            used_commands = next_part_index
            index += 1

        self.commands.extend(parts[-1])
        self.commands.append("match")


    def get_all_parts(self) -> tuple:
        parts = []
        last_part_start = 0
        read_commands = 0
        for i in range(len(self.expression) + 1):
            if i == len(self.expression):
                new_part = self.get_one_part(last_part_start, len(self.expression), read_commands)
                parts.append(new_part)
                read_commands += len(new_part)
                break

            if self.expression[i] == '|':
                read_commands += 1
                new_part = self.get_one_part(last_part_start, i, read_commands)
                read_commands += len(new_part)
                read_commands += 1
                parts.append(new_part)
                last_part_start = i+1

        return (parts, read_commands)

    def get_one_part(self, start_index, end_index, commands_before) -> list:
        commands = []
        for i in range(start_index, end_index):
            if self.expression[i] in self.alphabeth:
                commands.append(f'char {self.expression[i]}')
                continue
            
            if self.expression[i] == '+':
                l1 = len(commands)-1 + commands_before
                commands.append(f'split {l1} {l1 + 2}')
                continue

            if self.expression[i] == '*':
                prev_command = commands.pop()
                command_parts = prev_command.split()

                if (command_parts[0] != "char"): # we have no  braces, so input *+, for example - is incorrect
                    raise "Invalid regular expression!\n"
                
                char = command_parts[1]
                l1 = len(commands) + commands_before
                l2 = l1 + 1
                l3 = l1 + 3
                commands.append(f'split {l2} {l3}')
                commands.append(f'char {char}')
                commands.append(f'jmp {l1}')
                continue

            if self.expression[i] == '?':
                prev_command = commands.pop()
                command_parts = prev_command.split()
                if (command_parts[0] != "char"):
                    raise "Invalid regular expression!\n"
                
                char = command_parts[1]
                l1 = len(commands) + 1 + commands_before
                l2 = l1 + 1
                commands.append(f'split {l1} {l2}')
                commands.append(f'char {char}')
                continue

        return commands


    def match_word(self, word, program_counter = 0, char_index = 0):
        if len(self.commands) == 0:
            print("Please, call build_commands function before matching!\n")
            return
        counter = program_counter
        while counter < len(self.commands):
            command = self.commands[counter].split()
            if (command[0] == 'match' and char_index == len(word)):
                return True
            
            if (command[0] =='match' and char_index != len(word)):
                return False
            
            if (command[0] == 'jmp'):
                state = int(command[1])
                counter = state
                continue

            if (command[0] == 'split'):
                state1 = int(command[1])
                state2 = int(command[2])

                return self.match_word(word, state1, char_index) or self.match_word(word, state2, char_index)
            
            if (len(word) <= char_index):
                return False

            if (command[0] == 'char'):
                if (command[1] != word[char_index]):
                    return False
                char_index += 1
                counter += 1
                continue

        return False
