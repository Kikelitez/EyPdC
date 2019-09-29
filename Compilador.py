# -*- coding: utf-8 -*-
import re
import xlrd
import numpy

#Array para guardar los errores durante el proceso
Err=[]
#Creamos una lista donde se guardarán las variables y constantes. 
Vars={}
Const={}
#Lista para guardar los mnemónicos registrados
Reg=[]
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
#Definimos las listas donde se guardarán los mnemónicos para compararlos con los registros leidos
Mnem = []
#Dirección de los archivos
dir_txt = 'C:/Users/Kike/Desktop/Proyecto EyPC/Ejemplo.txt'   
dir_Exc = "C:/Users/Kike/Desktop/Proyecto EyPC/68HC11.xlsx"

def Lista(lis):
    
    l=[]
    lis.append(l)
    return lis

def RemueveL(lista):
    while [] in lista: lista.remove([])
    return lista
    
def CargaExcel(Archivo):

    #Abrimos el archivo para trabajar y buscamos la hoja que usaremos
    workbook = xlrd.open_workbook(Archivo)
    sheet = workbook.sheet_by_name('Instrucciones')

    #Dentro de la hoja, leemos fila por fila y separamos los datos.
    for rownum in range(sheet.nrows):
        v=sheet.cell(rownum, 1).value
        Lista(Mnem)
            
            
        if len(v)<7 and len(v)>2:

                Mnem[rownum].append(sheet.cell(rownum, 1).value)
                Mnem[rownum].append(sheet.cell(rownum, 2).value)
                Mnem[rownum].append(sheet.cell(rownum, 5).value)
                Mnem[rownum].append(sheet.cell(rownum, 8).value)
                Mnem[rownum].append(sheet.cell(rownum, 11).value)
                Mnem[rownum].append(sheet.cell(rownum, 14).value)
                Mnem[rownum].append(sheet.cell(rownum, 17).value)
                Mnem[rownum].append(sheet.cell(rownum, 20).value)
    
    RemueveL(Mnem)
    
def Remueve(linea):
   X=re.split("(\s)+",linea)
   while " " in X: X.remove(" ")
   while "\t" in X: X.remove("\t")
   while "" in X: X.remove("")
   while "\n" in X: X.remove("\n")
   return X

def Separa(arg):
    if(len(arg)==6):
        print(arg[0]+arg[1])
    return
   
def Registra(Archivo):
#Mientras se pueda abrir leemos linea a linea y contamos los datos
    with open(Archivo) as f:
    
        linea = f.readline()
        cnt=0
        while linea:
            #Separamos los comentarios 
            end=re.findall(r"end|END",linea)
            Com=re.findall(r"((^\*))", linea) 
            Esp=re.findall(r"(^\s(\s*\t*)[A-Za-z]*)", linea)
            #Separamos las constantes y variables en el registro
            Var=re.findall(r".*(\s|\t)(EQU|equ)(\s|\t)(\$(00)[A-Fa-f0-9]{2})",linea)
            Cons=re.findall(r".*(\s|\t)(EQU|equ)(\s|\t)(\$(10)[A-Fa-f0-9]{2})",linea)
            #Encontramos el primer END para regresar el registro
            if len(end)!=0:
                
                #print(cnt,"FIN")
                linea = f.readline()

                break
            #Verificamos que sea un comentario 
            elif len(Com)!=0:

                cnt+=1
                #print(cnt,"Es comentario")
                linea = f.readline()
            #Verificamos que sea una constante
            elif len(Cons)!=0:
            
                cnt+=1
                r=Remueve(linea)
                Const[r[0]]=r[2]
                #print(cnt,"Es Constante")
                linea = f.readline()
            #Verificamos que sea una variable    
            elif len(Var)!=0:
                
                r=Remueve(linea)
                Vars[r[0]]=r[2]
                cnt+=1
                #print(cnt,"Es Variable")
                linea = f.readline()
            #Verificamos que cuente con al menos un espacio
            elif len(Esp)!=0:
                r=Remueve(linea)
                Separa(r[1])
                cnt+=1
                print(cnt,"Gud",linea)  
                Reg.append(r)
                linea = f.readline()
            
            #Si no hay espacio guardamos un error   
            else:
                cnt+=1
                r=Remueve(linea)
                print(r)
                Err.append(("009",cnt))
                #print("Error")
                linea = f.readline()
                               
 
    
    
def Compara():
    #for i in range(len(Mnem)-1):
        #print(Mnem[i][0])
    return 0
                        

CargaExcel(dir_Exc)
Registra(dir_txt)
Compara()
print("Registro",Reg)
print("Errores:",Err)      
    

              