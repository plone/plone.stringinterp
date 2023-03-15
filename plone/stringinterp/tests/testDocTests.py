from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING
from plone.testing import layered

import doctest
import unittest


testfiles = (
    "substitutionTests.txt",
    "moreSubstitutionTests.txt",
    "wrapperTests.txt",
    "interpolationTests.txt",
)


def test_suite():
    return unittest.TestSuite(
        [
            layered(
                doctest.DocFileSuite(
                    test_file,
                    package="plone.stringinterp.tests",
                    optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                ),
                layer=PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING,
            )
            for test_file in testfiles
        ]
    )
