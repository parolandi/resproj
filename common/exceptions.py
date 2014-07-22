
def assertThrow(true_expected):
    if not true_expected:
        raise BaseException()
    