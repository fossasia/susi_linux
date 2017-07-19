import susi_python as susi


def test_response():
    response = susi.ask('Hi')

    assert response is not None

