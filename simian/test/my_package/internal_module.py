from simian.test.my_package.external_module import external_fn_a
from simian.test.my_package.external_module import external_fn_b


def my_fn():
    external_fn_a()
    external_fn_b()
    internal_fn_a()
    internal_fn_b()


def internal_fn_a():
    raise RuntimeError('internal_fn_a() should never be called')


def internal_fn_b():
    raise RuntimeError('internal_fn_b() should never be called')
