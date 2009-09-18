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


class BaseSubstitution(object):
    implements(IStringSubstitution)

    def __init__(self, context):
        self.context = context


class UrlSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    def __call__(self):
        return self.context.absolute_url()


class TitleSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return safe_unicode(self.context.Title())


class DescriptionSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return safe_unicode(self.context.Description())


class TypeSubstitution(BaseSubstitution):
    adapts(IMinimalDublinCore)

    def __call__(self):
        return self.context.Type()

class CreatorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listCreators()) )


class ContributorsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.listContributors()) )


class SubjectSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( ', '.join(self.context.Subject()) )
#


class FormatSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Format() )
#


class LanguageSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Language() )
#


class IdentifierSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Identifier() )
#


class RightsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    def __call__(self):
        return safe_unicode( self.context.Rights() )
#


class ReviewStateSubstitution(BaseSubstitution):
    adapts(IWorkflowAware)
    
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
    
    def __call__(self):
        return self.formatDate(self.context.created())


class EffectiveSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

    def __call__(self):
        return self.formatDate(self.context.effective())


class ExpiresSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

    def __call__(self):
        return self.formatDate(self.context.expires())


class ModifiedSubstitution(DateSubstitution):
    adapts(ICatalogableDublinCore)

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
    
    def __call__(self):
        return self.getMetadata('comment')
        
#

class PriorStateSubstitution(VersionedSubstitution):
    
    def __call__(self):
        return self.getMetadata('review_state')
        
#

class PrincipalSubstitution(VersionedSubstitution):
    
    def __call__(self):
        return self.getMetadata('principal')
        
#


# A base class for all the role->email list adapters
class MailAddressSubstitution(BaseSubstitution):
    adapts(IContentish)
    
    def getEmailsForRole(self, role):
        # Returns a list of emails for users having the specified role.
        # Thanks to Christophe Bosse and Cyrille Lebeaupin
        # for demonstrating that this is a great application for sets.
        
        mtool = getToolByName(self.context, "portal_membership")
        gtool = getToolByName(self.context, "portal_groups")
        acl_users = getToolByName(self.context, "acl_users")

        # get a set of ids of members with the global role
        ids = set(acl_users.portal_role_manager.listAssignedPrincipals(role))

        # union with set of ids of members with the local role
        ids |= set([id for id, irole 
                       in acl_users._getAllLocalRoles(self.context).items()
                       if irole == role])

        members = set()
        for id in ids:
            member = mtool.getMemberById(id)
            if member is not None:
                members.add(member)
            else:
                # id may be for a group
                group = gtool.getGroupById(id)
                if group is not None:
                    members = members.union(group.getGroupMembers())
                
        emails = set()
        for member in members:
            email = member.getProperty('email', None)
            if email:
                emails.add(safe_unicode(email))
        
        return u', '.join(emails)

# 


class OwnerEmailSubstitution(MailAddressSubstitution):
    
    def __call__(self):
        return self.getEmailsForRole('Owner')
        
#


class ReviewerEmailSubstitution(MailAddressSubstitution):
    
    def __call__(self):
        return self.getEmailsForRole('Reviewer')
        
#


class ManagerEmailSubstitution(MailAddressSubstitution):
    
    def __call__(self):
        return self.getEmailsForRole('Manager')
        
#


class MemberEmailSubstitution(MailAddressSubstitution):
    
    def __call__(self):
        return self.getEmailsForRole('Member')
        
#


class UserEmailSubstitution(BaseSubstitution):
    adapts(IContentish)
    
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

