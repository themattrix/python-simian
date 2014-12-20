from distutils.core import setup

setup(
    name='simian',
    version='1.0.0',
    packages=('simian',),
    url='https://github.com/themattrix/python-simian',
    license='MIT',
    author='Matthew Tardiff',
    author_email='mattrix@gmail.com',
    install_requires=('mock',),
    tests_require=('nose',),
    description=(
        'A decorator for easily mocking out multiple dependencies by '
        'monkey-patching.'))
