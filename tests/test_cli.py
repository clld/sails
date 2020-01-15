import pytest

from sails.__main__ import main


def test_initdb():
    with pytest.raises(SystemExit):
        main(args=['initdb', '-h'])
