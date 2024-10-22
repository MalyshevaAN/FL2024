import os

from dfa_minimize import DFA_State_Machine


class Simple_Checker:
    def __init__(self):
        self.machines_and_tests = {
            "/tests/test1.txt": "/tests/test1_data.txt",
            "/tests/test2.txt": "/tests/test2_data.txt",
        }

    def check_correctness(self):
        for machine_file, test_file in self.machines_and_tests.items():
            machine = DFA_State_Machine(machine_file)
            with open(os.path.dirname(os.path.abspath(__file__))
                      + test_file, 'r') as f:
                all_done = True
                num_line = 1
                test = f.readline()
                print("Testing file " + machine_file + "...")
                machine.dfa_minimize()
                while (test and all_done):
                    test = test.split()
                    word = test[0]
                    result = bool(int(test[1]))
                    if (machine.accept_word(word) != result):
                        print("Test failed: line " + str(num_line))
                        all_done = False
                        break
                    test = f.readline()
                    num_line += 1
                if (all_done):
                    print("All tests passed!")


class Equality_Checker:
    def __init__(self):
        self.machines_and_tests = {
            "/tests/test1.txt": "/tests/test1_equal.txt",
            "/tests/test2.txt": "/tests/test2_equal.txt",
        }

        self.full_machines = {
            "/tests/test1.txt": False,
            "/tests/test2.txt": False,
            "/tests/test3.txt": True
        }

    def check_equality(self):
        passed = True
        print("Testing euality...")
        for machine_file, test_file in self.machines_and_tests.items():
            machine = DFA_State_Machine(machine_file)
            equal = machine.check_equality(test_file)
            if (not equal):
                print("Something went wrong while testing ", machine_file)
                passed = False
                break
        if (passed):
            print("All passed!")

    def all_words_equality(self):
        passed = True
        for machine_file, result in self.full_machines.items():
            print("Testing file " + machine_file + " for having all words\n")
            machine = DFA_State_Machine(machine_file)
            if machine.check_if_all_words() != result:
                print("Something went wrong while testing ", machine_file)
                passed = False
                break
        if (passed):
            print("All passed!")


if __name__ == "__main__":
    simple_checker = Simple_Checker()
    simple_checker.check_correctness()
    equality_checker = Equality_Checker()
    equality_checker.check_equality()
    equality_checker.all_words_equality()
