Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.3.3 (2020-09-07)
------------------

Bug fixes:


- Resolve deprecation warning [gforcada] (#14)


1.3.2 (2020-04-22)
------------------

Bug fixes:


- Minor packaging updates. (#1)


1.3.1 (2018-11-04)
------------------

Bug fixes:

- The ``Format`` accessor should actually return the ``format`` attribute
  (see plone/Products.CMFPlone#2540)
  [ale-rt]


1.3.0 (2018-09-28)
------------------

New features:

- Add support for Python 3.
  [pbauer]


1.2.1 (2016-11-18)
------------------

New features:

- Removed ZopeTestCase.  [maurits]


1.2 (2016-09-20)
----------------

New features:

- Provide a ContextWrapper adapter in order to easily pass custom messages
  to StringInterpoator
  [avoinea]


1.1.4 (2016-08-18)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.1.3 (2016-05-25)
------------------

Fixes:

- Adapt to changes in SimpleViewClass in zope4.
  [pbauer]

- Fix typo
  [staeff]

1.1.2 (2015-03-13)
------------------

Fixes:

- Fixed "RuntimeError: maximum recursion depth exceeded" in
  recursiveGetGroupUsers when you have a group A containing group B containing
  group A.
  [vincentfretin]


1.1.1 (2014-11-01)
------------------

- Add creator, creator_fullname, creator_email,
  creators_emails and contributors_emails
  [avoinea]


1.1 (2014-02-25)
----------------

- Add portal_url and portal_title.
  [thomasdesvenain]

- Add parent_id.
  [maartenkling]

- Convert tests to plone.app.testing for Plone 5.
  [davisagli]


1.0.10 (2013-05-30)
-------------------

- Added review_state_title substitution variable.
  [ichim-david]


1.0.9 (2013-05-26)
------------------

- Added id substitution variable
  that works with content events and user events.
  [thomasdesvenain]

- Email substitutions are not restricted to contentish anymore,
  so we can use them with user events.
  [thomasdesvenain]


1.0.8 (2013-05-23)
------------------

- Added editor_emails substitution variable.
  [thomasdesvenain]


1.0.7 (2012-08-11)
------------------

- Added parent_title substitution, which gets the title of the container.
  [thomasdesvenain]

- Fixed user_fullname substitution : display user id if fullname is not set.
  [thomasdesvenain]

- Do not restrict string interpolation to IContentish if not necessary.
  Fixes email content rule related with plone.app.discussion comments.
  Refs https://dev.plone.org/ticket/13047
  [thomasdesvenain]


1.0.6 (2012-08-04)
------------------

- Added parent_url substitution (the url of the object parent).
  [thomasdesvenain]


1.0.5 (2012-01-26)
------------------

- Recursive get members works in a non wrapped context
  (when getting PloneGroups instead of GroupData from GroupTool)
  [thomasdesvenain]

- Add MANIFEST.in
  [WouterVH]


1.0.4 - 2011-04-01
------------------

- Added contributor_emails and reader_emails substitution variables.
  [thomasdesvenain]


1.0.3 - 2010-11-11
------------------

- Fix a bug with member email substitutions when a user has been
  removed from acl_users.
  [rossp]


1.0.2 - 2010-09-20
------------------

- Role email substitution works with user that have role through a group.
  [thomasdesvenain]


1.0.1 - 2010-09-15
------------------

- Internationalized ${type} substitution.
  [thomasdesvenain]

- Fixed: get emails for role works with local roles.
  [thomasdesvenain]


1.0 - 2010-07-18
----------------

- Update license to GPL version 2 only.
  [hannosch]


1.0b1 - 2009-11-12
------------------

- Initial release.
