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

Dependencies
============

Dependencies are all in the CMF* namespace, so this theoretically useful
outside Plone. It does use the 'plone' identifier for the message factory.


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


Member / Group Information for roles on content
-----------------------------------------------

owner_emails
reviewer_emails
manager_emails
member_emails
user_email

Current User Information
------------------------

user_fullname
user_id

Last Change (workflow or version) Information

change_comment
change_title
change_type
change_authorid
