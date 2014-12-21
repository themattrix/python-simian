def external_fn_a():
    raise RuntimeError('called external_fn_a()')


def external_fn_b():
    raise RuntimeError('called external_fn_b()')  # pragma: no cover
