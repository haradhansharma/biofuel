
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4    
from reportlab.lib.colors import black, blue, red, whitesmoke, green, beige, gray, magenta, white, darkgreen
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from doc.doc_processor import site_info
from . models import *
from . helper import nreport_context


class ReportPDFData:
    def __init__(self, request, slug):   
        self.request = request
        self.slug = slug   
        self.pagesize = A4
        self.PH = self.pagesize[1]
        self.PW = self.pagesize[0]
        self.M = 0.5 * inch      
        self.styles = getSampleStyleSheet()
        
        self.title = 'Green Fuel Validation Platform'
        self.t_additional = 'Self Analysis Report'
        self.author = self.evaluator().orgonization
        self.creator = self.evaluator().email
        self.producer = site_info().get('domain')
        self.stylesN = self.styles['Normal']
        self.stylesH1 = self.styles['Heading1']
        self.stylesH2 = self.styles['Heading2']
        self.stylesH3 = self.styles['Heading3'] 
        self.stylesH4 = self.styles['Heading4']    
           
        self.stylesH5 = self.styles['Heading5']    
        
        self.stylesH6 = self.styles['Heading6']    
           
        self.stylesT = self.styles['Title']
        self.stylesB = self.styles['BodyText']   
        self.stylesB.alignment = TA_JUSTIFY
        
        self.styles.add(ParagraphStyle(name='TitleR', parent=self.stylesT, textColor=red), alias='titleR') 
        self.styles.add(ParagraphStyle(name='SectionT', parent=self.stylesH2, textColor=red, underlineWidth = self.PW), alias='sectionT')  
        self.styles.add(ParagraphStyle(name='LeftIndent', parent=self.stylesN, leftIndent=self.M/2, textColor = green ), alias='leftindent')  
        self.styles.add(ParagraphStyle(name='Footer', parent=self.stylesN, alignment=TA_CENTER, textColor = green ), alias='footer')  
        
              
        self.stylesTR = self.styles['TitleR']
        self.SectionT = self.styles['SectionT']
        self.SectionT.spaceAfter = 0
        self.LeftIndent = self.styles['LeftIndent']
        self.Footer = self.styles['Footer']
        
        
        self.title_font_size = 16     
        
        
    def evaluator(self):
        evaluator = Evaluator.objects.get(slug = self.slug)
        return evaluator
        
    
    def report_initial(self, c, doc):        
        c.drawInlineImage('https://shippinglab.dk/wp-content/uploads/2019/07/tugboat-on-big-sea-slider.jpg' ,0,0,width=self.PW,height=self.PH)   
        
 
    def top_string(self, c, doc):
        c.setFont('Times-Roman',9)
        c.drawString(inch/2, self.PH - self.M/2, f'{self.title}--{self.t_additional}')
        
   
    def uline(self):
        drawing = Drawing(self.PW,2)
        line = Line(0,0,self.PW,0)
        line.strokeColor = red
        line.strokeWidth = 2
        drawing.add(line)
        
        return drawing   
    def uline34(self):
        drawing = Drawing(self.PW/3,2)
        line = Line(0,0,self.PW/3,0)
        line.strokeColor = red
        line.strokeWidth = 2
        drawing.add(line)
        
        return drawing 
    def uline100(self):
        drawing = Drawing(self.PW-self.M*2.5,2)
        line = Line(0,0,self.PW-self.M*2.5,0)
        line.strokeColor = red
        line.strokeWidth = 1
        drawing.add(line)
        
        return drawing 
    
    def ulineDG100(self):
        drawing = Drawing(self.PW-self.M*2.5,2)
        line = Line(0,0,self.PW-self.M*2.5,0)
        line.strokeColor = darkgreen
        line.strokeWidth = 1
        drawing.add(line)
        
        return drawing 
    def ulineG100(self):
        drawing = Drawing(self.PW-self.M*2.5,2)
        line = Line(0,0,self.PW-self.M*2.5,0)
        line.strokeColor = green
        line.strokeWidth = 1
        drawing.add(line)
        
        return drawing 
       
    def first_page(self, c, doc):
        c.saveState() 
        self.report_initial(c, doc)      
        self.top_string(c, doc)   
        c.setFillColorRGB(255, 0, 0)     
        c.setFont('Times-Bold', self.title_font_size)
        c.drawCentredString(self.PW/2.0, self.PH-self.M*2, f'EVALUATION REPORT OF {self.evaluator().biofuel.name.upper()}')
        c.setFont('Times-Roman',9)
        c.setFillColorRGB(255, 255, 255)  
        c.drawString(self.M, self.M, "Cover Page / %s / %d" % (self.t_additional, self.evaluator().id))
        c.restoreState()
        
    def later_page(self, c, doc):
        c.saveState()
        self.top_string(c, doc)
        c.setFont('Times-Roman',9)
        c.drawString(self.M, self.M/3, "Page / %d %s / %d" % (doc.page, self.t_additional, self.evaluator().id))
        c.restoreState()
    
    def wrapped_pdf(self):
        Story = [Spacer(self.PW/2.0,self.PH/2.5)]
        report_number = [
            Paragraph('-----------------------------------------------', self.stylesTR),
            Paragraph(f'Report #{self.evaluator().id}', self.stylesTR),
            Paragraph('-----------------------------------------------', self.stylesTR)            
         ]
        Story.extend(report_number)
        Story.append(Spacer(1,self.PH/4))
        Story.extend(self.basic_summary())            
        Story.append(PageBreak())
        Story.extend(self.desclimar_and_content())
        Story.append(PageBreak())        
        Story.extend(self.grape_status())
        Story.extend(self.summary_statement())
        Story.extend(self.question_specific_feedback())
        Story.extend(self.details_of_activities())
        Story.extend(self.biofuel_history())
        
        return Story
    
    def basic_summary(self):
        style = TableStyle([
        ('GRID', (0,0), (3,3), 0.15, red),
        ('BACKGROUND', (0,0), (3,0), red),
        ('TEXTCOLOR', (0,0), (-1,0), whitesmoke), # The negative one means "go to the last element"        
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),        
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 12),        
        ('BOTTOMPADDING', (0,0), (-1,0), 12), # 12 = 12 pixels        
        ('BACKGROUND', (0,1), (-1,-1), beige), # Background for the rest of the table (excluding the title row)        
        ('SPAN', (2,1), (2,2)),
        ('ALIGN', (2,1), (2,2), 'CENTER'),
        ('VALIGN', (2,1), (2,2), 'MIDDLE'),        
        ])
        
        data = [
        ['Name And Organization', 'Email And Phone', 'Selected Biofuel'],
        [f'{self.evaluator().name}', f'{self.evaluator().email}', f'{self.evaluator().biofuel.name}'],
        [f'{self.evaluator().orgonization}', f'{self.evaluator().phone}', ''],        
        ]
        
        table = Table(data, colWidths = (self.PW-self.M*2)/3, cornerRadii=[5, 5, 5, 5])
        table.setStyle(style)
            
        flowables = [
            Paragraph('<a name="basic"/><font color = beige>BASIC SUMMARY</font>', self.SectionT),
            self.uline(),
            Spacer(0.15*inch,0.15*inch),
            table,        
            
            ]
        
        return flowables     
    
    def desclimar_and_content(self):
        text = "<p> Use of any knowledge, information or data contained in this document n\
            shall be at the user's sole risk. The members of the ShippingLab n\
            Project accept no liability or responsibility, in negligence or otherwise, n\
            for any loss, damage or expense whatever sustained by any person as a result of n\
            the use, in any manner or form, of any knowledge, information or data contained in n\
            this document, or due to any inaccuracy, omission or error therein contained.</p>"
        text2 = "<p> Danish Maritime Fund shall not in any way be liable or responsible for the use of n\
            any such knowledge, information or data, or of the consequences thereof.</p> "
        data = [
            Spacer(self.M,self.M),
            Paragraph('CONTENT', self.SectionT), 
            self.uline(),           
            ListFlowable(
            [
            ListItem(Paragraph('<a href = #dis >Disclaimer</a>', self.stylesH3),bulletColor='green',value='square'),
            ListItem(Paragraph('<a href = #lsb >Latest Status Of Biofuel</a>', self.stylesH3),bulletColor='green',value='square'),            
            ListItem(Paragraph('<a href = #bs >Biofuel Summary</a>', self.stylesH3),bulletColor='green',value='square'),            
            ListItem(Paragraph('<a href = #qsf >Question Specific Feedack</a>', self.stylesH3),bulletColor='green',value='square'),
            ListItem(Paragraph('<a href = #doa >Details of Activities</a>', self.stylesH3),bulletColor='green',value='square'),
            ListItem(Paragraph('<a href = #bh >Biofuel History</a>', self.stylesH3),bulletColor='green',value='square'), 
            ListItem(Paragraph('<a href = #on >Ownership</a>', self.stylesH3),bulletColor='green',value='square'), 
            
            ],
            bulletType='bullet',
            start='square',           
            ),           
            
            PageBreak(),  
            Spacer(self.PH/2,self.PH/2),          
            Paragraph('<a name="dis"/>DISCLAIMER', self.SectionT),
            self.uline(),
            Paragraph(text, self.stylesB),
            Paragraph(text2, self.stylesB),            
            Spacer(0.15*inch,0.15*inch),
        ]
        
        return data
        
       
    def grape_status(self):
        context = nreport_context(self.request, self.slug)       
        drawing = Drawing(self.PW - self.M - self.M - self.M/2, 260)
        data = context['item_seris']
        bc = HorizontalBarChart()      
        bc.data = data
        bc.strokeColor = green        
        bc.categoryAxis.labels.dx = self.PW/1.5
        bc.categoryAxis.labels.dy = 20             
        bc.categoryAxis.categoryNames = context['item_label']       
        bc.categoryAxis.style = 'stacked'
        bc.x = 2       
        bc.height = 250
        bc.width = self.PW - self.M - self.M - self.M/2
        bc.data = data        
        bc.groupSpacing = 10
        bc.valueAxis.valueMin = 0
        bc.categoryAxis.labels.boxAnchor = 'e'       

        from reportlab.graphics.widgets.grids import ShadedRect
        bc.bars.symbol = ShadedRect()
        bc.bars.symbol.fillColorStart = green
        bc.bars.symbol.fillColorEnd = white
        bc.bars.symbol.orientation = 'horizontal'
        bc.bars.symbol.cylinderMode = 1
        bc.bars.symbol.strokeWidth = 0
        bc.bars.symbol.strokeColor = green        

        bc.bars[1].symbol = ShadedRect()
        bc.bars[1].symbol.fillColorStart = gray
        bc.bars[1].symbol.fillColorEnd = white
        bc.bars[1].symbol.orientation = 'horizontal'
        bc.bars[1].symbol.cylinderMode = 1
        bc.bars[1].symbol.strokeWidth = 0
        bc.bars[1].symbol.strokeColor = gray        

        bc.bars[2].symbol = ShadedRect()
        bc.bars[2].symbol.fillColorStart = red
        bc.bars[2].symbol.fillColorEnd = white
        bc.bars[2].symbol.orientation = 'horizontal'
        bc.bars[2].symbol.cylinderMode = 1
        bc.bars[2].symbol.strokeWidth = 0
        bc.bars[2].symbol.strokeColor = red

        drawing.add(bc)    
       
        flowables = [
            Paragraph('<a name="lsb"/>LATEST STATUS OF THE BIOFUEL', self.SectionT),
            self.uline(),
            Spacer(0.25*inch,0.25*inch),
            Paragraph('<b>:Traffic-light Overview:</b>', self.Footer),
            # self.ulineDG100(),   
            Spacer(0.05*inch,0.05*inch),                     
            drawing,
            Spacer(0.25*inch,0.25*inch),
            Paragraph('<b>:Remarkable Points:</b>', self.Footer),
            # self.ulineDG100(), 
            Spacer(0.05*inch,0.05*inch),            
            self.points_status(),
            Spacer(0.25*inch,0.25*inch),
            Paragraph('<b>:Todos:</b>', self.Footer),
            self.ulineDG100(),  
            Paragraph('<b>The following is the prioritised list of validation activities that should be undertaken based on your self assessment responses:</b>', self.stylesB),
            Spacer(0.10*inch,0.10*inch),            
                       
            ]       
        todos = self.todos()
        flowables.extend(todos)                        
        flowables.append(Spacer(0.05*inch,0.05*inch))
        flowables.append(Paragraph('<font color = "darkgreen"><b>Please see the <a href = #doa>"Deatils of activities"</a> section for more details.</b></font>', self.stylesB))        
        return flowables
    
    def points_status(self):
        style = TableStyle([
        ('GRID', (0,0), (1,1), 0.25, red), 
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12), # 12 = 12 pixels
        ('BACKGROUND', (0,1), (-1,-1), beige), # Background for the rest of the table (excluding the title row)
        ])
        
        
        negative_point_block =[
            Paragraph('Negative Points', self.stylesN),
            self.uline34(),            
            ListFlowable(
            [
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),           
            ],
            bulletType='bullet',
            start='square',           
            )
        ] 
        
        positive_point_block =[
            Paragraph('Positive Points', self.stylesN),
            self.uline34(),            
            ListFlowable(
            [
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),
            ListItem(Paragraph('sublist item 2', self.stylesN),bulletColor='red',value='square'),           
            ],
            bulletType='bullet',
            start='square',           
            )
        ] 
        
        data = [        
        [negative_point_block, positive_point_block],  
        
        ]        
        table = Table(data, colWidths = (self.PW-self.M*2)/2 - self.M/2, cornerRadii=[5, 5, 5, 5])
        table.setStyle(style)    
        return table 
    
    
    def todos(self):       
        context = nreport_context(self.request, self.slug)   
        na_ac = context['na_ac']   
        data = []   
        inn = 0    
        for na in na_ac:
            inn += 1
            todo_title = f'{inn}. <li><b>{na.name_and_standared.upper()}</b>({na.is_active})</li>'
            quotations = ''
            for quotation in na.get_quotations():
                quotations += f'<font color = green><u><a href="{self.request.build_absolute_uri(quotation.get_absolute_url())}"><b>Quot#</b>{quotation.id}::{quotation.price}</a></u></font> , '    
            self.stylesH5.spaceAfter = 0         
            data.append(Paragraph(todo_title, self.stylesH5))
            data.append(self.uline100())
            self.stylesH6.leftIndent = 18
            data.append(Paragraph(quotations, self.stylesH6))            
            data.append(Spacer(0.05*inch,0.05*inch))           
        return data    
    
    def summary_statement(self):
        context = nreport_context(self.request, self.slug)  
        eva_label = context['eva_label']  
        
        data = [
            PageBreak(),
            Paragraph(f'<a name="bs"/><font>BIOFUEL SUMMARY</font>', self.SectionT),
            self.uline(),
            Spacer(0.5*inch,0.5*inch)
        ] 
        
        for el in eva_label:         
            self.stylesH4.spaceAfter = 0   
            title = Paragraph(f'<a name="{el.id}l"/><font color="darkgreen">{el.label.label.upper()}</font>', self.stylesH4)
            data.append(title)
            data.append(self.ulineDG100())            
            for es in el.evalebelstatement_set.all():
                if es.statement is not None:
                    st = Paragraph(es.statement, self.stylesB)
                    data.append(st)                                    
                if es.next_step is not None:                    
                    ns = Paragraph(es.next_step, self.stylesB)
                    data.append(ns)
                    data.append(Spacer(0.15*inch,0.15*inch))         
        
        return data
    
    def question_specific_feedback(self):
        context = nreport_context(self.request, self.slug)  
        evaluation = context['evaluation']        
        data = [
            PageBreak(),
            Paragraph(f'<a name="qsf"/><font>QUESTION SPECIFIC FEEDBACK</font>', self.SectionT),
            self.uline(),
            Spacer(0.5*inch,0.5*inch)
        ] 
        
        style = TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, red), 
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE', (0,0), (4,4), 9),
        ('BOTTOMPADDING', (0,0), (4,4), 4), # 12 = 12 pixels
        ('BACKGROUND', (0,1), (-1,-1), beige), # Background for the rest of the table (excluding the title row)
        ])
        
        for e in evaluation:
            ques = Paragraph(f'<font color="green">Question : {e.question.name}</font>', self.stylesN)
            data.append(ques)
            data.append(self.ulineG100())
            data.append(Spacer(0.1*inch,0.1*inch))           
            data.append(Paragraph((f'<b>Chosen Option :</b>{str(e.option.name)}'), self.stylesN))
            data.append(Paragraph(f'<b>Suggested Quotations :</b>', self.stylesN))
            quotations = ''
            for quotation in e.question.get_quotations:
                quotations += f'<font color = green><u><a href="{self.request.build_absolute_uri(quotation.get_absolute_url())}">Quotation#{quotation.id}::{quotation.price}</a></u></font> , '    
            self.stylesH6.leftIndent = 18             
            for quotation in e.question.get_related_quotations:
                quotations += f'<font color = green><u><a href="{self.request.build_absolute_uri(quotation.get_absolute_url())}">Quotation#{quotation.id}::{quotation.price}</a></u></font> , '  
            if quotations: 
                self.stylesH6.spaceBefore = 0                        
                data.append(Paragraph(quotations, self.stylesH6))            
            comments = ''
            for qa in e.get_question_comment:
                comments += f'<p>{qa.comments}</p>'
            data.append(Paragraph(f'<b>Self Comment :</b>{comments}', self.stylesN))
            data.append(Paragraph(f'<b>GFVP Feedback :</b> {e.option.statement}', self.stylesB))
            if e.question.stanchart.all():
                data.append(Paragraph(f'<b>Typical std values : </b>'))
                
                
                table_data = [        
                    ['Oil Name', 'Unit', 'Value', 'Link'],           
                ] 
                
                for cd in e.question.stanchart.all():
                    table_data.append([cd.oil_name , cd.unit, cd.value, cd.link])     
                    
                table = Table(table_data, colWidths = (self.PW-self.M*2)/4 - self.M/2, cornerRadii=[5, 5, 5, 5])
                table.setStyle(style)              
                data.append(table) 
                data.append(Spacer(0.15*inch,0.15*inch))  
        
        return data
    
    def details_of_activities(self):
        context = nreport_context(self.request, self.slug)  
        next_activities = context['next_activities']        
        data = [
            PageBreak(),
            Paragraph(f'<a name="doa"/><font>DETAILS OF ACTIVITIES</font>', self.SectionT),
            self.uline(),
            Spacer(0.5*inch,0.5*inch)
        ] 
        
        for e in next_activities:           
            name = Paragraph(f'<font color="green">ACTIVITY : {e.name_and_standared.upper()}</font>', self.stylesN)
            data.append(name)
            data.append(self.ulineG100())
            data.append(Spacer(0.1*inch,0.1*inch))            
            data.append(Paragraph(f'<b>Related Questions :</b>'))
            rqs = []
            self.stylesB.spaceBefore = 1            
            for rq in e.related_questions.all():    
                self.stylesB.fontSize = 8
                self.stylesB.textColor = green                
                rqs.append(ListItem(Paragraph(f'{rq.name}', self.stylesB),bulletColor='green',value='circle', bulletFontSize = 8))    
                   
            q_data = ListFlowable(
                rqs,
                bulletType='bullet',
                start='square',           
                )
            data.append(q_data)
            self.stylesB.fontSize = 10      
            self.stylesB.textColor = black                  
            data.append(Paragraph(f'<b>Descriptions :</b> {e.descriptions}', self.stylesB))
            data.append(Paragraph(f'<b>Completed :</b> {e.is_active}', self.stylesN))
            data.append(Spacer(0.15*inch,0.15*inch))      
            
        
        return data
    
    def biofuel_history(self):
        context = nreport_context(self.request, self.slug)  
        dfh = context['dfh']        
        history_data = [
            PageBreak(),
            Paragraph(f'<a name="bh"/><font>BIOFUEL HISTORY</font>', self.SectionT),
            self.uline(),
            Spacer(0.5*inch,0.5*inch)
        ] 
        
        for results in dfh:
            for data_date, data_list in results.items():
                h_date = data_date
                h_label = data_list[0]
                h_series = data_list[1] 
                
                data = h_series

                labels = h_label

                drawing = Drawing(self.PW-self.M*3, 170)

                bc = VerticalBarChart()
                bc.x = self.M
                # bc.y = 50
                bc.height = 150
                bc.width = self.PW-self.M*3
                bc.data = data

                bc.barSpacing = 2
                bc.groupSpacing = 10
                bc.barWidth = 10

                bc.valueAxis.valueMin = 0
                bc.valueAxis.valueMax = 100
                bc.valueAxis.valueStep = 20
                bc.valueAxis.labels.fontName = 'Helvetica'
                bc.valueAxis.labels.fontSize = 8

                bc.categoryAxis.categoryNames = labels
                bc.categoryAxis.labels.fontName = 'Helvetica'
                bc.categoryAxis.labels.fontSize = 8
                bc.valueAxis.labels.boxAnchor = 'n'
                bc.valueAxis.labels.textAnchor = 'middle'
                bc.categoryAxis.labels.dy = -10

                bc.barLabels.nudge = 10

                bc.barLabelFormat = '%0.2f'
                bc.barLabels.dx = 0
                bc.barLabels.dy = 0
                bc.barLabels.boxAnchor = 'n'  # irrelevant (becomes 'c')
                bc.barLabels.fontName = 'Helvetica'
                bc.barLabels.fontSize = 6
                
                
                bc.bars[0].fillColor = green
                bc.bars[0].strokeColor = green                
                bc.bars[1].fillColor = gray
                bc.bars[1].strokeColor = gray                
                bc.bars[2].fillColor = red
                bc.bars[2].strokeColor = red

                drawing.add(bc)
                
                history_title = Paragraph(f'<font color="green">On : {h_date}</font>', self.stylesN)
                history_data.append(history_title)
                history_data.append(self.ulineG100())   
                history_data.append(Spacer(0.20*inch,0.20*inch))                                            
                history_data.append(drawing)
                history_data.append(Spacer(0.20*inch,0.20*inch))           
        
        return history_data
        