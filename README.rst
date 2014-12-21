Simian
======

|Build Status| |Coverage Status| |Code Health|

A decorator for easily mocking out multiple dependencies by
monkey-patching. Example:

.. code:: python

    # my_package.my_module
    from third_party_package import expensive_fn
    from my_package.other_module import another_expensive_fn

    def my_fn():
        if expensive_fn():
            another_expensive_fn()
            local_expensive_fn()


    def local_expensive_fn():
        ...


    # my_package.test.test_my_module
    import simian
    from functools import partial
    from mock import call
    from my_package import my_module


    patch_my_fn = partial(
        simian.patch,
        module=my_module,
        module_path='my_package.my_module',
        external=(
            'third_party_package.expensive_fn',
            'my_package.other_module.another_expensive_fn'),
        internal=(
            'local_expensive_fn',))


    @patch_my_fn()
    def test_my_fn_with_expensive_fn_true(master_mock):
        master_mock.expensive_fn.return_value = True
        my_module.my_fn()
        assert master_mock.mock_calls == [
            call.expensive_fn(),
            call.another_expensive_fn(),
            call.local_expensive_fn()]


    @patch_my_fn()
    def test_my_fn_with_expensive_fn_false(master_mock):
        master_mock.expensive_fn.return_value = False
        my_module.my_fn()
        assert master_mock.mock_calls == [
            call.expensive_fn()]

.. |Build Status| image:: https://travis-ci.org/themattrix/python-simian.svg?branch=master
   :target: https://travis-ci.org/themattrix/python-simian
.. |Coverage Status| image:: https://img.shields.io/coveralls/themattrix/python-simian.svg
   :target: https://coveralls.io/r/themattrix/python-simian
.. |Code Health| image:: https://landscape.io/github/themattrix/python-simian/master/landscape.svg
   :target: https://landscape.io/github/themattrix/python-simian/master
