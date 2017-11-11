
def assert_throw(true_expected):
    if not true_expected:
        raise BaseException()
    