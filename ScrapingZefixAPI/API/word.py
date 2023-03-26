from .models import firms
from django.utils import timezone
from docxtpl import DocxTemplate
from docx import Document
from ScrapingZefixAPI.settings import APP_DICT, BASE_DIR
import os
import PyPDF2
import shutil
from os import listdir
from os.path import isfile, join

class fileManager():
    def __init__(self):
        self.raw_date = timezone.now() - timezone.timedelta(1)
        self.date = str(self.raw_date).split()[0]
        self.TEMPLATE_PATH = join(BASE_DIR,'Static/Word/template.docx')
        self.stamp = 'tmp_%i'%(int(timezone.now().timestamp()))

        self.all_dir_path = join(BASE_DIR, 'Static', self.date)
        self.pdf_dir_path = join(BASE_DIR, 'Static/PDF', self.stamp)
        self.word_dir_path = join(BASE_DIR, 'Static/Word', self.stamp)

        os.mkdir(self.pdf_dir_path)
        os.mkdir(self.word_dir_path)
        os.mkdir(self.all_dir_path)


    def get_zip_daily(self):
        firms_of_the_day = firms.objects.filter(date__exact=self.date).all()
        for firm in firms_of_the_day:
            self.create_word(firm)

        self.create_pdf()
        pdf_path = self.concat_pdf()
        
        zip_path = shutil.make_archive('%s'%self.date, 'zip', base_dir=self.word_dir_path, root_dir=BASE_DIR)
        os.system('mv %s.zip %s'%(self.date, self.all_dir_path))
        



    def create_word(self, firm:firms):
        doc = DocxTemplate(self.TEMPLATE_PATH)
        dict = {
            "firm": firm.name,
            "lastname":(firm.admin).lastname,
            "surname":(firm.admin).surname,
            "zip":firm.zip,
            "city":firm.city,
            "street":firm.street,
            "gender":APP_DICT["FR"]["gender"][(firm.admin).gender],
            "date": '%s %s %s'%(self.raw_date.day, APP_DICT['MONTHS'][self.raw_date.month-1], self.raw_date.year)
        }
        doc.render(dict)
        doc.save(join(self.word_dir_path, firm.name + '.docx')) 
        

    def create_pdf(self):
        os.system('soffice --convert-to pdf --infilter=",,CMU Serif," %s/*.docx --outdir %s'%(self.word_dir_path, self.pdf_dir_path))

    def concat_pdf(self) -> str:
        pdfWriter = PyPDF2.PdfFileWriter()
        
        onlypdffiles = [join(self.pdf_dir_path, f) for f in listdir(self.pdf_dir_path) if isfile(join(self.pdf_dir_path,f)) and f.find('.pdf')> -1]
        for file in onlypdffiles:
            pdfFileObj = open(file,'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
        
        pdfOutput = open(join(self.all_dir_path, '%s.pdf'%self.date), 'wb')
        pdfWriter.write(pdfOutput)
        pdfOutput.close()
        return join(self.all_dir_path, '%s.pdf'%self.date)
        
    def words_path(self) -> str:
        return self.word_dir_path

    def pdfs_path(self) -> str:
        return self.pdf_dir_path
        