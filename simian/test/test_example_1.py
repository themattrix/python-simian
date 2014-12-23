import simian
from simian.test.example_1 import my_module


@simian.patch(my_module, external=['time.sleep'])
def test_my_sleep(master_mock):
    my_module.my_sleep(99)
    master_mock.sleep.assert_called_once_with(99)
