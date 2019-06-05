jupyter-logging-widget
======================

A Jupyter widget for capturing and monitoring loggers.

Installation
------------

To install use pip:

    $ pip install git+https://github.com/sanbales/jupyter-logging-widget.git


For a development installation,

    $ git clone https://github.com/sanbales/jupyter-logging-widget.git
    $ cd jupyter-logging-widget
    $ pip install -e .

Usage
-----

To use, import and instantiate the widget in your Jupyter notebook:

    $ from ipyw_logger import LoggerWidget
    $ LoggerWidget()

TODOs
-----

* Improve the performance of the viewer (potentially implement throttling)
* Add documentation
* Add tests
