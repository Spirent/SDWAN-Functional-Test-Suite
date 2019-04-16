#!/usr/bin/env python

"""
This file is used to run the test script individually
Example:
python3 runtest.py -f /home/spirent/vincent3/einstein/testpacks/sample/sdwan001.py -c /home/spirent/vincent3/einstein//testbed.yaml -o /home/spirent/vincent3/einstein/testrun2
"""
import os
import sys
import argparse
import ast

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-f', '--script', help='test script')
arg_parser.add_argument(
    '-c', '--config', help='YAML config file')
arg_parser.add_argument(
    '-o', '--outdir', help='Output result dir')

args = arg_parser.parse_args()

if args.script is None:
    sys.exit("Test script must be specified")
if args.config is None:
    sys.exit("YMAL config file must be specified")
if args.outdir is None:
    sys.exit("Output dir must be specified")
if not os.path.exists(args.script):
    sys.exit("Missing script file: {0}".format(args.script))
if not os.path.exists(args.config):
    sys.exit("Missing config file: {0}".format(args.config))
if not os.path.exists(args.outdir):
    sys.exit("Missing output dir: {0}".format(args.outdir))

#Get class name in the script
f = open(args.script,'r')
root = ast.parse(f.read())
classes = [node.name for node in ast.walk(root) if isinstance(node, ast.ClassDef)]
f.close()

if classes is None or len(classes)==0:
    sys.exit("Missing class name in the test script: {0}".format(args.script))
classname = classes[0]
sys.path.append(os.path.dirname(args.script))
scriptname = os.path.splitext(os.path.basename(args.script))[0]
exec("from {0} import {1} as testClass".format(scriptname, classname))

print("<--------test initializing...----------->")
runner = testClass(args.outdir, args.config)
try:
    print("<--------test setup...------------------>")
    runner.setup()

    print("<--------test run...-------------------->")
    runner.run()
except Exception as e:
    print("Error: %s" % e)
finally :
    print("<--------test cleanup...---------------->")
    runner.cleanup()
    print("<--------test end----------------------->")    
