import os

from virtual_machine import Virtual_Machine


class Checker:
    def __init__ (self):
        self.tests_common_name = "/vm_tests/test"

    def test(self):
        passed = True
        for i in range (1, 11):
            file_name = self.tests_common_name + str(i) + ".txt"
            with open (os.path.dirname(os.path.abspath(__file__)) + file_name, 'r') as f:
                reqular_expression = f.readline()
                virtual_machine = Virtual_Machine(reqular_expression)
                virtual_machine.build_commands()
                line = f.readline()
                while line:
                    word, result = line.split()
                    if (virtual_machine.match_word(word) != int(result)):
                        print(f'Something went wrong while testing {file_name}:'
                              f'regular expression {reqular_expression}'
                              f'and word {word}\n')
                        passed = False
                        return 
                    line = f.readline()
        if passed:
            print("All passed!\n")


if __name__ == "__main__":
    checker = Checker()
    checker.test()
