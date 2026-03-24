from plone.stringinterp.dollarReplace import LazyDict
from plone.stringinterp.interfaces import IStringSubstitution
from zope.component import provideAdapter
from zope.interface import implementer
from zope.interface import Interface

import unittest


class IDummyContent(Interface):
    pass


@implementer(IDummyContent)
class DummyContent:
    pass


@implementer(IStringSubstitution)
class GoodSubstitution:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        return "good value"


@implementer(IStringSubstitution)
class FailingSubstitution:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        raise RuntimeError("Adapter execution failed")


class TestLazyDict(unittest.TestCase):
    def setUp(self):
        provideAdapter(
            GoodSubstitution, (IDummyContent,), IStringSubstitution, name="good"
        )
        provideAdapter(
            FailingSubstitution, (IDummyContent,), IStringSubstitution, name="failing"
        )
        self.context = DummyContent()

    def test_good_substitution(self):
        lazy = LazyDict(self.context)
        self.assertEqual(lazy["good"], "good value")

    def test_missing_substitution_raises_keyerror(self):
        lazy = LazyDict(self.context)
        with self.assertRaises(KeyError):
            lazy["nonexistent"]

    def test_failing_adapter_does_not_crash(self):
        """An adapter that raises during execution should not crash.

        Regression test for
        https://github.com/plone/Products.CMFPlone/issues/1358
        """
        lazy = LazyDict(self.context)
        with self.assertRaises(KeyError):
            lazy["failing"]
