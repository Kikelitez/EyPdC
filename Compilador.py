# -*- coding: utf-8 -*-
import re
import xlrd

#Array para guardar los errores durante el proceso
Err=[]
#Diccionario de Errores
Errores={"001" : "Constante Inexistente",
         "002" : "Variable Inexistente",
         "003" : "Etiqueta Inexistente",
         "004" : "Mnemónico Inexistente",
         "005" : "Instrucción Carece de Operandos ",
         "006" : "Instrucción No Lleva Operando(s)",
         "007" : "Magnitud de Operando Errónea",
         "008" : "Salto Relativo Muy Lejano",
         "009" : "Instrucción carece de un espacio relativo al margen",
         "010" : "No se encuentra END"}
#Encontramos la dirección del archivo
ArchivoExcel = "C:/Users/Kike/Desktop/Proyecto EyPC/68HC11.xlsx"
#Abrimos el archivo para trabajar y buscamos la hoja que usaremos
workbook = xlrd.open_workbook(ArchivoExcel)
sheet = workbook.sheet_by_name('Instrucciones')
#Definimos las listas donde se guardarán los mnemónicos para compararlos con los registros leidos
Mnem = []
IMM = []
DIR = []
INDX = []
INDY = []
EXT = []
INH = []
REL = []

#Dentro de la hoja, leemos fila por fila y separamos los datos.
for rownum in range(sheet.nrows):
    v=sheet.cell(rownum, 1).value
    if len(v)<5 and len(v)>2:
            Mnem.append(sheet.cell(rownum, 1).value)
            IMM.append(sheet.cell(rownum, 2).value)
            DIR.append(sheet.cell(rownum, 5).value)
            INDX.append(sheet.cell(rownum, 8).value)
            INDY.append(sheet.cell(rownum, 11).value)
            EXT.append(sheet.cell(rownum, 14).value)
            INH.append(sheet.cell(rownum, 17).value)
            REL.append(sheet.cell(rownum, 20).value)

#Se lee el archivo con registros
dir_txt = 'C:/Users/Kike/Desktop/Proyecto EyPC/Ejemplo.txt'   
#Creamos una lista donde se guardarán las variables y constantes. 
Vars=[]
Const=[]

#Mientras se pueda abrir leemos linea a linea y contamos los datos
with open(dir_txt) as f:
    
    linea = f.readline()
    cnt=0
    
    while linea:
    #Separamos los comentarios 
        Com=re.findall(r"((^\*))", linea)
        Esp=re.findall(r"(^\s(\s*\t*)[A-Za-z]*)", linea)
    #Variable para separar las constantes en el registro
        Equ=re.findall(r"(EQU|equ)",linea)
        
        #Verificamos que no sea un comentario 
        if len(Com)!=0:

            cnt+=1
            print(cnt,"Es comentario")
            linea = f.readline()
         
        #Verificamos que cuente con al menos un espacio
        elif len(Esp)!=0:
            
            cnt+=1
            print(cnt,linea,"Gud")   
            linea = f.readline()
            
        #Si no hay espacio guardamos un error   
        else:
            cnt+=1
            Err.append(("009",cnt))
            print(cnt,linea,"Error")
            linea = f.readline()
            print("Errores:",Err)
    
       

