from mock import call
from nose.tools import eq_, raises
from simian import patch
from simian.test.my_package import internal_module
from simian.test.my_package import external_module


def test_patch_with_multiple_arguments():
    @patch(
        module=internal_module,
        external=(
            'simian.test.my_package.external_module.external_fn_a',
            'simian.test.my_package.external_module.external_fn_b'),
        internal=(
            'internal_fn_a',
            'internal_fn_b'))
    def inner(master_mock):
        internal_module.my_fn()
        eq_(master_mock.mock_calls, [
            call.external_fn_a(),
            call.external_fn_b(),
            call.internal_fn_a(),
            call.internal_fn_b()])
    inner()  # pylint: disable=E1120


@raises(RuntimeError)
def test_patch_with_no_external():
    @patch(
        module=internal_module,
        internal=(
            'internal_fn_a',
            'internal_fn_b'))
    def inner(master_mock):
        try:
            internal_module.my_fn()
        except RuntimeError as e:
            eq_(str(e), 'called external_fn_a()')
            eq_(master_mock.mock_calls, [])
            raise
    inner()  # pylint: disable=E1120


def test_patch_with_no_external_does_not_reload():
    @patch(
        module=internal_module,
        internal=(
            'internal_fn_a',
            'internal_fn_b'))
    def inner(master_mock):
        assert master_mock
        ne_(internal_fn_a, internal_module.internal_fn_a)
        ne_(internal_fn_b, internal_module.internal_fn_b)
        eq_(external_fn_a, external_module.external_fn_a)
        eq_(external_fn_b, external_module.external_fn_b)

    internal_fn_a = internal_module.internal_fn_a
    internal_fn_b = internal_module.internal_fn_b
    external_fn_a = external_module.external_fn_a
    external_fn_b = external_module.external_fn_b

    inner()  # pylint: disable=E1120

    eq_(internal_fn_a, internal_module.internal_fn_a)
    eq_(internal_fn_b, internal_module.internal_fn_b)
    eq_(external_fn_a, external_module.external_fn_a)
    eq_(external_fn_b, external_module.external_fn_b)


@raises(RuntimeError)
def test_patch_with_no_internal():
    @patch(
        module=internal_module,
        external=(
            'simian.test.my_package.external_module.external_fn_a',
            'simian.test.my_package.external_module.external_fn_b'))
    def inner(master_mock):
        try:
            internal_module.my_fn()
        except RuntimeError as e:
            eq_(str(e), 'called internal_fn_a()')
            eq_(master_mock.mock_calls, [
                call.external_fn_a(),
                call.external_fn_b()])
            raise
    inner()  # pylint: disable=E1120


def test_patch_with_internal_restores_targets():
    @patch(
        module=internal_module,
        external=(
            'simian.test.my_package.external_module.external_fn_a',
            'simian.test.my_package.external_module.external_fn_b'),
        internal=(
            'internal_fn_a',
            'internal_fn_b'))
    def inner(master_mock):
        internal_module.my_fn()
        eq_(master_mock.mock_calls, [
            call.external_fn_a(),
            call.external_fn_b(),
            call.internal_fn_a(),
            call.internal_fn_b()])

    inner()  # pylint: disable=E1120

    @raises(RuntimeError)
    def ensure_target_unpatched(target):
        target()

    ensure_target_unpatched(external_module.external_fn_a)
    ensure_target_unpatched(external_module.external_fn_b)
    ensure_target_unpatched(internal_module.internal_fn_a)
    ensure_target_unpatched(internal_module.internal_fn_b)


def test_patch_with_test_generator_targets():
    @patch(
        module=internal_module,
        external=(
            'simian.test.my_package.external_module.external_fn_a',
            'simian.test.my_package.external_module.external_fn_b'),
        internal=(
            'internal_fn_a',
            'internal_fn_b'))
    def inner(master_mock):
        internal_module.my_fn()
        eq_(master_mock.mock_calls, [
            call.external_fn_a(),
            call.external_fn_b(),
            call.internal_fn_a(),
            call.internal_fn_b()])

    yield inner
    yield inner


@raises(RuntimeError)
def test_patch_with_no_internal_no_external():
    @patch(module=internal_module)
    def inner(master_mock):
        try:
            internal_module.my_fn()
        except RuntimeError as e:
            eq_(str(e), 'called external_fn_a()')
            eq_(master_mock.mock_calls, [])
            raise
    inner()  # pylint: disable=E1120


def test_patch_with_generated_targets():
    external_format = 'simian.test.my_package.external_module.external_fn_{c}'
    internal_format = 'internal_fn_{c}'

    # noinspection PyUnresolvedReferences
    @patch(
        module=internal_module,
        external=(external_format.format(c=c) for c in 'ab'),
        internal=(internal_format.format(c=c) for c in 'ab'))
    def inner(master_mock):
        internal_module.my_fn()
        eq_(master_mock.mock_calls, [
            call.external_fn_a(),
            call.external_fn_b(),
            call.internal_fn_a(),
            call.internal_fn_b()])
    inner()  # pylint: disable=E1120


@raises(RuntimeError)
def test_no_patch():
    try:
        internal_module.my_fn()
    except RuntimeError as e:
        eq_(str(e), 'called external_fn_a()')
        raise


#
# Test Helpers
#

def ne_(a, b, msg=None):
    if a == b:
        raise AssertionError(
            msg or "{a!r} == {b!r}".format(a=a, b=b))  # pragma: no cover
