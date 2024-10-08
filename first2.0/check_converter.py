import os

from converter import Converter
from state_machine import State_Machine


class Check_Converter:
    def __init__(self):
        self.machines_and_tests = {
            "/tests/test_converter_1.txt": "/tests/test_converter_1_data.txt",
            "/tests/test_converter_2.txt": "/tests/test_converter_2_data.txt",
            "/tests/test_converter_3.txt": "/tests/test_converter_3_data.txt"
        }

    def check_correctness(self):
        for machine_file, test_file in self.machines_and_tests.items():
            test_converter = Converter(machine_file)
            test_converter.make_dfa("/tests/test.txt")
            # проверяем, что перестроенный
            # dfa автомат работает также, как изначально данный nfa автомат
            machine = State_Machine("/tests/test.txt")
            with open(os.path.dirname(os.path.abspath(__file__))
                      + test_file, 'r') as f:
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
    checker = Check_Converter()
    checker.check_correctness()
