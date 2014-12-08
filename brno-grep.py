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
import re
import fileinput
import sys
from optparse import OptionParser, OptionGroup



UNDERSCORE_SEQ = '\033[4m'
RESET_SEQ = '\033[0m'
COLOR_SEQ = '\033[95m'
UNDERSCORE_CHARACTER = "^"

def terminal_size():
    """ from http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python answer by
    http://stackoverflow.com/users/362947/pascal"""
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h


class Output(object):
    """Provides output method "show()" """

    def __init__(self, options, regexp):
        self.underscore = options.underscore
        self.color = options.color
        self.machine = options.machine
        self.regexp = regexp

    def show(self, f_name, line_no, matches):
        """ Prints output according to formatting settings """
        if self.machine:
            self._print_machine_format(f_name, line_no, matches)
        elif self.color:
            print self._highlighted_format(f_name, line_no, matches)
        elif self.underscore:
            self._print_underscore_format(f_name, line_no, matches)

    def _print_machine_format(self, f_name, count, matches):
        for match in matches:
            start_pos, end_pos = match.span()
            print ':'.join([f_name, str(count), str(start_pos), match.string[start_pos:end_pos]])


    def _highlighted_format(self, f_name, line_no, matches):
        end_seq = start_seq = ""
        if self.color or self.underscore:
            end_seq = RESET_SEQ
            start_seq = COLOR_SEQ if self.color else UNDERSCORE_SEQ
        mod = re.sub(''.join([r"(", self.regexp, r")"]), start_seq + r'\1' + end_seq, matches[0].string)
        mod = ' '.join([f_name, '{:4d}'.format(line_no), mod])
        return mod.rstrip()

    def _print_underscore_format(self, f_name, line_no, matches):
        width, _ = terminal_size()
        line = matches[0].string

        occurencies = [item for sublist in [x.span() for x in matches] for item in sublist]
        occurencies.insert(0,0) #Beginning of the string. Insert spaces till the first match
        lengths_of_matches = [occurencies[x+1] - occurencies[x] for x in range(len(occurencies) - 1)]
        underlines = ""
        for i in range(len(lengths_of_matches)):
            if i % 2:
                underlines += lengths_of_matches[i] * UNDERSCORE_CHARACTER
            else:
                underlines += lengths_of_matches[i] * ' '

        line_prefix = ' '.join([f_name, '{:4d}'.format(line_no), ''])
        underline_prefix = ' ' * len(line_prefix)

        line = line_prefix + line
        underlines = underline_prefix + underlines

        line_splits = [line[x:x+width] for x in range(0, len(line), width)]
        underline_splits = [underlines[x:x+width] for x in range(0, len(underlines), width)]

        for i in range(len(line_splits)):
            print line_splits[i].rstrip()
            try:
                print underline_splits[i].rstrip()
            except IndexError:
                pass #No more matches at the end of line






if __name__ == "__main__":
    parser = OptionParser(usage="%prog [OPTIONS] PATTERN [FILE]... ")
    group = OptionGroup(parser, "Output formatting:", \
            "Following are mutually exclusive options:")
    group.add_option("-u", "--underscore", action="store_true", dest="underscore", \
            default=False, help="draw underscores under the matching text")
    group.add_option("-c", "--color", action="store_true", dest="color", \
            default=False, help="highlight matching text")
    group.add_option("-m", "--machine", action="store_true", dest="machine", default=False, \
            help="generate machine readable output\nformat: file_name:no_line:start_pos:matched_text")
    parser.add_option_group(group)\

    options, args = parser.parse_args()

    if options.underscore + options.color + options.machine > 1: #True==1, False==0
        parser.error("Options -u(--underscore), -c(--color), -m(--machine) are mutually exclusive.")
    if len(args) < 1:
        parser.error('Regular expression is mandatory')

    regexp = args[0]
    try:
        re.compile(regexp)
    except re.error:
        print 'Invalid regular expression: "%s". Exiting' % regexp
        sys.exit(2)

    args.pop(0) #now args is a list of passed files

    out = Output(options, regexp)
    try:
        for line in fileinput.input(args): # list of files in args, or stdin if args is empty or has "-"
            matches = [_ for _ in re.finditer(regexp, line)]
            if len(matches):
                out.show(fileinput.filename(), fileinput.filelineno(), matches)
    except:
        print "Error. File not found: %s. Exiting" % fileinput.filename()
        raise
        sys.exit(1)


