"""
Implement a script in Python that searches one or more named input
files (standard input if no files are specified, or the file name
'-' is given) for lines containing a match to a regular expression
pattern (given on command line as well).

Assume that input is ascii, you don't need to deal with different
encoding.

If a line matches, print it. Please print the file name and the line
number for every match.

Script accept list optional parameters which are mutually exclusive:
-u ( --underscore ) which draw underscores under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine readable output
                   format: file_name:no_line:start_pos:matched_text

Multiple matches on single line are allowed, without overlapping.

The script should be compatible with Python 2.6, and in line with
PEP8 coding guidelines. Please add proper documentation and error
handling.

Hint: Is is recommended to use a module for parsing the command line
arguments and the "re" module for matching the pattern.
Try to use OOP in order to encapsulate differences  between output
formats.

Feel free to ask any questions you have.

[1] http://www.pixelbeat.org/docs/terminal_colours
"""
import sys
import re
import itertools

from optparse import OptionParser, OptionGroup

UNDERSCORE_SEQ = '\033[4m'
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[95m'

parser = OptionParser(usage="%prog [OPTIONS] PATTERN [FILE]... ")
group = OptionGroup(parser, "Output formatting", "Following are mutually exclusive options")
group.add_option("-u", "--underscore", action="store_true", dest="underscore", default=False, help="draw underscores under the matching text")
group.add_option("-c", "--color", action="store_true", dest="color", default=False, help="highlight matching text")
group.add_option("-m", "--machine", action="store_true", dest="machine", default=False, help="generate machine readable output\n                   format: file_name:no_line:start_pos:matched_text")
parser.add_option_group(group)
options, args = parser.parse_args()
if options.underscore + options.color + options.machine > 1:
    parser.error("Options -u(--underscore), -c(--color), -m(--machine) are mutually exclusive.")
if len(args) < 1:
    parser.error('Regular expression is mandatory')
regexp = args[0]
files = args[1:] if args[1:] else [sys.stdin]
print options
print args


class Output(object):

    def __init__(self, options):
        self.underscore = options.underscore
        self.color = options.color
        self.machine = options.machine

    def show(self, f_name, count, matches):
        if self.machine:
            print self._machine_format(f_name, count, matches)
        else:
            print self._highlighted_format(f_name, count, matches)

    def _machine_format(self, f_name, count, matches):
        for match in matches:
            start_pos, end_pos = match.span()
            print ':'.join([f_name, str(count), str(start_pos), match.string[start_pos:end_pos]])


    def _highlighted_format(self, f_name, count, matches):
        """>>> import itertools
>>> y = itertools.flatten(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'flatten'
>>> y = [j for a in x for j in a]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined
>>> y = [j for i in a for j in i]
>>> y
[1, 2, 3, 4, 6, 7]
>>> from itertools import chain
>>> a
[(1, 2), (3, 4), (6, 7)]
>>> list(chain(a))
[(1, 2), (3, 4), (6, 7)]
>>> list(chain(*a))
[1, 2, 3, 4, 6, 7]
>>> list(chain(*a))
[1, 2, 3, 4, 6, 7]
>>> bond = list(chain(*a))
>>> bond
[1, 2, 3, 4, 6, 7]
>>> aaa='111111111111'
>>> for i in range(len(bond)):
...
KeyboardInterrupt
>>> q = []
>>> for i in range(len(bond)):
...     q.append(aaa[i:i+1]+'$')
...
>>> q
['1$', '1$', '1$', '1$', '1$', '1$']
>>> ''.join(q)
'1$1$1$1$1$1$'
>>>
"""

        end_seq = start_seq = ""
        if self.color or self.underscore:
            end_seq = RESET_SEQ
            start_seq = COLOR_SEQ if self.color else UNDERSCORE_SEQ

        spans = [x.span for x in matches]
        boundaries = itertools.chain(*spans)
        start_mark = True
        resulting_string = ""
        for i in boundaries:
            resulting_string += matches[0].string




out = Output(options)

for f_name in files:
    count = 1
    with open(f_name, 'rb') as handle:
        for line in handle:
            matches = [_ for _ in re.finditer(regexp, line)]
            if len(matches):
                out.show(f_name, count, line, matches)
                print f_name, count, line.strip()
            count += 1






























