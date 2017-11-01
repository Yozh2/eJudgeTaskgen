#!/usr/local/bin/python3
import os
from sys import argv
import subprocess       # For executing .c files
import argparse
import logging

from pprint import PrettyPrinter
from prettytable import PrettyTable

# TODO  write args error handling in methods

def touch(path=None, filename=None, text=None):
    # Create subdirectories from the path if don't exist

    if not os.path.exists(path):
        os.makedirs(path)

    with open(filename, 'w') as tempfile:
        os.utime(path, None)
        tempfile.writelines(text)

def create_testpath(path='.', name='', ext=''):
    return os.path.join(path, '{:03d}'.format(name) + ext)

def compile_solution(path=None, ext=None):
    compiler = {'.c':'gcc', '.cpp':'g++', '.py':'error'}               # Choose the compiler
    subprocess.call([compiler[ext], '-o', path + '.out', path])
    return path + '.out'

def get_solution(problem, test):

    """
    Get the solution from the output of the problem with
    """

    # Create paths to the problem_solution.ext and
    solution_ext = '.c' # For future improvements
    solution_name = os.path.basename(problem) + '_solution' + solution_ext
    logging.debug('Missing solution for {}'.format(test))

    solution_path = os.path.join(problem, solution_name)
    # TODO check if the solution exists
    logging.debug('Found solution {} for {}'.format(solution_path, problem))

    # Compiling the solution
    solution_exec_path = compile_solution(solution_path, solution_ext)
    logging.debug('Compiled solution {} for {}'.format(solution_exec_path, problem))

    # Execute problem_solution.ext and get output
    with open(test, 'rb') as test_file:
        solution = subprocess.Popen([solution_exec_path],
                                    stdin=subprocess.PIPE,  stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True)
        original_solution = solution.communicate(input=test_file.read())[0].decode()
        logging.debug('Got solution "{}" for {}'.format(original_solution.replace('\n', r'\n'), problem))

    os.remove(solution_exec_path)
    return original_solution

def testgen(path='.'):
    """
    Opens the func_A/test.txt given and parses it. The tests are written in the following format:

        input1
        ---
        output1
        ===
        input2
        ---
        output2
        ===

    Then creates func_A/tests directory and generates tests in it in the following format:
        001.dat, 001.ans, 002.dat, 002.ans

    path - path to the fucn_A directory
    """

    try:
        # Check if the Problem directory path given exists
        if not os.path.exists(path):
            logging.error('Problem directory not found: {}'.format(path))
            raise FileNotFoundError

        # Check if the test.txt file exists in the Problem directory
        test_path = os.path.join(path, 'test.txt')
        if not os.path.exists(test_path):
            logging.error('problem/test.txt file not found: {}'.format(test_path))
            raise FileNotFoundError

        # Create problem/tests directory if it does not exist
        testdir_path = os.path.join(path, 'tests')
        if not os.path.exists(testdir_path):
            os.mkdir(testdir_path)
            logging.debug('tests directory created: {}'.format(testdir_path))

        # Starting to parse the problem/test.txt file
        seps = {'mid':'---', 'end':'==='}       # separators
        data = list()                           # data list
        ans = list()                            # answer list

        with open(test_path, 'r') as test_file:
            dat_id = 0      # Number of .dat file name
            ans_id = 0      # Number of .ans file name
            line_id = 0     # Line number
            content = 'data'

            for line in test_file.readlines():
                # if line begins with --- or === then it is separator
                # First we read data until --- separator
                # Then we read answer until === separator
                # if we meet some odd separators, raise the exception and ignore those lines
                line_id += 1
                line3 = line[:3]

                if content == 'data':
                    # Read Data
                    if line3 not in seps.values():
                        data.append(line)
                    # Wrong separator detected -> raise exception and ignore the line
                    elif line3 == seps['end']:
                        logging.warning('test.txt/line{}: wrong separator'.format(line_id, seps['end']))
                        raise UserWarning
                    else: # found correct middle separator
                        dat_id += 1
                        testname = create_testpath(path=testdir_path, name=dat_id, ext='.dat')
                        touch(path=testdir_path, filename=testname, text=data)
                        data = []
                        content = 'answer'

                elif content == 'answer':
                    # Read answer
                    if line3 not in seps.values():
                        if line[0] == '?':  # Need to get answer from ideal solution
                            test_path = create_testpath(path=testdir_path, name=dat_id, ext='.dat')
                            ans = get_solution(problem=path, test=test_path)
                            continue

                        ans.append(line)
                    # Wrong separator detected -> raise exception and ignore the line
                    elif line3 == seps['mid']:
                        logging.warning('test.txt/line{}: wrong separator'.format(line_id, seps['mid']))
                        raise UserWarning
                    else: # found correct middle separator
                        ans_id += 1
                        ansname = create_testpath(path=testdir_path, name=ans_id, ext='.ans')
                        touch(path=testdir_path, filename=ansname, text=ans)
                        ans = []
                        content = 'data'

    except FileNotFoundError:
        print('No such file or directory!')
        exit()

    except UserWarning:
        pass



# ==================================================================================================
if __name__ == "__main__":

    def parse_args():
        """ Parses arguments and returns args object to the main program"""
        parser = argparse.ArgumentParser()
        parser.add_argument("PROBLEMNAME", type=str, nargs='?', default='.',
                            help="The name of the PROBLEM directory we want work to.")
        return parser.parse_args()

    # Enable logging
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] \
    %(message)s', level=logging.DEBUG, filename=u'{}.log'.format(argv[0]))

    # Parse command-line arguments
    ARGS = parse_args()
    #PATH = os.path.abspath(os.path.join('.', os.pardir, ARGS.PROBLEMNAME))
    PATH = os.path.join('.', os.pardir, ARGS.PROBLEMNAME)
    # PATH = abspath(./../problem)

    testgen(PATH)
