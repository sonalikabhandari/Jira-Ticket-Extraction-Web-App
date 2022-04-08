from io import BytesIO
import xlsxwriter
import pandas as pd
import xlwt
from xlsxwriter.utility import xl_rowcol_to_cell
import datetime
from .models import JiraTicket
from django.db.models import Prefetch
from django.db.models import Q
import json
from django.utils.translation import ugettext

def WriteToExcel():
    output = BytesIO()


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


    def datetime_handler(x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        raise TypeError("Unknown type")

    with open('result-test.json', 'w') as f:
        json.dump(Tickets,f, indent=4, default=datetime_handler)

        # with open('result-test.json', 'r') as jsonfile:
        #     data = json.load(jsonfile)

        #
    with open('result-test.json', 'r') as myfile:
        data=myfile.read()

    parsed = json.loads(data)
    df = pd.DataFrame([])
    element = 0
    length = len(parsed)
    for element in range(0, length):
        try:
            CBOBBCM_Key = parsed[element]['CBOBBCM_Key']
            CBOBBCM_Summary = parsed[element]['CBOBBCM_Summary']
            CBOBBCM_Status = parsed[element]['CBOBBCM_Status']
            CBOBBCM_Assignee = parsed[element]['CBOBBCM_Assignee']
            CBOBBCM_Created = parsed[element]['CBOBBCM_Created']
            CBOBBIPPD_Key = parsed[element]['CBOBBIPPD_Key']
            CBOBBIPPD_Summary = parsed[element]['CBOBBIPPD_Summary']
            CBOBBIPPD_status = parsed[element]['CBOBBIPPD_status']
            CBOBBIPPD_Assignee = parsed[element]['CBOBBIPPD_Assignee']
            CBOBBIPPD_Created = parsed[element]['CBOBBIPPD_Created']
            CBOBBOPPD_Key = parsed[element]['CBOBBOPPD_Key']
            CBOBBOPPD_Summary = parsed[element]['CBOBBOPPD_Summary']
            CBOBBOPPD_status = parsed[element]['CBOBBOPPD_status']
            CBOBBOPPD_Assignee = parsed[element]['CBOBBOPPD_Assignee']
            CBOBBOPPD_Created = parsed[element]['CBOBBOPPD_Created']

            df_data = [CBOBBCM_Key,CBOBBCM_Summary,CBOBBCM_Status,CBOBBCM_Assignee,CBOBBCM_Created,CBOBBIPPD_Key,CBOBBIPPD_Summary,CBOBBIPPD_status,CBOBBIPPD_Assignee,CBOBBIPPD_Created,CBOBBOPPD_Key,CBOBBOPPD_Summary,CBOBBOPPD_status,CBOBBOPPD_Assignee, CBOBBOPPD_Created]# change elements to needs
            df = df.append([df_data])
            element = element + 1

        except KeyError as e:
            print ("I got a key error! " + str(e) + str(element))
        except NameError as e:
            print ("I got a Name Error! " + str(e) + str(element))


    # df[4]= [d.date() for d in df[4]]
    df[5]= df[5].apply(','.join)
    df[6]= df[6].apply(','.join)
    df[7]= df[7].apply(','.join)
    df[8]= df[8].apply(','.join)
    df[9]= df[9].apply(','.join)
    df[10]= df[10].apply(','.join)
    df[11]= df[11].apply(','.join)
    df[12]= df[12].apply(','.join)
    df[13]= df[13].apply(','.join)
    df[14]= df[14].apply(','.join)


    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Jira_Summary', startrow = 0)
    workbook = writer.book

    worksheet = writer.sheets['Jira_Summary']

    worksheet.set_zoom(80)

    number_format = workbook.add_format({'num_format': '#,##0', 'align': 'center',  'valign':'vcenter'})
    float_format =  workbook.add_format({'num_format': '0"%"', 'align': 'center',  'valign':'vcenter'})
    date_format = workbook.add_format({'num_format': 'mm/dd/yyyy', 'align': 'center',  'valign':'vcenter'})
    text_format = workbook.add_format({'align': 'center',  'valign':'vcenter'})
    #text_format = workbook.add_format({'align': 'center',  'valign':'vcenter', 'text_wrap':True})
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'align':'center',
        'valign': 'vcenter',
        'fg_color': '#BFBFBF',
        'border': 1})

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value , header_format)






    # for row in range(0,0):
    #     worksheet.write(0, col_num, value , header_format)

    worksheet.write(0,0,"CBOBBCM_Key")
    worksheet.write(0,1,"CBOBBCM_Summary")
    worksheet.write(0,2,"CBOBBCM_Status")
    worksheet.write(0,3,"CBOBBCM_Assignee")
    worksheet.write(0,4,"CBOBBCM_Created")
    worksheet.write(0,5,"CBOBBIPPD_Key")
    worksheet.write(0,6,"CBOBBIPPD_Summary")
    worksheet.write(0,7,"CBOBBIPPD_status")
    worksheet.write(0,8,"CBOBBIPPD_Assignee")
    worksheet.write(0,9,"CBOBBIPPD_Created")
    worksheet.write(0,10,"CBOBBOPPD_Key")
    worksheet.write(0,11,"CBOBBOPPD_Summary")
    worksheet.write(0,12,"CBOBBOPPD_status")
    worksheet.write(0,13,"CBOBBOPPD_Assignee")
    worksheet.write(0,14,"CBOBBOPPD_Created")

    # for index, row in df.iterrows():
    #     worksheet.write(row["0"], 'https://jiratest.corp.chartercom.com/browse/'+row["CBOBBCM_Key"] , string = row["CBOBBCM_Key"])


    worksheet.set_column('A:A', 30 ,text_format)
    worksheet.set_column('B:B', 50 ,text_format)
    worksheet.set_column('C:C', 30 ,text_format)
    worksheet.set_column('D:D', 30  ,text_format)
    worksheet.set_column('E:E', 30,date_format)
    worksheet.set_column('F:F', 30  ,text_format)
    worksheet.set_column('G:G', 50  ,text_format)
    worksheet.set_column('H:H', 30 ,text_format)
    worksheet.set_column('I:I', 30,text_format)
    worksheet.set_column('J:J', 30 ,date_format)
    worksheet.set_column('K:K', 30 ,text_format)
    worksheet.set_column('L:L', 50 ,text_format)
    worksheet.set_column('M:M', 30 ,text_format)
    worksheet.set_column('N:N', 30 ,text_format)
    worksheet.set_column('O:O', 30 ,date_format)

    worksheet.set_row(0,60, header_format)
    worksheet.autofilter('A1:O1')

    # Here we will adding the code to add data
    writer.save()
    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data
