from pexpect import replwrap, EOF
import signal
from ipykernel.kernelbase import Kernel

class IrbKernel(Kernel):
    implementation = 'irb_kernel'
    implementation_version = '0.0.1'
#    language = 'no-op'
#    language_version = '0.1'
    language_info = {
        'name': 'ruby',
        'codemirror_mode': 'ruby',
        'mimetype': 'text/x-ruby',
        'file_extension': '.rb',
    }
    banner = "Irb kernel - as useful as a parrot"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_irb()

    def _start_irb(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.irbwrapper = replwrap.REPLWrapper("irb --simple-prompt", ">> ", None)
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not code.strip():
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

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=IrbKernel)
