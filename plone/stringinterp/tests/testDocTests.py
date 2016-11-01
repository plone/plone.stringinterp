from plone.testing import layered
# from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.contenttypes.testing import (
    PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING
)
import doctest
import unittest


testfiles = (
    'substitutionTests.txt',
    'moreSubstitutionTests.txt',''
    'wrapperTests.txt',
    'interpolationTests.txt',
)


def test_suite():
    return unittest.TestSuite([
        layered(doctest.DocFileSuite(
            f, package='plone.stringinterp.tests',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
                layer=PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING)
                for f in testfiles
        ])
