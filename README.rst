Simian |Version| |Build| |Coverage| |Health|
============================================

|Compatibility| |Implementations| |Format| |Downloads|

A decorator for easily mocking out multiple dependencies by
monkey-patching.

.. code:: python

    @simian.patch(module=..., module_path=..., external=[...], internal=[...])


Installation:

.. code:: shell

    $ pip install simian


``simian.patch`` is a convenience wrapper around `mock.patch`_ with the
following benefits:

1. All patched objects are collected under a single ``master_mock``, which is
   provided to the function being decorated. Any patched target can be
   accessed by its basename (e.g., a patched ``time.sleep`` would be
   accessed in the decorated function as ``master_mock.sleep``).
2. The patching works even if the target is imported directly (e.g., a call to
   ``sleep`` is patched the same as a call to ``time.sleep``). Simian handles
   this by reloading the module under test after applying the ``external``
   patches.
3. Objects ``internal`` to the module under test can be patched as well. They
   are collected under the same ``master_mock`` and can be referenced in the
   same way.

After leaving the decorated function, simian reloads the module under test
*again*, bringing it back to its pre-patched state (although all of the
module's addresses in memory have changed).


External Patching
-----------------

.. code:: python

    #
    # my_package.my_module
    #

    from time import sleep


    def my_sleep(duration_secs):
        print('Sleeping for {n} seconds'.format(n=duration_secs))
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


Internal Patching
-----------------

The above example demonstrates ``external`` patching, but ``internal``
(same-module) patching works as well. Let's extend the above example.

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
        print(msg)


    #
    # my_package.test.test_my_module
    #

    import simian
    from mock import call
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
under test must also be supplied (in this case, ``"my_package.my_module"``).
Simian uses this string to build the full target path.


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
