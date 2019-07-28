from metakernel import MetaKernel
from ib_pseudocode_python.cli import Transpiler

import sys
from io import StringIO


class PseudocodeKernel(MetaKernel):
    implementation = 'Vanilla Python'
    implementation_version = '0.7'
    language_version = '0.1'
    language_info = {'name': 'vanilla_python', 'file_extension': '.vanilla', 'mimetype': 'text/plain'}
    banner = "Vanilla Python kernel - transpiles to Python and executes"
    transpiler = Transpiler()

    kernel_json = {
        'argv': [
            sys.executable, '-m', 'metakernel_vanilla_python', '-f', '{connection_file}'],
        'display_name': 'Vanilla Python',
        'language': 'vanilla_python',
        'name': 'vanilla_python'
    }

    kernel_javascript = r"""
define(
['codemirror/lib/codemirror', 'codemirror/addon/mode/simple', 'codemirror/addon/mode/multiplex'],
function(CodeMirror) {

    CodeMirror.defineSimpleMode('ib_pseudocode_top', {
        start: [
            {regex: /%%transpile/,
                token: "comment"},
            {regex: /".*?"/,  // string
                token: "string"},
            {regex: /\b(?:if|else|then|while|loop|from|to|until)\b/,
               token: "keyword"},
            {regex: /\bend(?! sub)\b/,
                token: "keyword"},
            {regex: /\bsub\b/,
                token: "def"},
            {regex: /\bend sub\b/,
               token: "def"},
            {regex: /\breturn\b/,
               token: "meta"},
            {regex: /\b(?:output|out|Stack|Collection|Queue|Array)\b/,
               token: "atom"},
            {regex: /#.*/,
                token: "comment"},
            {regex: /\b(?:NOT|div|mod|AND|OR)\b/,
                token: "operator"},
            {regex: /[.,=≠<>+\*-]/,
                token: "operator"},
            {regex: /\b[0-9.]+(?![A-Z_]+)\b/,  // number
                token: "string"},
            {regex: /\b(?:true|false)\b/,
                token: "string"},
            {regex: /\b[A-Z0-9_]+\b/,  // variable
                token: "string-2"},
            {regex: /[()\[\]]/,
                token: "bracket"},
            {regex: /\b(?:hasNext|addItem|getNext|resetNext|push|pop|isEmpty|dequeue|enqueue)\b/,
                token: "attribute"},
            {regex: /\b(?:from_x_integers|from_list|from_x_characters|from_file).*?\b/,
                token: "attribute"}
        ]
    });
    return {
        onload: function(){
            CodeMirror.defineMode("vanilla_python", function (config) {
                return CodeMirror.multiplexingMode(
                    CodeMirror.getMode(config, "ib_pseudocode_top"),
                    {
                        open: '###',
                        close: '###',
                        delimStyle: 'comment',
                        mode: CodeMirror.getMode(config, "plain")
                    },
                    {
                        open: '# py:',
                        close: '# vanilla:',
                        delimStyle: 'comment',
                        mode: CodeMirror.getMode(config, "python")
                    }
                )
            });
        }
    };
});
"""

    def __init__(self, *args, **kwargs):
        self.out_magic = None
        super().__init__(*args, **kwargs)

    def do_execute(self, code, *args, **kwargs):
        kwargs['silent'] = True
        return super().do_execute(code, **kwargs)

    def do_execute_direct(self, code):
        pseudo_code_stream = StringIO(code)
        pseudocode, code = self.transpiler.transpile(pseudo_code_stream)
        if hasattr(self, 'transpile_magic_offset'):
            result, error = self.transpiler.execute_and_capture(
                code, pseudocode, lineoffset=self.transpile_magic_offset
            )
        else:
            result, error = self.transpiler.execute_and_capture(code, pseudocode)

        result = result.strip().split('\n')
        if error:
            # Output the non-error part to stout, and output the error part to sterr
            if len(result) > 4:
                self.Print('\n'.join(result[:len(result)-4]))
                self.Error('\n'.join(result[len(result)-4:]))
            else:
                self.Error('\n'.join(result))
        else:
            # Output whatever we got in stout as the output cell
            message = {
                "metadata": {},
                "data": {
                    'text/plain': "\n".join(result)
                },
                "execution_count": self.execution_count
            }
            self.send_response(self.iopub_socket, 'execute_result', message)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }


if __name__ == "__main__":

    PseudocodeKernel.run_as_main()
