# -*- coding: utf-8 -*-
import re
import xlrd

#Array para guardar los errores durante el proceso
Err=[]
#Creamos una lista donde se guardarán las variables y constantes. 
Vars={}
Const={}
#Lista para guardar los mnemónicos registrados
Reg=[]
#Palabras reservadas
Reser=["ORG","EQU","FCB","END"]
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
dir_txt = 'C:/Users/Kike/Desktop/Proyecto EyPC/Inh.txt'   
dir_Exc = "C:/Users/Kike/Desktop/Proyecto EyPC/68HC11.xlsx"

#Método que inserta una lista en una lista
def Lista(lis):
    
    l=[]
    lis.append(l)
    return lis
#Método que elimina impurezas en la lista 
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
   
#Método que elimina impurezas en la regex
def Remueve(X):
   while " " in X: X.remove(" ")
   while "\t" in X: X.remove("\t")
   while "" in X: X.remove("")
   while "\n" in X: X.remove("\n")
   while None in X:X.remove(None)
   
   return X

#Método que separa los números de los símbolos
def Separa(arg):
    s=re.split("(\$)|(\#\$)|(\#)|(\s)",arg)
    Remueve(s)
    #print(s)
    if len(s)==0:
        s=""
        
    return s
   
def Registra(Archivo):
#Mientras se pueda abrir leemos linea a linea y contamos los datos
    with open(Archivo) as f:
    
        linea = f.readline()
        cnt=0
        while linea:
            Lista(Reg)
            #print(Reg,"\n",cnt)
            for i in range(4):
                Lista(Reg[cnt])
            #Separamos los comentarios 
            end=re.findall(r"end|END",linea)
            Com=re.findall(r"((^\*))", linea) 
            Esp=re.findall(r"(^\s(\s*\t*)[A-Za-z]*)", linea)
            #Separamos las constantes y variables en el registro
            Var=re.findall(r".*(\s|\t)(EQU|equ)(\s|\t)(\$(00)[A-Fa-f0-9]{2})",linea)
            Cons=re.findall(r".*(\s|\t)(EQU|equ)(\s|\t)(\$(10)[A-Fa-f0-9]{2})",linea)
            #Encontramos el primer END para regresar el registro
            if len(end)!=0:
                cnt+=1
                #print(cnt,"FIN")
                r=Remueve(re.split("(\s)+",linea))
                Lista(Reg)
                #print(Reg,"\n",cnt)
                Reg[cnt-1][0]=r[0]
                Reg[cnt-1][1]=""
                Reg[cnt-1][2]=""
                Reg[cnt-1][3]=cnt
                #print(Reg[cnt-1])
                f.close()
                return 1
                
            #Verificamos que sea un comentario 
            elif len(Com)!=0:

                cnt+=1
                #print(cnt,"Es comentario")
                linea = f.readline()
            #Verificamos que sea una constante
            elif len(Cons)!=0:
            
                cnt+=1
                r=Remueve(re.split("(\s)+",linea))
                r[2]=Separa(r[2])
                Const[r[0]]=r[2][1]
                #print(cnt,"Es Constante")
                linea = f.readline()
            #Verificamos que sea una variable    
            elif len(Var)!=0:
                
                r=Remueve(re.split("(\s)+",linea))
                r[2]=Separa(r[2])
                Vars[r[0]]=r[2][1]
                cnt+=1
                #print(cnt,"Es Variable")
                linea = f.readline()
            #Verificamos que cuente con al menos un espacio
            elif len(Esp)!=0:
                r=Remueve(re.split("(\s)+",linea))
                if len(r)!=1:
                    s=Separa(r[1])
                    r[1]=s[1]
                    r.append(s[0])
                cnt+=1

                r.append(cnt)
                #print(cnt,"Gud",r)  
                Reg[cnt-1][0]=r[0]
                #print(len(r),Reg[cnt-1])
                if len(r)<3:
                    Reg[cnt-1][1]="None"
                    Reg[cnt-1][2]="None"
                    Reg[cnt-1][3]=r[1]
                else:
                    Reg[cnt-1][1]=r[2]
                    Reg[cnt-1][2]=r[1]
                    Reg[cnt-1][3]=r[3]
                #print(Reg[cnt-1])
                linea = f.readline()
            
            #Si no hay espacio guardamos un error   
            else:
                cnt+=1
                r=Remueve(re.split("(\s)+",linea))
                r.append(cnt)
                Reg[cnt-1][0]=r[0]
                Err.append(("009","Linea "+str(cnt)))
                linea = f.readline()
                
#Método que regresa el valor para buscar en los Mnemónicos
def Modos(arg): 
    Modos={
            "#$": 1, #IMM
            "$": 2 , #DIR
            "INDX": 3, #INDX
            "INDY" : 4, #INDY
            "$": 5, #EXT
            "None": 6, #INH
            "REL" : 7 #REL
            }
    
    m=Modos.get(arg)             
    return m

#Método que compara los valores del registro con los mnemónicos
def Compara():
    #Lista donde se guardan los valores de la comparación
    L=[]
    #Compara los mnemónicos del registro con los del Excel
    for i in range(len(Reg)-1):
        a=Reg[i][0].lower()
        k=0
            
        for j in range(len(Mnem)):
            b=Mnem[j][0]

            
            #Si coincide, añadimos los valores según el modo de direccionamiento
            if a==b:
                #Si hay coincidencias con letras superiores a F 
                if Reg[i][2]=="None":
                    
                    x=Separa(Mnem[j][Modos(Reg[i][1])])

                    if len(x)>1:
                        x=x[0]+x[1]
                        L.append([x,Reg[i][3]])
                    else:
                        L.append([x[0],Reg[i][3]])
                        break
                else:
                    #print("\nRegistro: ",Reg)
                    
                    if Mnem[j][Modos(Reg[i][1])]=="-- ":

                        Err.append(("006","Linea "+str(Reg[i][3])))
                        break
                        
                    else:
                        L.append([str(Mnem[j][Modos(Reg[i][1])]),Reg[i][3]])
                        L.append([Reg[i][2],Reg[i][3]])
                    
            else:
                k+=1
#Si no encontró el mnemónico, y el registro no se encuentra en palabras reservadas hay error
        if k==145 and Reg[i][0] not in Reser:
            Err.append(("004","Linea "+ str(Reg[i][3])))
    return L
               
 
def Imprime(L):

    j=0
    cnt=0
    n=0
    print("\n   Dir\t\t  0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F")
    print("<",int(Reg[0][2]),">\t",end="")
    for i in range(len(L)):

        punto=re.findall(r"[0-9]*.*(\.)0",L[i][0])
        if len(punto)>0:
            L[i][0]=L[i][0][0:2]
        
        if len(L[i][0])==2:
            print(" ",L[i][0],end="")
            cnt+=1
            if cnt==16*(n+1):
                n+=1
                print("\n<",int(Reg[0][2])+10*n,">\t",end="")

            
        else:
            print(" ",L[i][0][0:2],end="")
            j+=1
            cnt+=1
            if cnt==16*(n+1):
                n+=1
                print("\n<",int(Reg[0][2])+10*n,">\t",end="")
                
            print(" ",L[i][0][2:4],end="")
            cnt+=1
            if cnt==16*(n+1):
                n+=1
                print("\n<",int(Reg[0][2])+10*n,">\t",end="")

def ImprimeErrores():
    print("\n\nErrores: \n")   
    for i in range(len(Err)):
        print("\033[1;31m ",Err[i][1]," ","\033[1;32m",Errores.get(Err[i][0]))
            
#Método que inicia el proceso
def main():
    
    CargaExcel(dir_Exc)
    
    if Registra(dir_txt)==1:
        print("Registro cargado correctamente")
    else:
        print("Error al cargar el archivo con el registro")
        return 0
    
    for i in range (len(Reg)):  
        RemueveL(Reg[i])
    RemueveL(Reg)
    
    if Reg[len(Reg)-1][0]!="END" and Reg[len(Reg)-1][0].lower()!="end":
        Err.append("010")
        
    print("\nConstantes: ",Const)
    print("\nVariables: ",Vars)
    print("\nRegistro: ",Reg)
    c=Compara()
    print("\nComparaciones: ", c)
    for i in range(len(c)):
        x=re.findall(r"[G-Zg-z]+",c[i][0])

        if c[i][0] in Const and len(x)!=0:
            c[i][0]=Const.get(c[i][0])
            
        elif c[i][0] in Vars and len(x)!=0:
            c[i]=Vars.get(c[i][0])
            
        elif c[i][0] not in Const and len(x)!=0:
            
            Err.append(("001","Linea "+ str(c[i][1])))
            Err.append(("003","Linea "+ str(c[i][1])))
        
        elif c[i][0] not in Vars and len(x)!=0:
            
            Err.append(("002","Linea "+ str(c[i][1])))
            Err.append(("003","Linea "+ str(c[i][1])))
            
        elif c[i][0] not in Const and c[i][0] not in Vars and len(x)!=0:
            
            Err.append(("003","Linea "+ str(c[i][1])))
            print("Etiqueta inexistente")
        
            
   
    Imprime(c)
    
    if(len(Err)!=0):
        ImprimeErrores()
    
main()
