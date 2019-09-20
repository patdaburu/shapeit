#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from shapeit.srs import by_srid, InvalidSrException


@pytest.mark.parametrize(
    'srid,authority,valid',
    [
        (4326, None, True),
        (666, None, False)
    ]
)
def test_by_srid(srid, authority, valid):
    """
    Arrange/Act: Retrieve a spatial reference (`Sr`) using the `by_srid()`
        function.
    Assert: A valid SRID and authority returns a proper spatial reference.  An
        invalid SRID-authority combination raises an exception.

    :param srid: the SRID
    :param authority: the authority (`None` to use the default)
    :param valid: `True` if we expect the SRID to be valid
    """
    args = {
        k: v for k, v in {
            'srid': srid,
            'authority': authority
        }.items() if v is not None
    }
    if valid:
        _sr = by_srid(**args)
        assert _sr.srid == srid
    else:
        with pytest.raises(InvalidSrException):
            by_srid(**args)
