irb_kernel
==========

|PyPI version shields.io|

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/irb_kernel.svg
   :target: https://pypi.python.org/pypi/irb_kernel/
   
.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/PyDataOsaka/irb_kernel/master

A Jupyter wrapper kernel for irb (REPL for Ruby programming language)

The code in this project is almost same as bash_kernel_.
Many thanks to the bash_kernel_ project.

.. _bash_kernel: https://github.com/takluyver/bash_kernel/

To Try irb_kernel without installing, click the binder badge

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/PyDataOsaka/irb_kernel/master


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
