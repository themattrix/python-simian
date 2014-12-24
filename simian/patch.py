import mock
from contextlib2 import ExitStack, contextmanager
from functools import wraps
from simian.reload import reload as reload_module


def patch(module, external=(), internal=()):
    """
    Temporarily monkey-patch dependencies which can be external to, or internal
    to the supplied module.

    :param module: Module object
    :param external: External dependencies to patch (full paths as strings)
    :param internal: Internal dependencies to patch (short names as strings)
    :return:
    """
    external = tuple(external)
    internal = tuple(internal)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # The master mock is used to contain all of the sub-mocks. It is a
            # useful container and can also be used to determine the order of
            # calls to all sub-mocks.
            master_mock = mock.MagicMock()

            def get_mock(name):
                return getattr(master_mock, __patch_name(name))

            def patch_external(name):
                return mock.patch(name, get_mock(name))

            def patch_internal(name):
                return mock.patch(module.__name__ + '.' + name, get_mock(name))

            try:
                with __nested(patch_external(n) for n in external):
                    if external:
                        # Reload the module to ensure that patched external
                        # dependencies are accounted for.
                        reload_module(module)

                    # Patch objects in the module itself.
                    with __nested(patch_internal(n) for n in internal):
                        return fn(master_mock, *args, **kwargs)
            finally:
                if external:
                    # When all patches have been discarded, reload the module
                    # to bring it back to its original state (except for all of
                    # the references which have been reassigned).
                    reload_module(module)
        return wrapper
    return decorator


def __patch_name(long_name):
    return long_name.split('.')[-1]


@contextmanager
def __nested(context_managers):
    with ExitStack() as stack:
        yield tuple(stack.enter_context(c) for c in context_managers)
