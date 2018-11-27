jupyter-logging-widget
===============================

A Jupyter widget for capturing and monitoring logs.

Installation
------------

To install use pip:

    $ pip install jupyter-logging-widget
    $ jupyter nbextension enable --py --sys-prefix jupyter-logging-widget


For a development installation (requires npm),

    $ git clone https://github.com/sanbales/jupyter-logging-widget.git
    $ cd jupyter-logging-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix jupyter-logging-widget
    $ jupyter nbextension enable --py --sys-prefix jupyter-logging-widget
