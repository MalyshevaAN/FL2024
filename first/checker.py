import os

from state_machine import State_Machine

class Checker:
    def __init__(self):
        self.machines_and_tests = {
            "/tests/test1.txt" : "/tests/test1_data.txt",
            "/tests/test2.txt" : "/tests/test2_data.txt",
            "/tests/test3.txt" : "/tests/test3_data.txt",
            "/tests/test4.txt" : "/tests/test4_data.txt",
            "/tests/test5.txt" : "/tests/test5_data.txt"
        }

    def check_correctness(self):
        for machine_file, test_file in self.machines_and_tests.items():
            machine = State_Machine(machine_file)
            with open(os.path.dirname(os.path.abspath(__file__)) + test_file, 'r') as f:
                all_done = True
                num_line = 1
                test = f.readline()
                print("Testing file " + machine_file + "...")
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
            


if __name__ == "__main__":
    checker = Checker()
    checker.check_correctness()
