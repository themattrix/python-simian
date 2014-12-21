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
