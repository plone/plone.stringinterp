#!/usr/bin/env python
# encoding: utf-8
"""
interfaces.py

Created by Steve McMahon on 2009-08-12.
Copyright (c) 2009 Plone Foundation.
"""

from zope.interface import Interface


class IStringSubstitution(Interface):
    """
        provides callable returning the substitution

        if you would like your substitution listed
        in lists, provide name, description and category
        class attributes
    """

    def __call__():
        """
            return substitution
        """


class IStringInterpolator(Interface):
    """
        provides callable returning
        interpolated string
    """

    def __call__():
        """
            return interpolated string
        """


class IStringSubstitutionInfo(Interface):
    """
      provides information on available IStringSubstitution adapters
    """

    def substitutionList():
        """
        returns sequence:
        [ (categoryTitle,
          [{'id':subId, 'description':subDescription}, ...]), ...  ]
        """

class IContextWrapper(Interface):
    """
        Wrap context in order to be able to provide custom strings
        not stored on context

        Usage:

        >>> wrapper = IContextWrapper(obj)(m1='A message', m2="Another one")
        >>> notify(CustomEvent(wrapper))
    """

    def __call__(kwargs):
        """"
           Return wrapped context
        """
