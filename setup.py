from __future__ import print_function
from distutils import log
import os

from setuptools import setup, find_packages


here = os.path.dirname(os.path.abspath(__file__))
is_repo = os.path.exists(os.path.join(here, '.git'))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'A Jupyter widget for capturing and monitoring logs.'


def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py_ = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py_.finalize_options()


version_ns = {}

with open(os.path.join(here, 'ipyw_logger', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    'name': 'ipyw_logger',
    'version': version_ns['__version__'],
    'description': 'A Jupyter widget for capturing and monitoring logs.',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'data_files': [],
    'install_requires': [
        'colorama',
        'ipywidgets>=7.0.0',
        'traitlets',
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {},

    'author': 'Santiago Balestrini-Robinson',
    'author_email': 'sanbales@gmail.com',
    'url': 'https://github.com/sanbales/jupyter-logging-widget',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
}

setup(**setup_args)
