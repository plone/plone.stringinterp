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
    """

    def __call__():
        """
            return substitution
        """

    # if you would like your substitution listed
    # in lists, provide name, description and category
    # class attributes



class IStringInterpolator(Interface):
    """
        provides callable returning
        interpolated string
    """

    def __call__(s):
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
        [ (categoryTitle, [{'id':subId, 'description':subDescription}, ...]), ...  ]
        """
