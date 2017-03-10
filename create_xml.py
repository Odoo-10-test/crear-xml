import os
import csv
import xmlrpclib
import re


HOST='localhost'
PORT=8089
DB='chile'
USER='admin'
PASS='12345'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)


def html_escape(text):
    """Produce entities within text.""" 
    html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }
    return "".join(html_escape_table.get(c,c) for c in text)
     
def _generate_partner_activities(estado):
    if estado is True:
        cont = 1
        path_file = '/home/odoo/Chile/ssi_activities.csv'
        view = open('./economical_activities_data.xml','w')
        view.write('<?xml version="1.0" encoding="utf-8"?>\n')   
        view.write('<odoo>\n  <data noupdate="1">\n') 
        archive = csv.DictReader(open(path_file))
        
        for field in archive:
            print 'Numero: ',cont
            name = html_escape(field["Name"].replace('"', '').replace("'", '').strip())
            code = html_escape(field["Code"].replace('"', '').replace("'", '').strip())
            tax_category = html_escape(field["TAX Category"].replace('"', '').replace("'", '').strip())
            vat_affected = html_escape(field["VAT Affected"].replace('"', '').replace("'", '').strip())
            internet_available = html_escape(field["Available at Internet"].replace('"', '').replace("'", '').strip())
            active = True
           
            view.write("    <record id='SII-EA%s' model='economical.activities' >\n"%str(cont))
            view.write("      <field name='name'>%s</field>\n"%str(name))
            view.write("      <field name='code'>%s</field>\n"%str(code)) 
            view.write("      <field name='tax_category'>%s</field>\n"%str(tax_category))
            view.write("      <field name='vat_affected'>%s</field>\n"%str(vat_affected))
            view.write("      <field name='internet_available'>%s</field>\n"%internet_available)
            view.write("      <field name='active'>%s</field>\n"%active) 
            view.write("    </record>\n")
            cont = cont + 1
        view.write('  </data>\n</odoo>\n')
        
def _generate_sii_document_class(estado):
    if estado is True:
        cont = 1
        path_file = '/home/odoo/Chile/sii_document_class.csv'
        view = open('./document_class_data.xml','w')
        view.write('<?xml version="1.0" encoding="utf-8"?>\n')   
        view.write('<odoo>\n  <data noupdate="1">\n') 
        archive = csv.DictReader(open(path_file))
        
        for field in archive:
            print 'Numero: ',cont
            name = html_escape(field["Name"].replace('"', '').replace("'", '').strip())
            sii_code = html_escape(field["SII Code"].replace('"', '').replace("'", '').strip())
            doc_code_prefix = html_escape(field["Document Code Prefix"].replace('"', '').replace("'", '').strip())
            code_template = html_escape(field["Code Template for Journal"].replace('"', '').replace("'", '').strip())
            report_name = html_escape(field["Name on Reports"].replace('"', '').replace("'", '').strip())
            document_type = html_escape(field["Document Type"].replace('"', '').replace("'", '').strip())
            dte = html_escape(field["DTE"].replace('"', '').replace("'", '').strip())
            active = html_escape(field["Active"].replace('"', '').replace("'", '').strip())
           
            view.write("    <record id='SII-DC%s' model='sii.document.class' >\n"%str(cont))
            view.write("      <field name='name'>%s</field>\n"%str(name))
            view.write("      <field name='sii_code'>%s</field>\n"%str(sii_code)) 
            view.write("      <field name='doc_code_prefix'>%s</field>\n"%str(doc_code_prefix))
            view.write("      <field name='code_template'>%s</field>\n"%str(code_template))
            view.write("      <field name='report_name'>%s</field>\n"%report_name)
            view.write("      <field name='dte'>%s</field>\n"%dte) 
            view.write("      <field name='active'>%s</field>\n"%active) 
            view.write("    </record>\n")
            cont = cont + 1
        view.write('  </data>\n</odoo>\n')
        
def _generate_sii_regional_offices(estado):
    if estado is True:
        cont = 1
        path_file = '/home/odoo/Chile/offices.csv'
        view = open('./regional_offices_data.xml','w')
        view.write('<?xml version="1.0" encoding="utf-8"?>\n')   
        view.write('<odoo>\n  <data noupdate="1">\n') 
        archive = csv.DictReader(open(path_file))
        
        for field in archive:
            print 'Numero: ',cont
            name = html_escape(field["name"].replace('"', '').replace("'", '').strip())
            code = html_escape(field["codes"].replace('"', '').replace("'", '').strip())
            
            ele_code = code.split('-')
            lis_code = len(code.split('-'))
            
            lis = []
            for i in range(lis_code-1):
                val = ele_code[i]
                county = 'ref('"'%s'"')'%(val)
                lis.append(county)
            counties = ', '.join(lis)
            view.write('    <record id="SII-RO%s" model="sii.regional.offices">\n'%str(cont))
            view.write('      <field name="name">%s</field>\n'%str(name))
            view.write('      <field name="county_ids" eval="[(6, 0, [%s])]" />\n'%str(counties)) 
            view.write('    </record>\n')
            cont = cont + 1
        view.write('  </data>\n</odoo>\n')

def __main__():
    print 'Ha comenzado la creacion del archivo'
    _generate_partner_activities(False)
    _generate_sii_document_class(False)
    _generate_sii_regional_offices(True)
    print 'Ha finalizado la creacion del archivo'
__main__()
