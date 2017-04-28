from __nonstandard__ import nobreak_keyword

def test_nobreak():
    x = 1
    for i in range(3):
        x += 1
    nobreak:
        x = 42
    assert x == 42

    x = 1
    for i in range(3):
        if i == 1:
            break
    nobreak:
        x = 42
    assert x == 1
