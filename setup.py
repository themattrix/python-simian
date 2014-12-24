from setuptools import setup

setup(
    name='simian',
    version='2.0.0',
    packages=('simian',),
    url='https://github.com/themattrix/python-simian',
    license='MIT',
    author='Matthew Tardiff',
    author_email='mattrix@gmail.com',
    install_requires=('mock', 'contextlib2'),
    tests_require=('nose', 'flake8'),
    description=(
        'A decorator for easily mocking out multiple dependencies by '
        'monkey-patching.'),
    classifiers=(
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'))
