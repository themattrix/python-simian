Simian |Version| |Build| |Coverage| |Health|
============================================

|Compatibility| |Implementations| |Format| |Downloads|

A decorator for easily mocking out multiple dependencies by
monkey-patching.

``simian.patch`` is a wrapper around `mock.patch`_ to allow
for convenient patching of multiple targets in a single decorator.
All resulting patched objects are collected under a single
``master_mock`` object, which is provided to the function being
decorated.

For example:

.. code:: python

    #
    # my_package.my_module
    #

    from time import sleep

    def my_sleep(duration_secs):
        print('Sleeping for {duration} seconds'.format(duration=duration_secs))
        sleep(duration_secs)


    #
    # my_package.test.test_my_module
    #

    import simian
    from my_package import my_module

    @simian.patch(my_module, external=['time.sleep'])
    def test_my_sleep(master_mock):
        my_module.my_sleep(99)
        master_mock.sleep.assert_called_once_with(99)


Note several things about ``time.sleep`` in the above example:

* It is patched and provided to the test as ``master_mock.sleep``.
* The patching works despite ``my_sleep`` calling ``sleep`` directly,
  as opposed to calling the fully-qualified ``time.sleep``.

The second point works because ``simian.patch`` reloads the given
module *after* patching all of the external targets. It reloads the
module *again* after leaving the decorated function, bringing the
module back to its pre-patched state.

The above example demonstrates ``external`` patching, but ``internal``
(same-module) patching works as well. Let's extend the above example:

.. code:: python

    #
    # my_package.my_module
    #

    from time import sleep

    def my_sleep(duration_secs):
        my_logger('Starting {n}-second sleep'.format(n=duration_secs))
        sleep(duration_secs)
        my_logger('Finished {n}-second sleep'.format(n=duration_secs))

    def my_logger(msg):
        ...


    #
    # my_package.test.test_my_module
    #

    import simian
    from my_package import my_module

    @simian.patch(
        my_module,
        'my_package.my_module',
        external=['time.sleep'],
        internal=['my_logger'])
    def test_my_sleep(master_mock):
        my_module.my_sleep(99)
        master_mock.assert_has_calls(
            calls=[
                call.my_logger('Starting 99-second sleep'),
                call.sleep(99),
                call.my_logger('Finished 99-second sleep')],
            any_order=False)

Note that when ``internal`` targets are supplied, the full path to the module
under test must also be supplied (in this case, ``my_package.my_module``).


.. |Build| image:: https://travis-ci.org/themattrix/python-simian.svg?branch=master
   :target: https://travis-ci.org/themattrix/python-simian
.. |Coverage| image:: https://img.shields.io/coveralls/themattrix/python-simian.svg
   :target: https://coveralls.io/r/themattrix/python-simian
.. |Health| image:: https://landscape.io/github/themattrix/python-simian/master/landscape.svg
   :target: https://landscape.io/github/themattrix/python-simian/master
.. |Version| image:: https://pypip.in/version/simian/badge.svg?text=version
    :target: https://pypi.python.org/pypi/simian
.. |Downloads| image:: https://pypip.in/download/simian/badge.svg
    :target: https://pypi.python.org/pypi/simian
.. |Compatibility| image:: https://pypip.in/py_versions/simian/badge.svg
    :target: https://pypi.python.org/pypi/simian
.. |Implementations| image:: https://pypip.in/implementation/simian/badge.svg
    :target: https://pypi.python.org/pypi/simian
.. |Format| image:: https://pypip.in/format/simian/badge.svg
    :target: https://pypi.python.org/pypi/simian
.. _mock.patch: https://docs.python.org/3/library/unittest.mock.html#patch
