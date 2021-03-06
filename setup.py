# -*- encoding: utf8 -*-
import glob
import io
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(
    name="wri-dbseeder",
    version="4.2.0",
    license="MIT",
    description="ETL WRI Data",
    long_description="",
    author="Steve Gourley",
    author_email="SGourley@utah.gov",
    url="https://github.com/agrc/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "dbseeder = dbseeder.__main__:main"
        ]
    },
    cmdclass={
        'test': Tox
    },
    install_requires=[
        'requests==2.8.1',
        'pyopenssl==0.15.1',
        'ndg-httpsclient==0.4.0',
        'pyasn1==0.1.9'
    ],
    tests_require=[
        'tox',
        'nose==1.3.4',
        'coverage==3.7.1'
    ],
)
