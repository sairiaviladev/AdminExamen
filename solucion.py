import mysql.connector
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(output_file, tot_cruces_recibidos, importe_total, cruces_por_hora, cruces_tipo_TAG, cruces_cat_cobrada):
    pdf = canvas.Canvas(output_file, pagesize=letter)
    
    #Se pinta el título del documento
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Reporte de Cruces")

    #Respuestas a las preguntas
    pdf.setFont("Helvetica", 12)
    y = 700
    pdf.drawString(100, y, f"1. ¿Cuántos cruces he recibido en el archivo?: {tot_cruces_recibidos}")
    y -= 20
    pdf.drawString(100, y, f"2. ¿Cuál es el importe total de los cruces recibidos?: {importe_total}")
    y -= 20
    pdf.drawString(100, y, "3. ¿Cuántos cruces he recibido en cada hora del día?:")
    y -= 20
    for hora, cant in cruces_por_hora.items():
        pdf.drawString(120, y, f"{hora}: {cant}")
        y -= 15
    y -= 5
    pdf.drawString(100, y, "4. ¿Cuántos cruces he recibido por cada tipo de TAG?:")
    y -= 20
    for tipo_TAG, cant in cruces_tipo_TAG.items():
        pdf.drawString(120, y, f"{tipo_TAG}: {cant}")
        y -= 15
    y -= 5
    pdf.drawString(100, y, "5. ¿Cuántos cruces he recibido por cada categoría cobrada?:")
    y -= 20
    for categoria, cant in cruces_cat_cobrada.items():
        pdf.drawString(120, y, f"{categoria}: {cant}")
        y -= 15

    pdf.save()

tot_cruces_recibidos = 0
importe_total = 0
cruces_por_hora = {}
cruces_tipo_TAG = {}
cruces_cat_cobrada = {}

try:
    tree = ET.parse('documentation\V00067505042023235814.xml')
    root = tree.getroot()

    with mysql.connector.connect(host="localhost", user="root", password="", database="Registros_Peaje") as conn:
        cur = conn.cursor()

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS Registros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_TAG VARCHAR(100),
            concesion INT,
            tipo_TAG INT,
            IUT VARCHAR(100),
            categoria INT,
            categoria_cobrada INT,
            categoria_detectada INT,
            status INT,
            hora_peaje TIME,
            fecha_peaje DATE,
            importe_peaje INT,
            numero_reenvio INT,
            entrada INT,
            salida INT,
            sentido INT
            )
            '''
        )

        for dato in root.findall('Registro'):
            numero_TAG = dato.find('Numero_TAG').text
            concesion = int(dato.find('Concesion').text)
            tipo_TAG = int(dato.find('Tipo_TAG').text)
            IUT = dato.find('IUT').text
            categoria = int(dato.find('Categoria').text)
            categoria_cobrada = int(dato.find('Categoria_Cobrada').text)
            categoria_detectada = int(dato.find('Categoria_Detectada').text)
            status = int(dato.find('Status').text)
            hora_peaje = dato.find('Hora_peaje').text
            fecha_peaje = dato.find('Fecha_peaje').text
            importe_peaje = int(dato.find('Importe_peaje').text)
            numero_reenvio = int(dato.find('Numero_Reenvio').text)
            entrada = int(dato.find('Entrada').text)
            salida = int(dato.find('Salida').text)
            sentido = int(dato.find('Sentido').text)

            cur.execute(
                '''   
                INSERT INTO Registros(
                    numero_TAG, concesion, tipo_TAG, IUT, categoria, categoria_cobrada, categoria_detectada,
                    status, hora_peaje, fecha_peaje, importe_peaje, numero_reenvio, entrada, salida, sentido
                ) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s )''', 
                (numero_TAG, concesion, tipo_TAG, IUT, categoria, categoria_cobrada, categoria_detectada,
                status, hora_peaje, fecha_peaje, importe_peaje, numero_reenvio, entrada, salida, sentido)         
            )   

            tot_cruces_recibidos += 1
            importe_total += importe_peaje

            if hora_peaje in cruces_por_hora:
                cruces_por_hora[hora_peaje] += 1
            else:
                cruces_por_hora[hora_peaje] = 1

            if tipo_TAG in cruces_tipo_TAG:
                cruces_tipo_TAG[tipo_TAG] += 1
            else:
                cruces_tipo_TAG[tipo_TAG] = 1

            if categoria_cobrada in cruces_cat_cobrada:
                cruces_cat_cobrada[categoria_cobrada] += 1
            else:
                cruces_cat_cobrada[categoria_cobrada] = 1

            conn.commit()

except Exception as e:
    print("Error:", e)

#Respuesta a las preguntas en terminal
print("1. ¿Cuántos cruces he recibido en el archivo?", tot_cruces_recibidos)
print("2. ¿Cuál es el importe total de los cruces recibidos?", importe_total)

print("3. ¿Cuántos cruces he recibido en cada hora del día?")
for hora, cant in cruces_por_hora.items():
    print(f" {hora}: {cant}")

print("4. ¿Cuántos cruces he recibido por cada tipo de TAG?")
for tipo_TAG, cant in cruces_tipo_TAG.items():
    print(f" {tipo_TAG}: {cant}")

print("5. ¿Cuántos cruces he recibido por cada categoría cobrada?")
for categoria, cant in cruces_cat_cobrada.items():
    print(f" {categoria}: {cant}")


output_file = "reporte_cruces_sairi.pdf"


create_pdf(output_file, tot_cruces_recibidos, importe_total, cruces_por_hora, cruces_tipo_TAG, cruces_cat_cobrada)
