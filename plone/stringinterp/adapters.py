#!/usr/bin/env python
"""
adapters.py

Created by Steve McMahon on 2009-08-12.
Copyright (c) 2009 Plone Foundation.
"""

from AccessControl import Unauthorized
from AccessControl.interfaces import IRoleManager
from Acquisition import aq_get
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import Implicit
from plone.base import PloneMessageFactory as _
from plone.base.i18nl10n import ulocalized_time
from plone.base.utils import safe_text
from plone.memoize.request import memoize_diy_request
from plone.stringinterp.interfaces import IContextWrapper
from plone.stringinterp.interfaces import IStringSubstitution
from Products.CMFCore.interfaces import ICatalogableDublinCore
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IDublinCore
from Products.CMFCore.interfaces import IMinimalDublinCore
from Products.CMFCore.interfaces import IWorkflowAware
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.PlonePAS.interfaces.group import IGroupData
from zope.component import adapter
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface


@implementer(IContextWrapper)
class ContextWrapper(Implicit):
    """Wrapper for context"""

    def __init__(self, context):
        self.context = context

    def __call__(self, **kwargs):
        alsoProvides(self, IRoleManager)
        if IContentish.providedBy(self.context):
            alsoProvides(self, IContentish)
        if IMinimalDublinCore.providedBy(self.context):
            alsoProvides(self, IMinimalDublinCore)
        if IWorkflowAware.providedBy(self.context):
            alsoProvides(self, IWorkflowAware)
        if IDublinCore.providedBy(self.context):
            alsoProvides(self, IDublinCore)
        if ICatalogableDublinCore.providedBy(self.context):
            alsoProvides(self, ICatalogableDublinCore)

        for key, value in kwargs.items():
            setattr(self, key, value)
        return self.__of__(self.context)


@implementer(IStringSubstitution)
class BaseSubstitution:
    """Base substitution"""

    def __init__(self, context):
        if IContextWrapper.providedBy(context):
            self.wrapper = context
            self.context = aq_inner(self.wrapper.context)
        else:
            self.wrapper = None
            self.context = context

    # __call__ is a wrapper for the subclassed
    # adapter's actual substitution that makes sure we're
    # not generating unauth exceptions or returning non-unicode.
    def __call__(self):
        try:
            return safe_text(self.safe_call())
        except Unauthorized:
            return _("Unauthorized")


@adapter(IContentish)
class UrlSubstitution(BaseSubstitution):
    category = _("All Content")
    description = _("URL")

    def safe_call(self):
        return self.context.absolute_url()


@adapter(Interface)
class ParentIdSubstitution(BaseSubstitution):
    category = _("All Content")
    description = _("Identifier of the parent content or login of managed user")

    def safe_call(self):
        return aq_parent(self.context).getId()


@adapter(Interface)
class IdSubstitution(BaseSubstitution):
    category = _("All Content")
    description = _("Identifier of the content or login of managed user")

    def safe_call(self):
        return self.context.getId()


@adapter(IContentish)
class ParentUrlSubstitution(BaseSubstitution):
    category = _("All Content")
    description = _("Folder URL")

    def safe_call(self):
        return aq_get(aq_parent(self.context), "absolute_url")()


@adapter(IMinimalDublinCore)
class TitleSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Title")

    def safe_call(self):
        return self.context.Title()


@adapter(IContentish)
class ParentTitleSubstitution(BaseSubstitution):
    category = _("All Content")
    description = _("Parent title")

    def safe_call(self):
        return aq_get(aq_parent(self.context), "Title")()


@adapter(IMinimalDublinCore)
class DescriptionSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Description")

    def safe_call(self):
        return self.context.Description()


@adapter(IMinimalDublinCore)
class TypeSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Content Type")

    def safe_call(self):
        return translate(self.context.Type(), context=self.context.REQUEST)


@adapter(IDublinCore)
class CreatorSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Creator Id")

    def safe_call(self):
        for creator in self.context.listCreators():
            return creator
        return ""


@adapter(IContentish)
class CreatorFullNameSubstitution(CreatorSubstitution):
    category = _("Dublin Core")
    description = _("Creator Full Name")

    def safe_call(self):
        creator = super().safe_call()
        if not creator:
            return ""

        pm = getToolByName(self.context, "portal_membership")
        member = pm.getMemberById(creator)
        if not member:
            return creator

        fname = member.getProperty("fullname", None)
        if not fname:
            return creator
        return fname


@adapter(IDublinCore)
class CreatorEmailSubstitution(CreatorSubstitution):
    category = _("Dublin Core")
    description = _("Creator E-Mail")

    def safe_call(self):
        creator = super().safe_call()
        if not creator:
            return ""
        pm = getToolByName(self.context, "portal_membership")
        member = pm.getMemberById(creator)
        if not member:
            return ""
        email = member.getProperty("email", "")
        if not email:
            return ""
        return email


@adapter(IDublinCore)
class CreatorsSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Creators Ids")

    def safe_call(self):
        return ", ".join(self.context.listCreators())


@adapter(IDublinCore)
class CreatorsEmailsSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Creators E-Mails")

    def safe_call(self):
        creators = self.context.listCreators()
        pm = getToolByName(self.context, "portal_membership")
        emails = []
        for creator in creators:
            member = pm.getMemberById(creator)
            if not member:
                continue
            email = member.getProperty("email", None)
            if not email:
                continue
            emails.append(email)
        return ", ".join(emails)


@adapter(IDublinCore)
class ContributorsSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Contributors Ids")

    def safe_call(self):
        return ", ".join(self.context.listContributors())


@adapter(IDublinCore)
class ContributorsEmailsSubstitution(BaseSubstitution):
    category = "Dublin Core"
    description = _("Contributors E-Mails")

    def safe_call(self):
        contributors = self.context.listContributors()
        pm = getToolByName(self.context, "portal_membership")
        emails = []
        for contributor in contributors:
            member = pm.getMemberById(contributor)
            if not member:
                continue
            email = member.getProperty("email", None)
            if not email:
                continue
            emails.append(email)
        return ", ".join(emails)


@adapter(IDublinCore)
class SubjectSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Subject")

    def safe_call(self):
        return ", ".join(self.context.Subject())


@adapter(IDublinCore)
class FormatSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Format")

    def safe_call(self):
        return self.context.Format()


@adapter(IDublinCore)
class LanguageSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Language")

    def safe_call(self):
        return self.context.Language()


@adapter(IDublinCore)
class IdentifierSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Identifier, actually URL of the content")

    def safe_call(self):
        return self.context.Identifier()


@adapter(IDublinCore)
class RightsSubstitution(BaseSubstitution):
    category = _("Dublin Core")
    description = _("Rights")

    def safe_call(self):
        return self.context.Rights()


@adapter(IWorkflowAware)
class ReviewStateSubstitution(BaseSubstitution):
    category = _("Workflow")
    description = _("Review State")

    def safe_call(self):
        wft = getToolByName(self.context, "portal_workflow")
        return wft.getInfoFor(self.context, "review_state")


@adapter(IWorkflowAware)
class ReviewStateTitleSubstitution(BaseSubstitution):
    category = _("Workflow")
    description = _("Review State Title")

    def safe_call(self):
        wft = getToolByName(self.context, "portal_workflow")
        review_state = wft.getInfoFor(self.context, "review_state")
        return _(wft.getTitleForStateOnType(review_state, self.context.portal_type))


class DateSubstitution(BaseSubstitution):
    def formatDate(self, adate):
        try:
            return safe_text(
                ulocalized_time(adate, long_format=True, context=self.context)
            )
        except ValueError:
            return "???"


@adapter(ICatalogableDublinCore)
class CreatedSubstitution(DateSubstitution):
    category = _("Dublin Core")
    description = _("Date Created")

    def safe_call(self):
        return self.formatDate(self.context.created())


@adapter(ICatalogableDublinCore)
class EffectiveSubstitution(DateSubstitution):
    category = _("Dublin Core")
    description = _("Date Effective")

    def safe_call(self):
        return self.formatDate(self.context.effective())


@adapter(ICatalogableDublinCore)
class ExpiresSubstitution(DateSubstitution):
    category = _("Dublin Core")
    description = _("Date Expires")

    def safe_call(self):
        return self.formatDate(self.context.expires())


@adapter(ICatalogableDublinCore)
class ModifiedSubstitution(DateSubstitution):
    category = _("Dublin Core")
    description = _("Date Modified")

    def safe_call(self):
        return self.formatDate(self.context.modified())


# A base class for adapters that need member information
@adapter(IContentish)
class MemberSubstitution(BaseSubstitution):
    def __init__(self, context):
        super().__init__(context)
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
                pset.add(prop)
        return pset

    def getPropsForIds(self, ids, propname):
        return self.getPropsForMembers(self.getMembersFromIds(ids), propname)


# A base class for all the role to email list adapters
@adapter(IContentish)
class MailAddressSubstitution(MemberSubstitution):
    def getEmailsForRole(self, role):
        portal = getSite()
        acl_users = getToolByName(portal, "acl_users")

        # get a set of ids of members with the global role
        ids = {p[0] for p in acl_users.portal_role_manager.listAssignedPrincipals(role)}

        # union with set of ids of members with the local role
        ids |= {
            id
            for id, irole in acl_users._getAllLocalRoles(self.context).items()
            if role in irole
        }

        # get members from group or member ids
        members = _recursiveGetMembersFromIds(portal, ids)

        # get emails
        return ", ".join(self.getPropsForMembers(members, "email"))


def _recursiveGetMembersFromIds(portal, group_and_user_ids):
    """get members from a list of group and member ids"""

    gtool = getToolByName(portal, "portal_groups")
    mtool = getToolByName(portal, "portal_membership")
    members = set()
    seen = set()

    def recursiveGetGroupUsers(mtool, gtool, seen, group):
        users = set()
        if IGroupData.providedBy(group):
            group_members = group.getGroupMembers()
        else:
            group_members = [mtool.getMemberById(m) for m in group.getMemberIds()]

        for group_or_user in group_members:
            if IGroupData.providedBy(group_or_user):
                group_or_user_id = group_or_user.getId()
                if group_or_user_id in seen:
                    continue

                seen.add(group_or_user_id)
                users = users.union(
                    recursiveGetGroupUsers(mtool, gtool, seen, group_or_user)
                )
            elif group_or_user is not None:
                # Other group data PAS plugins might not filter no
                # longer existing group members.
                users.add(group_or_user)

        return users

    for group_or_user_id in group_and_user_ids:
        _group = gtool.getGroupById(group_or_user_id)
        if _group:
            seen.add(group_or_user_id)
            members = members.union(recursiveGetGroupUsers(mtool, gtool, seen, _group))
        else:
            member = mtool.getMemberById(group_or_user_id)
            if member is not None:
                members.add(member)

    return members


class OwnerEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Owners E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Owner")


class ReviewerEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Reviewers E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Reviewer")


class ReaderEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Readers E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Reader")


class ContributorEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Contributors E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Contributor")


class EditorEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Editors E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Editor")


class ManagerEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Managers E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Manager")


class MemberEmailSubstitution(MailAddressSubstitution):
    category = _("Local Roles")
    description = _("Members E-Mails")

    def safe_call(self):
        return self.getEmailsForRole("Member")


@adapter(IContentish)
class UserEmailSubstitution(BaseSubstitution):
    category = _("Current User")
    description = _("E-Mail Address")

    def safe_call(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                email = user.getProperty("email", None)
                if email:
                    return email
        return ""


@adapter(IContentish)
class UserFullNameSubstitution(BaseSubstitution):
    category = _("Current User")
    description = _("Full Name")

    def safe_call(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                fname = user.getProperty("fullname", None)
                if fname:
                    return fname
                else:
                    return user.getId()

        return ""


@adapter(IContentish)
class UserIdSubstitution(BaseSubstitution):
    category = _("Current User")
    description = _("Id")

    def safe_call(self):
        pm = getToolByName(self.context, "portal_membership")
        if not pm.isAnonymousUser():
            user = pm.getAuthenticatedMember()
            if user is not None:
                return user.getId()
        return ""


# memoize on the request an expensive function called by the
# ChangeSubstitution class.
@memoize_diy_request()
def _lastChange(request, context):
    workflow_change = _lastWorkflowChange(context)
    last_revision = _lastRevision(context)
    if not workflow_change:
        return last_revision
    elif not last_revision:
        return workflow_change

    if (
        workflow_change
        and last_revision
        and workflow_change.get("time") > last_revision.get("time")
    ):
        return workflow_change

    return last_revision


def _lastWorkflowChange(context):
    workflow = getToolByName(context, "portal_workflow")
    try:
        review_history = workflow.getInfoFor(context, "review_history")
    except WorkflowException:
        return {}

    # filter out automatic transitions.
    review_history = [r for r in review_history if r["action"]]

    if review_history:
        r = review_history[-1]
        r["type"] = "workflow"
        r["transition_title"] = workflow.getTitleForTransitionOnType(
            r["action"], context.portal_type
        )
        r["actorid"] = r["actor"]
    else:
        r = {}

    return r


def _lastRevision(context):
    context = aq_inner(context)
    rt = getToolByName(context, "portal_repository")
    if rt.isVersionable(context):
        history = rt.getHistoryMetadata(context)
        if history:
            # history = ImplicitAcquisitionWrapper(history, pa)
            meta = history.retrieve(
                history.getLength(countPurged=False) - 1,
                countPurged=False,
            )["metadata"]["sys_metadata"]
            return dict(
                type="versioning",
                action=_("edit"),
                transition_title=_("Edit"),
                actorid=meta["principal"],
                time=meta["timestamp"],
                comments=meta["comment"],
                review_state=meta["review_state"],
            )

    return {}


# a base class for substitutions that use
# last revision or workflow information
class ChangeSubstitution(BaseSubstitution):
    def lastChangeMetadata(self, id):
        return _lastChange(self.context.REQUEST, self.context).get(id, "")


@adapter(IContentish)
class LastChangeCommentSubstitution(ChangeSubstitution):
    category = _("History")
    description = _("Comment")

    def safe_call(self):
        return self.lastChangeMetadata("comments")


@adapter(IContentish)
class LastChangeTitleSubstitution(ChangeSubstitution):
    category = _("History")
    description = _("Transition title")

    def safe_call(self):
        return self.lastChangeMetadata("transition_title")


@adapter(IContentish)
class LastChangeTypeSubstitution(ChangeSubstitution):
    category = _("History")
    description = _("Change type")

    def safe_call(self):
        return self.lastChangeMetadata("type")


@adapter(IContentish)
class LastChangeActorIdSubstitution(ChangeSubstitution):
    category = _("History")
    description = _("Change author")

    def safe_call(self):
        return self.lastChangeMetadata("actorid")


class PortalSubstitution(BaseSubstitution):
    category = _("Portal")

    def __init__(self, context):
        BaseSubstitution.__init__(self, context)
        self.portal = getToolByName(self.context, "portal_url").getPortalObject()


class PortalURLSubstitution(PortalSubstitution):
    description = _("Portal URL")

    def safe_call(self):
        return self.portal.absolute_url()


class PortalTitleSubstitution(PortalSubstitution):
    description = _("Portal title")

    def safe_call(self):
        return self.portal.Title()
