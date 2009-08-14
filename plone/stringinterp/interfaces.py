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


class IStringInterpolator(Interface):
    """
        provides callable returning
        interpolated string
    """

    def __call__(s):
        """
            return interpolated string
        """
