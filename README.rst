irb_kernel
==========

A Jupyter kernel for irb (REPL for Ruby programming language)

To install::

    sudo apt install ruby
    pip install irb_kernel
    python -m irb_kernel.install

To use it, run one of:

.. code:: shell

    jupyter notebook
    # In the notebook interface, select Irb from the 'New' menu
    jupyter qtconsole --kernel irb
    jupyter console --kernel irb

For details of how this works, see the Jupyter docs on `wrapper kernels
<http://jupyter-client.readthedocs.org/en/latest/wrapperkernels.html>`_, and
Pexpect's docs on the `replwrap module
<http://pexpect.readthedocs.org/en/latest/api/replwrap.html>`_
