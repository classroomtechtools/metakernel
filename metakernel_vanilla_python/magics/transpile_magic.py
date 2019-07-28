from metakernel import Magic
from ib_pseudocode_python.cli import Transpiler
import click
import io

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalTrueColorFormatter, TerminalFormatter


class TranspileMagic(Magic):

    def cell_transpile(self):
        """

        """
        transpiler = Transpiler()

        # lines keep getting added on, complicating calculations
        pseudocode, code = transpiler.transpile(io.StringIO(self.code.rstrip()))
        code = code.rstrip()

        # calc starting line no
        starting_blanks = 0  # start at one because we know there's at least one (not included) magic line
        for line in code.split('\n'):
            if line.strip():  # once we found non-whitespace, stop counting
                break
            else:
                starting_blanks += 1
        offset = starting_blanks + 2
        self.kernel.transpile_magic_offset = offset - starting_blanks - 1
        justify = len(str(len(code.split('\n')) + self.kernel.transpile_magic_offset)) + 2  # for gutter

        lexer = get_lexer_by_name("python3", stripall=True)
        formatter = TerminalFormatter()
        result = highlight(code, lexer, formatter)

        self.kernel.Print('\n'.join([f"{i+offset}".rjust(justify, ' ') + '|  ' + line for i, line in enumerate(result.split('\n'))]))
        self.evaluate = True


def register_magics(kernel):
    kernel.register_magics(TranspileMagic)
