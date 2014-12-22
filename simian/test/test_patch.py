from mock import call
from nose.tools import eq_, raises
from simian import patch
from simian.test.my_package import internal_module
from simian.test.my_package import external_module


def test_patch_with_multiple_arguments():
    @patch(
        module=internal_module,
        module_path='simian.test.my_package.internal_module',
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
    inner()


@raises(RuntimeError)
def test_patch_with_no_external():
    @patch(
        module=internal_module,
        module_path='simian.test.my_package.internal_module',
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
    inner()


@raises(ValueError)
def test_patch_with_internal_but_no_module_path():
    try:
        @patch(
            module=internal_module,
            internal=(
                'internal_fn_a',
                'internal_fn_b'))
        def never_called(master_mock):
            assert not master_mock  # pragma: no cover
        assert never_called         # pragma: no cover
    except ValueError as e:
        eq_(str(e), '"module_path" must be set for "internal" targets')
        raise


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
    inner()


def test_patch_with_internal_restores_targets():
    @patch(
        module=internal_module,
        module_path='simian.test.my_package.internal_module',
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

    @raises(RuntimeError)
    def ensure_target_unpatched(target):
        target()

    inner()

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
        module_path='simian.test.my_package.internal_module',
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
    inner()


@raises(RuntimeError)
def test_no_patch():
    try:
        internal_module.my_fn()
    except RuntimeError as e:
        eq_(str(e), 'called external_fn_a()')
        raise
