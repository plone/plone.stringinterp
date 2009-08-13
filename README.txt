Introduction
============

Provides ${id} style string interpolation using named adapters to look up
variables. This is meant to provide a trivially simple template system
for clients like plone.app.contentrules.

To interpolate a string in context, just follow the pattern::

    from plone.stringinterp import Interpolate
    
    Interpolate(context, "Here is the title: ${title}")()


Substitution of variables that are part of the Minimal Dublin Core are
provided with the package. To provide additional subsitutions, just
provide a named adapter implementing interfaces.IStringSubstitution
for your context. The adapter name is used for the lookup.



