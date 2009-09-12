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


