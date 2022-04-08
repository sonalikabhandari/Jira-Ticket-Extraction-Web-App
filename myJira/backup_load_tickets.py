from django.core.management.base import BaseCommand
from myJira.models import JiraTicket
from django.conf import settings
import os
from jira import JIRA
from CM_jira_tickets import settings

# username = os.environ.get('username')
# password = os.environ.get('password')
jira = JIRA(options={'server':'https://jira.charter.com', 'verify': False}, basic_auth=(settings.username, settings.password)) ## put this in settings.py file
# jql = "Project = CBOBBCM AND created > startOfYear()"

field_list = [
            'created',
            'status',
            'summary',
            'assignee',
            'issuelinks'
        ]


class Command(BaseCommand):
    help = "Insert Jira Tickets into database"

    def handle(self, *args, **options):

        self.stdout.write("Cleaning database...")
        JiraTicket.objects.all().delete()

        self.stdout.write("Generating Tickets")

        block_size = 200
        block_num = 0
        while True:
            start_idx = block_num*block_size
            issues = jira.search_issues(settings.jql,startAt=start_idx, maxResults=block_size,  fields=field_list )
            if len(issues) == 0:
                break
            block_num += 1
            for issue in issues:
                # jiraticket = JiraTicket(key=issue.key)

                jiraticket, created  = JiraTicket.objects.get_or_create(key=issue.key )
                jiraticket.Summary=issue.fields.summary
                jiraticket.status=issue.fields.status.name
                jiraticket.assignee=issue.fields.assignee.displayName
                jiraticket.created=issue.fields.created
                jiraticket.save()
                for link in issue.fields.issuelinks:
                    if hasattr(link, "outwardIssue"):
                        new_link, created = JiraTicket.objects.get_or_create(key=link.outwardIssue.key)
                        # do your if ticket is cbobbippd or cbobboppd and collect all your fields, status here
                        jiraticket.links.add(new_link)
                        linked_issue = jira.issue(new_link.key, fields=field_list)
                        if (new_link.key.startswith('CBOBBIPPD')):
                            if linked_issue.fields.status is not None:
                                new_link.status = linked_issue.fields.status.name
                            if linked_issue.fields.summary is not None:
                                new_link.Summary = linked_issue.fields.summary
                            if linked_issue.fields.assignee is not None:
                                new_link.assignee = linked_issue.fields.assignee.displayName
                            if linked_issue.fields.created is not None:
                                new_link.created = linked_issue.fields.created
                            new_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "outwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.outwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "inwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.inwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()




                            # for link in linked_issue.fields.issuelinks:
                            #     if hasattr(link, "outwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.outwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                            #     if hasattr(link, "inwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.inwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                        if (new_link.key.startswith('CBOBBOPPD')):
                            if linked_issue.fields.status is not None:
                                new_link.status = linked_issue.fields.status.name
                            if linked_issue.fields.summary is not None:
                                new_link.Summary = linked_issue.fields.summary
                            if linked_issue.fields.assignee is not None:
                                new_link.assignee = linked_issue.fields.assignee.displayName
                            if linked_issue.fields.created is not None:
                                new_link.created = linked_issue.fields.created
                            new_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "outwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.outwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "inwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.inwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()
                            # for link in linked_issue.fields.issuelinks:
                            #     if hasattr(link, "outwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.outwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                            #     if hasattr(link, "inwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.inwardIssue.key)
                            #         jiraticket.links.add(new_link_link)

                        # new_link.key, new_link_status etc
                    if hasattr(link, "inwardIssue"):
                        new_link, created = JiraTicket.objects.get_or_create(key=link.inwardIssue.key)
                        jiraticket.links.add(new_link)
                        linked_issue = jira.issue(new_link.key, fields=field_list)
                        if (new_link.key.startswith('CBOBBIPPD')):
                            if linked_issue.fields.status is not None:
                                new_link.status = linked_issue.fields.status.name
                            if linked_issue.fields.summary is not None:
                                new_link.Summary = linked_issue.fields.summary
                            if linked_issue.fields.assignee is not None:
                                new_link.assignee = linked_issue.fields.assignee.displayName
                            if linked_issue.fields.created is not None:
                                new_link.created = linked_issue.fields.created
                            new_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "inwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.inwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "outwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.outwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()
                            # for link in linked_issue.fields.issuelinks:
                            #     if hasattr(link, "outwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.outwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                            #     if hasattr(link, "inwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.inwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                        if (new_link.key.startswith('CBOBBOPPD')):
                            if linked_issue.fields.status is not None:
                                new_link.status = linked_issue.fields.status.name
                            if linked_issue.fields.summary is not None:
                                new_link.Summary = linked_issue.fields.summary
                            if linked_issue.fields.assignee is not None:
                                new_link.assignee = linked_issue.fields.assignee.displayName
                            if linked_issue.fields.created is not None:
                                new_link.created = linked_issue.fields.created
                            new_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "inwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.inwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()

                            for associated_link in linked_issue.fields.issuelinks:
                                if hasattr(associated_link, "outwardIssue"):
                                    child_link, created = JiraTicket.objects.get_or_create(key=associated_link.outwardIssue.key)
                                    new_link.links.add(child_link)
                                    child_linked_issue = jira.issue(child_link.key, fields=field_list)
                                    if child_linked_issue.fields.summary is not None:
                                        child_link.Summary = child_linked_issue.fields.summary
                                    if child_linked_issue.fields.status is not None:
                                        child_link.status = child_linked_issue.fields.status.name
                                    if child_linked_issue.fields.assignee is not None:
                                        child_link.assignee = child_linked_issue.fields.assignee.displayName
                                    if child_linked_issue.fields.created is not None:
                                        child_link.created = child_linked_issue.fields.created
                                    child_link.save()
                            # for link in linked_issue.fields.issuelinks:
                            #     if hasattr(link, "outwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.outwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                            #     if hasattr(link, "inwardIssue"):
                            #         new_link_link, created = JiraTicket.objects.get_or_create(key=link.inwardIssue.key)
                            #         jiraticket.links.add(new_link_link)
                #jiraticket.links.add(link.inwardIssue.key if hasattr(link, "inwardIssue") else link.outwardIssue.key for link in issue.fields.issuelinks)
    # for e in Entry.objects.all():
    #     print(e.headline)
        Ticket_count = JiraTicket.objects.filter(key__istartswith='cbobbcm').count()

        self.stdout.write(
            self.style.SUCCESS(f'Inserted {Ticket_count} Tickets')
        )
