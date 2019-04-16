#!/usr/bin/env python

import argparse
from genie.conf import Genie

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--testbed_file', help='Testbed file to validate')
args = arg_parser.parse_args()

if args.testbed_file is None:
    sys.exit("Testbed file must be specified")

try:
    testbed = Genie.init(args.testbed_file)
except Exception as e:
    raise e.__context__
