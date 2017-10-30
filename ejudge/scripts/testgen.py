#!/usr/local/bin/python3
import os
from sys import argv
import argparse
import logging

from pprint import PrettyPrinter
from prettytable import PrettyTable

def touch(path=None, name=None, text=None, ext=None):
    # Create subdirectories from the path if don't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Create filename
    filename = os.path.join(path, '{:03d}'.format(name) + '.' + ext)
    with open(filename, 'w') as tempfile:
        os.utime(path, None)
        tempfile.writelines(text)

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
                        touch(path=testdir_path, name=dat_id, text=data, ext='dat')
                        data = []
                        content = 'answer'

                elif content == 'answer':
                    # Read answer
                    if line3 not in seps.values():
                        ans.append(line)
                    # Wrong separator detected -> raise exception and ignore the line
                    elif line3 == seps['mid']:
                        logging.warning('test.txt/line{}: wrong separator'.format(line_id, seps['mid']))
                        raise UserWarning
                    else: # found correct middle separator
                        ans_id += 1
                        touch(path=testdir_path, name=ans_id, text=ans, ext='ans')
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
        parser.add_argument('-d', '--debug', action='store_true',
                            help="Print auxillary debug information while the \
                            program is running")
        return parser.parse_args()

    # Enable logging
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] \
    %(message)s', level=logging.DEBUG, filename=u'{}.log'.format(argv[0]))

    # Parse command-line arguments
    ARGS = parse_args()
    PATH = os.path.join('.', os.pardir, ARGS.PROBLEMNAME)

    # Raise an exception if the path doens't exist
    try:
        if not os.path.exists(PATH):
            raise FileNotFoundError

        testgen(PATH)

    except FileNotFoundError:
        print('Directory Not Found')
        logging.error('Directory Not Found')
        exit()
