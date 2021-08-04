import pandas as pd

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def generate_certificate(certificate_name, profissao):
    #nome final do arquivo com certificado
    file_certificate_name = 'certificado_'+certificate_name.replace(' ', '_')+'.png'
    #Cria objeto com o arquivo modelo para o certificado
    certificate_image = Image.open('certificado2.png')
    #desenha no objeto
    certificate_image_draw = ImageDraw.Draw(certificate_image)
    #seleciona a fonte
    certificate_font1 = ImageFont.truetype('times-new-roman-14.ttf', 50, encoding='unic')
    certificate_font2 = ImageFont.truetype('times-new-roman-14.ttf', 28, encoding='unic')
    #desenha o nome no certificado
    certificate_image_draw.text((350,310), certificate_name, font=certificate_font1, fill=(0, 0, 0))
    certificate_image_draw.text((480,391), profissao, font=certificate_font2, fill=(0, 0, 0))
    #salva o certificado editado
    certificate_image.save(file_certificate_name, 'PNG', resolution=100)

    return file_certificate_name

def sendMail(email_from, email_to, email_subject, email_body, file_certificate_name):

    msg = MIMEMultipart()
    
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject
    msg.add_header('Content-Type', 'text/html')
    msg.attach(MIMEText(email_body, 'plain'))

    attach_file= open(file_certificate_name, 'rb')
    attach_type = MIMEBase('image', 'png')
    attach_type.set_payload(attach_file.read())
    attach_type.add_header('Content-Disposition', 'attachment', filename=file_certificate_name)
    encoders.encode_base64(attach_type)

    msg.attach(attach_type)
    email_text = msg.as_string()

    smtpMail.sendmail(email_from, email_to, email_text)


dados = pd.read_csv('PlanilhaTesteDeAutomação.csv')
n = len(list(dados))

inputs = pd.read_csv('input.csv')
input_email = inputs.iloc[0,1]
input_password = inputs.iloc[1,1]

smtpMail = smtplib.SMTP('smtp.gmail.com: 587')
smtpMail.starttls()
smtpMail.login(input_email, input_password)
text_subject = 'E-mail automático gerado em pythom por um script para automação'
text_body = '''
            The passage experienced a surge in popularity during the 1960s when Letraset used it on their 
            dry-transfer sheets, and again during the 90s as desktop publishers bundled the text with 
            their software. Today it's seen all around the web; on templates, websites, and stock designs. 
            Use our generator to get your own, or read on for the authoritative history of lorem ipsum.
            '''

for i in range(n):
    name = dados.iloc[i, 1]
    email = dados.iloc[i, 2]
    prfissao = dados.iloc[i, 5]
    print(f'gerando certificado de {name}')
    certificado = generate_certificate(name, prfissao)
    print(f'gerado o certificado {certificado}')
    print(f'enviando certificado para {email}')
    sendMail('raulpessoa27@gmail.com', email, text_subject, text_body, certificado)
    print(f'email para {email} enviado')
