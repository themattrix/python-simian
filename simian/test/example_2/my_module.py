from time import sleep


def my_sleep(duration_secs):
    my_logger('Starting {n}-second sleep'.format(n=duration_secs))
    sleep(duration_secs)
    my_logger('Finished {n}-second sleep'.format(n=duration_secs))


def my_logger(msg):
    print(msg)
