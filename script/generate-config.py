#!/usr/bin/env python

import argparse
import codecs
import jinja2
import yaml
import os
import sys
from jinja2 import TemplateAssertionError
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Const


#
# http://xion.io/post/code/jinja-custom-errors.html
#
class ErrorExtension(Extension):
    """Extension providing {% error %} tag, allowing to raise errors
    directly from a Jinja template.
    """
    tags = frozenset(['error'])

    def parse(self, parser):
        """Parse the {% error %} tag, returning an AST node."""
        tag = parser.stream.next()
        message = parser.parse_expression()

        node = CallBlock(
            self.call_method('_exec_error', [message, Const(tag.lineno)]),
            [], [], [])
        node.set_lineno(tag.lineno)
        return node

    def _exec_error(self, message, lineno, caller):
        """Execute the {% error %} statement, raising an exception."""
        raise TemplateUserError(message, lineno)


class TemplateUserError(TemplateAssertionError):
    """Exception raised in the template through the use of {% error %} tag."""


def load_config(config):
    with open(config) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_template(template):
    if template is None:
        return jinja2.Template(
            sys.stdin.read(),
            extensions=[ErrorExtension],
            undefined=jinja2.StrictUndefined)

    path, filename = os.path.split(template)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path),
        extensions=[ErrorExtension],
        undefined=jinja2.StrictUndefined)
    return env.get_template(filename)


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', '--config', help='Physical testbed config file (YAML)')
arg_parser.add_argument('-t', '--template', help='Testbed template file (YAML)')
arg_parser.add_argument('-i', '--testbed_id', help='Testbed identifier in physical config')
arg_parser.add_argument('-f', '--testbed_file', help='Testbed output file')

args = arg_parser.parse_args()

if args.config is None:
    sys.exit("Physical testbed config file must be specified")
elif not os.path.exists(args.config):
    sys.exit("Missing config file: {0}".format(args.config))

if args.template is None:
    sys.exit("Testbed template file must be specified")
elif not os.path.exists(args.template):
    sys.exit("Missing template file: {0}".format(args.template))

if args.testbed_id is None:
    sys.exit("Testbed name must be specified")
    
if args.testbed_file is None:
    sys.exit("Output filename must be specified")

# Read JSON config
variables = load_config(args.config)

# Write to file
template = load_template(args.template)
file = open(args.testbed_file,"w")
file.write(template.render(variables[args.testbed_id]))
file.write("\n")
file.close()
