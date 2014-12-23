from time import sleep


def my_sleep(duration_secs):
    print('Sleeping for {n} seconds'.format(n=duration_secs))
    sleep(duration_secs)
