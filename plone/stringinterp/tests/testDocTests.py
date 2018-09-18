from plone.testing import layered
# from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.contenttypes.testing import (
    PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING
)
import doctest
import re
import six
import unittest


testfiles = (
    'substitutionTests.txt',
    'moreSubstitutionTests.txt',''
    'wrapperTests.txt',
    'interpolationTests.txt',
)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite([
        layered(
            doctest.DocFileSuite(
                f,
                package='plone.stringinterp.tests',
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                checker=Py23DocChecker(),
            ),
            layer=PLONE_APP_CONTENTTYPES_INTEGRATION_TESTING,
            ) for f in testfiles
        ])
