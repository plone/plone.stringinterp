#!/usr/bin/env python
# encoding: utf-8
"""
adapters.py

Created by Steve McMahon on 2009-08-12.
Copyright (c) 2009 Plone Foundation.
"""

from zope.interface import implements
from zope.component import adapts

from Acquisition import ImplicitAcquisitionWrapper

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import \
    IContentish, IMinimalDublinCore, IWorkflowAware, IDublinCore, \
    ICatalogableDublinCore

from Products.CMFEditions.interfaces import IVersioned

from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.i18nl10n import ulocalized_time

from interfaces import IStringSubstitution

from plone.stringinterp import _


class BaseSubstitution(object):
    implements(IStringSubstitution)
    
    def __init__(self, context):
        self.context = context


class UrlSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    category = _(u'All Content')
    description = _(u'URL')
    
    def __call__(self):
        return self.context.absolute_url()


class TitleSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Title')

    def __call__(self):
        return safe_unicode(self.context.Title())


class DescriptionSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Description')

    def __call__(self):
        return safe_unicode(self.context.Description())


class TypeSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Content Type')

    def __call__(self):
        return self.context.Type()

class CreatorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Creators')

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listCreators()) )


class ContributorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Contributors')

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listContributors()) )


class SubjectSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Subject')

    def __call__(self):
        return safe_unicode( ', '.join(self.context.Subject()) )
#


class FormatSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Format')

    def __call__(self):
        return safe_unicode( self.context.Format() )
#


class LanguageSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Language')

    def __call__(self):
        return safe_unicode( self.context.Language() )
#


class IdentifierSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Identifier')

    def __call__(self):
        return safe_unicode( self.context.Identifier() )
#


class RightsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Rights')

    def __call__(self):
        return safe_unicode( self.context.Rights() )
#


class ReviewStateSubstitution(BaseSubstitution):
    adapts(IWorkflowAware)
    
    category = _(u'Workflow')
    description = _(u'Review State')

    def __call__(self):
        wft = getToolByName(self.context, 'portal_workflow')
        return safe_unicode(wft.getInfoFor(self.context, 'review_state'))


class DateSubstitution(BaseSubstitution):

    def formatDate(self, adate):
        try:
            return safe_unicode(
               ulocalized_time(adate, long_format=True, context=self.context)
            )
        except ValueError:
            return u'???'


class CreatedSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)
    
    category = _(u'Dublin Core')
    description = _(u'Date Created')

    def __call__(self):
        return self.formatDate(self.context.created())


class EffectiveSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Date Effective')

    def __call__(self):
        return self.formatDate(self.context.effective())


class ExpiresSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Date Expires')

    def __call__(self):
        return self.formatDate(self.context.expires())


class ModifiedSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

    category = _(u'Dublin Core')
    description = _(u'Date Modified')

    def __call__(self):
        return self.formatDate(self.context.modified())


class VersionedSubstitution(BaseSubstitution):
    adapts(IVersioned)
    
    def getMetadata(self, item):
        pr = getToolByName(self.context, 'portal_repository')
        pa = getToolByName(self.context, 'portal_archivist')
        
        if pr.isVersionable(self.context):          
            history = pa.getHistoryMetadata(self.context)
            if history:
                history = ImplicitAcquisitionWrapper(history, pa)
                metadata = history.retrieve(history.getLength(countPurged=False)-1, countPurged=False)['metadata']['sys_metadata']
                return safe_unicode(metadata.get(item, u'???'))
        return u'???'

#

class ChangeCommentSubstitution(VersionedSubstitution):
    
    category = _(u'Versioning')
    description = _(u'Change Comment')

    def __call__(self):
        return self.getMetadata('comment')
        
#

class PriorStateSubstitution(VersionedSubstitution):
    
    category = _(u'Versioning')
    description = _(u'Prior State')

    def __call__(self):
        return self.getMetadata('review_state')
        
#

class PrincipalSubstitution(VersionedSubstitution):
    
    category = _(u'Versioning')
    description = _(u'Changed By')

    def __call__(self):
        return self.getMetadata('principal')
        
#


# A base class for adapters that need member information
class MemberSubstitution(BaseSubstitution):
    adapts(IContentish)

    def __init__(self, context):
        self.context = context
        self.mtool = getToolByName(self.context, "portal_membership")
        self.gtool = getToolByName(self.context, "portal_groups")

    def getMembersFromIds(self, ids):
        members = set()
        for id in ids:
            member = self.mtool.getMemberById(id)
            if member is not None:
                members.add(member)
            else:
                # id may be for a group
                group = self.gtool.getGroupById(id)
                if group is not None:
                    members = members.union(group.getGroupMembers())
        return members
    
    def getPropsForMembers(self, members, propname):
        pset = set()
        for member in members:
            prop = member.getProperty(propname, None)
            if prop:
                pset.add(safe_unicode(prop))
        return pset
        
    def getPropsForIds(self, ids, propname):
        return self.getPropsForMembers(self.getMembersFromIds(ids), propname)


# A base class for all the role->email list adapters
class MailAddressSubstitution(MemberSubstitution):
    adapts(IContentish)
    
    def getEmailsForRole(self, role):
        
        acl_users = getToolByName(self.context, "acl_users")

        # get a set of ids of members with the global role
        ids = set(acl_users.portal_role_manager.listAssignedPrincipals(role))

        # union with set of ids of members with the local role
        ids |= set([id for id, irole 
                       in acl_users._getAllLocalRoles(self.context).items()
                       if irole == role])

        return u', '.join(self.getPropsForIds(ids, 'email'))

# 


class OwnerEmailSubstitution(MailAddressSubstitution):
    
    category = _(u'E-Mail Addresses')
    description = _(u'Owners')

    def __call__(self):
        return self.getEmailsForRole('Owner')
        
#


class ReviewerEmailSubstitution(MailAddressSubstitution):
    
    category = _(u'E-Mail Addresses')
    description = _(u'Reviewers')

    def __call__(self):
        return self.getEmailsForRole('Reviewer')
        
#


class ManagerEmailSubstitution(MailAddressSubstitution):
    
    category = _(u'E-Mail Addresses')
    description = _(u'Managers')

    def __call__(self):
        return self.getEmailsForRole('Manager')
        
#


class MemberEmailSubstitution(MailAddressSubstitution):
    
    category = _(u'E-Mail Addresses')
    description = _(u'Members')

    def __call__(self):
        return self.getEmailsForRole('Member')
        
#


class UserEmailSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    category = _(u'Current User')
    description = _(u'E-Mail Address')
    
    def __call__(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                email = user.getProperty('email', None)
                if email:
                    return safe_unicode(email)
        return u''
#


class UserFullNameSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    category = _(u'Current User')
    description = _(u'Full Name')
    
    def __call__(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                fname = user.getProperty('fullname', None)
                if fname:
                    return safe_unicode(fname)
        return u''
#


class UserIdSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    category = _(u'Current User')
    description = _(u'Id')
    
    def __call__(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                return safe_unicode(user.getId())
        return u''
#
