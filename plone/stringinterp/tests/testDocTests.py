import unittest
import doctest

from Testing import ZopeTestCase as ztc
from plone.app.testing.bbb import PloneTestCase

testfiles = (
    'substitutionTests.txt',
    'moreSubstitutionTests.txt',''
    'interpolationTests.txt',
)


# Use this to avoid having ZopeDocFileSuite pollute the main test class
class PloneStringinterpTestCase(PloneTestCase):
    pass


def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            f, package='plone.stringinterp.tests',
            test_class=PloneStringinterpTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)

            for f in testfiles
        ]
    )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
