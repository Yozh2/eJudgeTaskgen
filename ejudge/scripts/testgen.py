#!/usr/local/bin/python3

"""
The main function in this package. Generates test input and
output data based on the tests.txt file given.

[path] - path to the problem directory

Opens the problem/test.txt given and parses it. The tests are
written in the following format:
    input1
    ---
    output1
    ===
    input2
    ---
    ?
    ===
with '---' line as a middle separator between input and output
and '===' line as the end-of-test separator.

Then creates problem/tests directory and generates tests in it
in the following format:
    001.dat, 001.ans, 002.dat, 002.ans

if some output test data is '?' (like in test2 in the example
above) then testgen looks for the problem_solution.c file as the
ideal solution for the problem in the problem directory and then
lauches it with test input to get the corresponding trustful ouput
data to write to the .ans file.
"""

import os
from sys import argv
import subprocess       # For executing .c files
import argparse
import logging
from shutil import rmtree
def touch(path=None, filename=None, text=None):
    """
    Creates file at [path] named [filename] with content [text].
    If [path] doesn't exist, then creates all required subdirectories.
    The file created has it's own creation time according to the UNIX
    system time.
    """

    # Create subdirectories from the path if don't exist
    if not os.path.exists(path):
        os.makedirs(name=path, exist_ok=True)

    # Create file with name [filename], set it's time and write content
    try:
        with open(filename, 'w') as tempfile:
            os.utime(path, None)
            tempfile.writelines(text)

    except NotImplementedError:
        logging.error('os.utime: dir_fd and follow_symlinks may not be available on your platform.')
    except TypeError:
        logging.warning('tempfile.writelines(None): unable to write NoneType object.')

def create_testpath(path='.', name=0, ext=''):
    """
    Creates the path for the test file [path]/[name][ext] from the [path] directory.
    [path] - str - path of the directory with the test file.
    [name] - int - test number will be written with leading zeros to contain three digits.
    [ext]  - str - test file extension string in format '.ext' with leading dot.
    """
    return os.path.join(path, '{:03d}'.format(name) + ext)

def compile_solution(dir_path=None, path=None, solution_name=None):
    """
    Chooses the proper compiler and compiles the file to create executable solution.
    Supports compilers listed in the compiler dictionary with file extensions as keys.
    The output executable will be [dir_path]/[path].out
    Returns the path to the executable.
    """

    compiler = {'.c':'gcc', '.cpp':'g++'}
    executable = os.path.join(dir_path, solution_name + '.out')

    ext = os.path.splitext(path)[1] # get the file extension of the executable
    subprocess.call([compiler[ext], '-o', executable, path])
    return executable

def execute_solution(path=None, test=None):
    '''Execute problem_solution.ext and get output'''
    with open(test, 'rb') as test_file:
        solution = subprocess.Popen([path],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True)
        original_solution = solution.communicate(input=test_file.read())[0].decode()
    return original_solution

def get_solution(problem, test):
    """
    Get the solution for [test] from the output for the [problem] via [problem]_solution.* file.
    """

    # Create tmp_testgen subdirectory if doesn't exist
    tmp_path = os.path.join(problem, 'tmp_testgen')
    if not os.path.exists(tmp_path):
        os.makedirs(name=tmp_path, exist_ok=True)

    # Get solution filename, extension (same as the problem's one)
    solution_ext = '.c'
    solution_name = os.path.basename(problem) + '_solution' + solution_ext
    logging.info('Missing solution for %s', test)
    logging.info('Solution_name %s for problem %s', solution_name, problem)

    # Get solution path and check if it exists. Return None otherwise.
    solution_path = os.path.join(problem, solution_name)
    if not os.path.exists(solution_path):
        logging.error('No solution found %s for %s', solution_path, problem)
        return None
    logging.debug('Found solution %s for %s', solution_path, problem)

    # Compile the solution
    solution_exec_path = compile_solution(dir_path=tmp_path, path=solution_path,
                                          solution_name=solution_name)
    logging.debug('Compiled solution %s for %s', solution_exec_path, problem)

    original_solution = execute_solution(path=solution_exec_path, test=test)
    logging.info('Got solution "%s" for %s', original_solution.replace('\n', r'\n'), problem)

    return original_solution

def testgen(path='.'):
    """
    The main function in this package. Generates test input and
    output data based on the tests.txt file given.

    [path] - path to the problem directory

    Opens the problem/test.txt given and parses it. The tests are
    written in the following format:
        input1
        ---
        output1
        ===
        input2
        ---
        ?
        ===
    with '---' line as a middle separator between input and output
    and '===' line as the end-of-test separator.

    Then creates problem/tests directory and generates tests in it
    in the following format:
        001.dat, 001.ans, 002.dat, 002.ans

    if some output test data is '?' (like in test2 in the example
    above) then testgen looks for the problem_solution.c file as the
    ideal solution for the problem in the problem directory and then
    lauches it with test input to get the corresponding trustful ouput
    data to write to the .ans file.
    """

    try:
        # Check if the Problem directory path given exists
        if not os.path.exists(path):
            logging.error('Problem directory not found: %s', path)
            raise FileNotFoundError

        # Check if the test.txt file exists in the Problem directory
        test_path = os.path.join(path, 'test.txt')
        if not os.path.exists(test_path):
            logging.error('problem/test.txt file not found: %s', test_path)
            raise FileNotFoundError

        # Create problem/tests directory if it does not exist
        testdir_path = os.path.join(path, 'tests')
        if not os.path.exists(testdir_path):
            os.mkdir(testdir_path)
            logging.debug('tests directory created: %s', testdir_path)

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
        logging.error('test.txt/line%d: wrong separator %s', line_id, line3)

def clean(path='.', log='testgen.py.log'):
    """
    Perform the cleanup. Reset the situation to the state testgen.py was launched.
    Delete "problem/tests" and "./__pycache__" subdirectories, remove packet's log file.
    """
    rmtree(os.path.join(path, 'tests'), ignore_errors=True, onerror=None)
    rmtree(os.path.join(path, 'tmp_testgen'), ignore_errors=True, onerror=None)
    rmtree('__pycache__', ignore_errors=True, onerror=None)
    os.remove(log)

# ==================================================================================================
if __name__ == "__main__":

    def parse_args():
        """ Parses arguments and returns args object to the main program"""
        parser = argparse.ArgumentParser()
        parser.add_argument("PROBLEMNAME", type=str,
                            help="The name of the PROBLEM directory we want work to.")
        parser.add_argument('-c', "--clean", action='store_true',
                            help="Reset the situation. Delete tests subdirectory, clean logs.")
        return parser.parse_args()

    # Enable logging
    LOG = u'{}.log'.format(argv[0])
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] \
    %(message)s', level=logging.DEBUG, filename=LOG)

    # Parse command-line arguments
    ARGS = parse_args()
    PATH = os.path.abspath(os.path.join('.', os.pardir, ARGS.PROBLEMNAME))
    #PATH = os.path.join('.', os.pardir, ARGS.PROBLEMNAME)
    # PATH = abspath(./../problem)

    if not ARGS.clean:
        # Generate tests directory and parse test.txt file
        testgen(PATH)
    else:
        clean(PATH, LOG)
