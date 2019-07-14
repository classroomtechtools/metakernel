from metakernel import MetaKernel
from ib_pseudocode_python.cli import Transpiler

import sys
from io import StringIO


class PseudocodeKernel(MetaKernel):
    implementation = 'IB_Pseudocode Python'
    implementation_version = '0.7'
    language_version = '0.1'
    language_info = {'name': 'ib_pseudocode', 'file_extension': '.pseudo', 'mimetype': 'text/plain'}
    banner = "IB PseudoCode kernel - transpiles to Python and executes"
    transpiler = Transpiler()

    kernel_json = {
        'argv': [
            sys.executable, '-m', 'metakernel_pseudocode', '-f', '{connection_file}'],
        'display_name': 'IB Pseudocode',
        'language': 'ib_pseudocode',
        'name': 'metakernel_pseudocode'
    }

    kernel_javascript = """
define(
['codemirror/lib/codemirror', 'codemirror/addon/mode/simple'],
function(CodeMirror, simple) {
  return {
    onload: function(){
        CodeMirror.defineSimpleMode('ib_pseudocode', {
            start: [
                {regex: /%%transpile/,
                    token: "comment"},
                {regex: /\\b(?:if|else|then|while|loop|end|from|to|until)\\b/,
                   token: "keyword"},
                {regex: /\\b(?:output|Stack|Collection|Array)\\b/,
                   token: "atom"},
                {regex: /\\/\\/.*/,
                    token: "comment"},
                {regex: /\\b(?:NOT|div|mod)\\b/,
                    token: "operator"},
                {regex: /[.,=≠<>+\\*-]/,
                    token: "operator"},
                {regex: /\\b[A-Z_]+\\b/,
                    token: "string-2"},
                {regex: /\\b[0-9.]+\\b/,
                    token: "number"},
                {regex: /".*?"/,
                    token: "string"},
                {regex: /[()\\[\\]]/,
                    token: "bracket"},
                {regex: /\\b(?:hasNext|addItem|getNext|push|pop|isEmpty|dequeue|enqueue)\\b/,
                    token: "attribute"},
                {regex: /\\bfrom_.*?\\b/,
                    token: "attribute"}
            ]
        });
        console.log('loaded');
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
            message = {"metadata": {}, "data": {'text/plain': "\n".join(result)}, "execution_count": self.execution_count}
            self.send_response(self.iopub_socket, 'execute_result', message)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
        }


if __name__ == "__main__":

    PseudocodeKernel.run_as_main()
