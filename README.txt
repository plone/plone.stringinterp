Introduction
============

Provides ${id} style string interpolation using named adapters to look up
variables. This is meant to provide a trivially simple template system
for clients like plone.app.contentrules.

To interpolate a string in context, just follow the pattern::

    from plone.stringinterp.interfaces import IStringInterpolator
    
    IStringInterpolator(context)("Here is the title: ${title}")


Substitution of variables that are part of the Dublin Core are
provided with the package. To provide additional subsitutions, just
provide a named adapter implementing interfaces.IStringSubstitution
for your context. The adapter name is used for the lookup.


Implemented Substitutions
=========================

All Content
-----------

url


Minimal Dublin Core
-------------------

title
description
type (content type)


Workflow Aware
--------------

review_state


Dublin Core
-----------

creators
contributors
subject
format (mime type)
language
rights
identifier


Catalogable Dublin Core
-----------------------

Everything should be in long local time format

created
effective
expires
modified


Versioned
---------

comment (change comment)
prior_state (previous review_state)
principal (author of last change)