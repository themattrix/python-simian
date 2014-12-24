import simian
from mock import call
from simian.test.example_2 import my_module


@simian.patch(my_module, external=['time.sleep'], internal=['my_logger'])
def test_my_sleep(master_mock):
    my_module.my_sleep(99)
    master_mock.assert_has_calls(
        calls=[
            call.my_logger('Starting 99-second sleep'),
            call.sleep(99),
            call.my_logger('Finished 99-second sleep')],
        any_order=False)
