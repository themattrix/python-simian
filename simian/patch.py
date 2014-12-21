import mock
from contextlib2 import ExitStack, contextmanager
from functools import wraps
from itertools import chain

try:
    # noinspection PyUnresolvedReferences
    from importlib import reload
except ImportError:  # pragma: no cover
    try:  # pragma: no cover
        # noinspection PyUnresolvedReferences
        from imp import reload  # pragma: no cover
    except ImportError:  # pragma: no cover
        # Fall back to the built-in "reload", which should be present when not
        # contained in importlib or imp.
        pass  # pragma: no cover


def patch(module, module_path, external=(), internal=()):
    """
    Temporarily monkey-patch dependencies which can be external to, or internal
    to the supplied module.

    :param module: Module object
    :param module_path: Full module path (as a string)
    :param external: External dependencies to patch (full paths as strings)
    :param internal: Internal dependencies to patch (short names as strings)
    :return:
    """

    def decorator(fn):
        # The master mock is used to contain all of the sub-mocks. It is a
        # useful container and can also be used to determine the order of calls
        # to all sub-mocks.
        master_mock = mock.MagicMock()

        def get_mock(name):
            return getattr(master_mock, __patch_name(name))

        # Create a mock object under the master mock for each patched item.
        for n in chain(external, internal):
            get_mock(n)

        def patch_external(name):
            return mock.patch(name, get_mock(name))

        def patch_internal(name):
            return mock.patch('.'.join((module_path, name)), get_mock(name))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                with __nested(patch_external(n) for n in external):
                    # Reload the module to ensure that patched external
                    # dependencies are accounted for.
                    reload(module)

                    # Patch objects in the module itself.
                    with __nested(patch_internal(n) for n in internal):
                        return fn(master_mock, *args, **kwargs)
            finally:
                # When all patches have been discarded, reload the module to
                # bring it back to its original state (except for all of the
                # references which have been reassigned).
                reload(module)
        return wrapper
    return decorator


def __patch_name(long_name):
    return long_name.split('.')[-1]


@contextmanager
def __nested(context_managers):
    with ExitStack() as stack:
        yield tuple(stack.enter_context(c) for c in context_managers)
