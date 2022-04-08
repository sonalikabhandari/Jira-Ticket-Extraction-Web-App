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

def ip_linked_WriteToExcel():
    output = BytesIO()


    parents = JiraTicket.objects.filter(key__icontains='cbobbcm')

    data = []
    for issue in parents:
        children = issue.links.filter(Q(links__key__icontains='cbobbip')|Q(links__key__icontains='cbobbop'))
        if children.exists():
            for child in children:
                grand_children = child.links.all()
                if grand_children.exists():
                    for grand_child in grand_children:
                        if not grand_child.key.startswith('CBOBBCM'):
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

                else:
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
                        'Grand_Child_Key': "",
                        'Grand_Child_Summary': "",
                        'Grand_Child_Status': "",
                        'Grand_Child_Assignee': "",
                        'Grand_Child_Created': "",
        })



        else:
            data.append({
                        'CBOBBCM_Key': issue.key,
                        'CBOBBCM_Summary': issue.Summary,
                        'CBOBBCM_Status': issue.status,
                        'CBOBBCM_Assignee': issue.assignee,
                        'CBOBBCM_Created': issue.created,
                        'CBOBBIPPD_Key': "",
                        'Child_Summary': "",
                        'Child_Status': "",
                        'Child_Assignee':"",
                        'Child_Created': "",
                        'Grand_Child_Key': "",
                        'Grand_Child_Summary': "",
                        'Grand_Child_Status': "",
                        'Grand_Child_Assignee':"",
                        'Grand_Child_Created': "",
        })



    new_d = []
    for x in data:
        if x not in new_d:
            new_d.append(x)

    def datetime_handler(x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        raise TypeError("Unknown type")

    with open('result-test.json', 'w') as f:
        json.dump(new_d,f, indent=4, default=datetime_handler)

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
            Child_Summary = parsed[element]['Child_Summary']
            Child_Status = parsed[element]['Child_Status']
            Child_Assignee = parsed[element]['Child_Assignee']
            Child_Created = parsed[element]['Child_Created']
            Grand_Child_Key = parsed[element]['Grand_Child_Key']
            Grand_Child_Summary = parsed[element]['Grand_Child_Summary']
            Grand_Child_Status = parsed[element]['Grand_Child_Status']
            Grand_Child_Assignee = parsed[element]['Grand_Child_Assignee']
            Grand_Child_Created = parsed[element]['Grand_Child_Created']

            df_data = [CBOBBCM_Key,CBOBBCM_Summary,CBOBBCM_Status,CBOBBCM_Assignee,CBOBBCM_Created,CBOBBIPPD_Key,Child_Summary,Child_Status,Child_Assignee,Child_Created,Grand_Child_Key,Grand_Child_Summary,Grand_Child_Status,Grand_Child_Assignee, Grand_Child_Created]# change elements to needs
            df = df.append([df_data])
            element = element + 1

        except KeyError as e:
            print ("I got a key error! " + str(e) + str(element))
        except NameError as e:
            print ("I got a Name Error! " + str(e) + str(element))


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



    worksheet.write(0,0,"CBOBBCM_Key")
    worksheet.write(0,1,"CBOBBCM_Summary")
    worksheet.write(0,2,"CBOBBCM_Status")
    worksheet.write(0,3,"CBOBBCM_Assignee")
    worksheet.write(0,4,"CBOBBCM_Created")
    worksheet.write(0,5,"CBOBBIPPD_Key")
    worksheet.write(0,6,"Child_Summary")
    worksheet.write(0,7,"Child_Status")
    worksheet.write(0,8,"Child_Assignee")
    worksheet.write(0,9,"Child_Created")
    worksheet.write(0,10,"Grand_Child_Key")
    worksheet.write(0,11,"Grand_Child_Summary")
    worksheet.write(0,12,"Grand_Child_Status")
    worksheet.write(0,13,"Grand_Child_Assignee")
    worksheet.write(0,14,"Grand_Child_Created")



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
    ip_xlsx_data = output.getvalue()
    # ip_xlsx_data contains the Excel file
    return ip_xlsx_data
