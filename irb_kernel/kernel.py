from pexpect import replwrap, EOF
from ipykernel.kernelbase import Kernel

import signal
import subprocess

__version__ = '0.2.0'

class IrbKernel(Kernel):
    implementation = 'irb_kernel'
    implementation_version = '0.2.0'
    language_info = {
        'name': 'ruby',
        'codemirror_mode': 'ruby',
        'mimetype': 'text/x-ruby',
        'file_extension': '.rb',
    }
    banner = "Irb kernel - A Jupyter kernel for irb (REPL for Ruby programming language)"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_irb()

    def _start_irb(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        output=subprocess.getoutput("irb -v")
        try:
            if output[:7] == 'irb 1.2':
                self.irbwrapper = replwrap.REPLWrapper("irb --simple-prompt --nocolorize --nomultiline", ">> ", None, continuation_prompt="?> ")
            else:
                self.irbwrapper = replwrap.REPLWrapper("irb --simple-prompt", ">> ", None, continuation_prompt="?> ")
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.irbwrapper.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.irbwrapper.child.sendintr()
            interrupted = True
            self.irbwrapper._expect_prompt()
            output = self.irbwrapper.child.before
        except EOF:
            output = self.irbwrapper.child.before + 'Restarting irb'
            self._start_irb()

        if not silent:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

