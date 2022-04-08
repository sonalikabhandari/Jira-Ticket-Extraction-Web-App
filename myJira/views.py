from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import os
from .models import JiraTicket
from django.db.models import Prefetch
from django.db.models import Q
from .excel_utils import WriteToExcel
from .ip_excel_utils import ip_linked_WriteToExcel
from .op_excel_utils import op_linked_WriteToExcel
# from .final_utils import inclusive_WriteToExcel
# from .merge import merge
from django.http import HttpResponseRedirect
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


# Create your views here.

@login_required
def jira_detailed_view(request):
    obj = JiraTicket.objects.filter(key__istartswith="cbobbcm").prefetch_related(Prefetch('links', queryset= JiraTicket.objects.filter(Q(key__istartswith='cbobboppd')| Q(key__istartswith='cbobbippd')),to_attr = 'cm_linked_tickets'))

        # obj = JiraTicket.object.getall()
        # bbippd = JiraTicket.objects.get(JiraTicket.key).links.filter(key__icontains='bbippd')
        #
        # context = {
        # 'Object': obj
        # }




    Tickets = []


    yourdict = {}

    for Ticket in obj:
        bbip_links = [s.key for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBIPPD')]
        bbip_summary = [s.Summary for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBIPPD')]

        bbip_status = [s.status for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBIPPD')]
        bbip_assignee = [s.assignee for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBIPPD')]
        bbip_created = [s.created for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBIPPD')]

        bbop_links = [s.key for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBOPPD')]
        bbop_summary = [s.Summary for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBOPPD')]


        bbop_status = [s.status for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBOPPD')]
        bbop_assignee = [s.assignee for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBOPPD')]
        bbop_created = [s.created for s in Ticket.cm_linked_tickets if s.key.startswith('CBOBBOPPD')]


        yourdict.update({
                        'CBOBBCM_Key': Ticket.key,
                        'CBOBBCM_Summary':Ticket.Summary,
                        'CBOBBCM_Status': Ticket.status,
                        'CBOBBCM_Assignee': Ticket.assignee,
                        'CBOBBCM_Created': Ticket.created,
                        'CBOBBIPPD_Key': bbip_links,
                        'CBOBBIPPD_Summary':bbip_summary,
                        'CBOBBIPPD_status':bbip_status,
                        'CBOBBIPPD_Assignee':bbip_assignee,
                        'CBOBBIPPD_Created':bbip_created,
                        'CBOBBOPPD_Key':bbop_links,
                        'CBOBBOPPD_Summary':bbop_summary,
                        'CBOBBOPPD_status': bbop_status,
                        'CBOBBOPPD_Assignee':bbop_assignee,
                        'CBOBBOPPD_Created':bbop_created

                    })
        Tickets.append(yourdict.copy())


    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="davidsexample.xls"'

    #
    if request.method == 'POST':
        response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Ticket_Summary_Report.xlsx'
        xlsx_data = WriteToExcel()
        response.write(xlsx_data)
        return response
    # if request.method == 'POST':
    #     response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename=All_Ticket_Summary_Report.xlsx'
    #     inclusive_data = inclusive_WriteToExcel()
    #     response.write(inclusive_data)
    #     return response


    # response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename=Ticket_Summary_Report.xlsx'
    # xlsx_data = WriteToExcel()
    # response.write(xlsx_data)
    # return response

#     data = WriteToExcel(Ticketdata)


    # for Ticket in obj:
    #     for a in Ticket.cm_linked_tickets:
    #         if (a.key.startswith('CBOBBIPPD')):
    #             bbip_links = a.key
    #             for link in bbip_links:
    #                 bbip_status = a.status
    #                 bbip_assignee = a.assignee
    #                 bbip_created = a.created
    #         if (a.key.startswith('CBOBBOPPD')):
    #             bbop_links = a.key
    #             for link in bbop_links:
    #                 bbop_status = a.status
    #                 bbop_assignee = a.assignee
    #                 bbop_created = a.created
    #
    #
    #             Tickets.append({
    #                     'CBOBBCM_Key': Ticket.key,
    #                     'CBOBBCM_Status': Ticket.status,
    #                     'CBOBBCM_Assignee': Ticket.assignee,
    #                     'CBOBBCM_Created': Ticket.created,
    #                     'CBOBBIPPD_Key': bbip_links,
    #                     'CBOBBIPPD_status': bbip_status,
    #                     'CBOBBIPPD_Assignee': bbip_assignee,
    #                     'CBOBBIPPD_Created': bbip_created,
    #                     'CBOBBOPPD_Key': bbop_links,
    #                     'CBOBBOPPD_status': bbop_status,
    #                     'CBOBBOPPD_Assignee': bbop_assignee,
    #                     'CBOBBOPPD_Created': bbop_created,
    #
    #                 })

    context = {

    'Tickets':Tickets,
    # 'settings.Myjira_url'
    # 'Ticketdata': Ticketdata

    }

    return render(request,"myJira/detail.html",context)
        #return render(request,"myJira/detail.html")
#  def export_file_to_xlsx(request):
#      response = HttpResponse(content_type='application/vnd.ms-excel')
#      response['Content-Disposition'] = 'attachment; filename=Jira_Summary.xlsx'
#      xlsx_data = WriteToExcel(Ticket_data)
#      response.write(xlsx_data)
#      return response
@login_required
def IP_PD_Tickets(request):
    parents = JiraTicket.objects.filter(key__icontains='cbobbcm')
    # obj = JiraTicket.objects.filter(key__istartswith="cbobbcm").prefetch_related(Prefetch('links', queryset= JiraTicket.objects.filter(Q(key__istartswith='cbobboppd')| Q(key__istartswith='cbobbippd')),to_attr = 'cm_linked_tickets'))
    data = []
    for issue in parents:
        children = issue.links.all()

         # filter = Q(links__key__icontains='cbobbippd')|Q(links__key__icontains='cbobboppd')
         # children = issue.links.filter(Q(links__key__icontains='cbobbip'))
        for child in children:
            if child.key.startswith('CBOBBIPPD'):
                grand_children = child.links.all()
                for grand_child in grand_children:
                    # if not grand_child.key.startswith('CBOBBCM'):
                    data.append({
                            'CBOBBCM_Key': issue.key,
                            'CBOBBCM_Summary': issue.Summary,
                            'CBOBBCM_Status': issue.status,
                            'CBOBBCM_Assignee': issue.assignee,
                            'CBOBBCM_Created': issue.created,
                            'CBOBBIPPD_Key': child.key,
                            'Child_Summary': child.Summary,
                            'Child_Status': child.status,
                            'Child_Assignee': child.assignee,
                            'Child_Created': child.created,
                            'Grand_Child_Key': grand_child.key,
                            'Grand_Child_Summary': grand_child.Summary,
                            'Grand_Child_Status': grand_child.status,
                            'Grand_Child_Assignee': grand_child.assignee,
                            'Grand_Child_Created': grand_child.created,
            })



    if request.method == 'POST':
        response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=IP_Linked_Tickets_Summary_Report.xlsx'
        ip_xlsx_data = ip_linked_WriteToExcel()
        response.write(ip_xlsx_data)
        return response

    new_d = []
    for x in data:
        if x not in new_d:
            new_d.append(x)

    context = {

        # 'data':data,

        'new_d':new_d,
        # 'Ticketdata': Ticketdata

        }


    return render(request,"myJira/IP_links.html",context)


@login_required
def OP_PD_Tickets(request):
        parents = JiraTicket.objects.filter(key__icontains='cbobbcm')
        # obj = JiraTicket.objects.filter(key__istartswith="cbobbcm").prefetch_related(Prefetch('links', queryset= JiraTicket.objects.filter(Q(key__istartswith='cbobboppd')| Q(key__istartswith='cbobbippd')),to_attr = 'cm_linked_tickets'))
        data = []
        for issue in parents:
             # filter = Q(links__key__icontains='cbobbippd')|Q(links__key__icontains='cbobboppd')
             children = issue.links.filter(Q(links__key__icontains='cbobbippd')|Q(links__key__icontains='cbobboppd'))
             for child in children:
                 if child.key.startswith('CBOBBOPPD'):
                     grand_children = child.links.all()
                     for grand_child in grand_children:
                         data.append({
                                'CBOBBCM_Key': issue.key,
                                'CBOBBCM_Summary': issue.Summary,
                                'CBOBBCM_Status': issue.status,
                                'CBOBBCM_Assignee': issue.assignee,
                                'CBOBBCM_Created': issue.created,
                                'CBOBBOPPD_Key': child.key,
                                'Child_Summary': child.Summary,
                                'Child_Status': child.status,
                                'Child_Assignee': child.assignee,
                                'Child_Created': child.created,
                                'Grand_Child_Key': grand_child.key,
                                'Grand_Child_Summary': grand_child.Summary,
                                'Grand_Child_Status': grand_child.status,
                                'Grand_Child_Assignee': grand_child.assignee,
                                'Grand_Child_Created': grand_child.created,
                })

        new_d = []
        for x in data:
            if x not in new_d:
                new_d.append(x)

        if request.method == 'POST':
            response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=OP_Linked_Tickets_Summary_Report.xlsx'
            op_xlsx_data = op_linked_WriteToExcel()
            response.write(op_xlsx_data)
            return response



        context = {

            'new_d':new_d,
            # 'Ticketdata': Ticketdata

            }


        return render(request,"myJira/OP_links.html",context)

def login(request):
    return render(request, 'registration/signup.html')

def signup(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CM-Tickets')
        else:
            form = UserCreationForm()
        return render(request, 'registration/signup.html', {
        'form': form
    })


def home(request):
    return render(request, 'home.html')
