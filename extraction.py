from Config import *
from recover_body import *

import os,sys
import time
import binascii
from struct import unpack
import sys
from pathlib import Path
import shutil,glob


def file_sorted(lista_codes):
    lista_files_dump=[]
    #mi da i path dei file code dei metodi
    for r,d,f in os.walk(copy_apk_to_tmp):
        for files in f:
            codes=files.replace(".txt","")
            path_file_txt=os.path.join(r,files)
            with open(path_file_txt,"r",encoding="latin-1") as file3:
                lines=file3.readlines()
                for line in lines:
                    if "strings.txt" in line or "314572800_dump" in line:
                        pass
                    else:
                        tupla=(codes,line)
                        lista_files_dump.append(tupla)
    lista_codes=sorted(lista_codes)

    return lista_files_dump,lista_codes


def convert(string):
    li = list(string.split(" "))
    return li


def extract_source_code():
    codes=[]
    with open(log,"r") as f:
        lines=f.readlines()
        for line in lines:
            if  "Hook method name:" in line:
                line=line.split(" ")
                line=line[6].split(".hook")
                codes.append(line[0])
    
    return codes


def recovered(lista_codes):
    list = os.listdir(dump)
    number_files = len(list)
    if number_files >0 :
        print (f"[+] Number of file in the dump dir: {number_files} [+]\n")
    else:
        print(f"[-] No file dump found [-]\n")
        sys.exit(0)

    for code in lista_codes:
        command=f'bash.exe -c " cd dump && grep {code} ./*" > tmp/{code}.txt'
        os.system(command)

    print("[+] Code files recovered successfully [+]\n")


def extraction_code(path_files):
    lista_line_binary_code=[]
    try:
        with open(path_files,"rb") as f:
            n = 0          
            b = f.read(16)  
            while b:
                s1 = " ".join([f"{i:02x}" for i in b]) # hex string
                s1 = s1[0:23] + " " + s1[23:]         # insert extra space between groups of 8 hex values
                s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in b]) # ascii string; chained comparison
                string=f"{n * 16:08x}  {s1:<48}  |{s2}|"
                lista_line_binary_code.append(string)
                n = n+1
                b = f.read(16)
    except Exception as e:
        print(__file__, ": ", type(e).__name__, " - ", e, sep="", file=sys.stderr)
        pass

    return lista_line_binary_code


def dex_size_namecodes(lista_files_dump,lista_codes):
    '''
    MEMORIA:
    file_dump = nome del file_dump
    path_file_dump = path del file_dump
    code = codice del metodo
    '''
    lista_filtrata_finale=[]
    lista_filtrata_file_dump=[]
    lista_filtrata_finale_code=[]
    lista_controllo=[]
    trovato=False
    count=0
    for element in lista_files_dump:
        #print(element)
        code=element[0]
        file_dump=convert(element[1])[2].replace("./","")
        for r,d,f in os.walk(dump):
            for files_found in f:
                if file_dump in files_found:
                    path_file_dump=os.path.join(r,files_found)
        
        lista_binary_code=extraction_code(path_file_dump)
        if len(lista_binary_code) > 0:
            n_elemento=0
            for element in lista_binary_code:
                #or "..I.CL"+code[0:1] in element
                if (("CL"+code[0:3] in element  or "L"+code[0:3] in element) or (code[0:5] in element and "CL" in lista_binary_code[n_elemento-1]) 
                or (code[3:10] in element and "CL" in lista_binary_code[n_elemento-1]) or (code[4:11] in element and "CL" in lista_binary_code[n_elemento-1])  
                or (code[5:12] in element and "CL" in lista_binary_code[n_elemento-1]) and (code not in lista_controllo) ):

                    lista_controllo.append(code)
                    #print(element)
                    trovato=True
                n_elemento=n_elemento+1
            
            if trovato == True:
                lista_filtrata_file_dump.append(path_file_dump)
                lista_filtrata_finale_code.append(code)
                lista_filtrata=[]
                #print(code)
                #print(path_file_dump)
                n_elemento=0
                count=0
                lista_controllo2=[]
                for element in lista_binary_code:
                    if "dex." in element:
                        lista_filtrata.append(element)
                        lista_filtrata.append(lista_binary_code[count+2])

                    if (("CL"+code[0:3] in element  or "L"+code[0:3] in element) or (code[0:5] in element and "CL" in lista_binary_code[n_elemento-1]) 
                    or (code[3:10] in element and "CL" in lista_binary_code[n_elemento-1])  or (code[4:11] in element and "CL" in lista_binary_code[n_elemento-1])  
                    or (code[5:12] in element and "CL" in lista_binary_code[n_elemento-1]) and (code not in lista_controllo2) ):
                        lista_controllo2.append(code)
                        lista_filtrata.append(element)
                        break

                    count=count+1
                    n_elemento=n_elemento+1
                
                
                lista_filtrata_finale.append(lista_filtrata)
                lista_filtrata=[]
            else:
                pass
        
        else:
            print("[-] Lista Binary code empty [-]\n")

        trovato=False
    

    return lista_filtrata_finale,lista_filtrata_file_dump,lista_filtrata_finale_code     


def extraction():
    try:
        lista_codes=extract_source_code()
        print("[+] Method Code extracted successfully [+]\n")
        print("[?] Running Fridump... [?]\n")
        os.system(fridump)
        print("[+] Fridump process done [+]\n")
        recovered(lista_codes)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    
    try:
        lista_files_dump,lista_codes=file_sorted(lista_codes)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    

    try:
        lista_filtrata_finale,lista_filtrata_file_dump,lista_filtrata_finale_code=dex_size_namecodes(lista_files_dump,lista_codes)
        #print(str(len(lista_filtrata_finale)) + " " + str(len(lista_filtrata_file_dump)) + " " + str(len(lista_filtrata_finale_code)) )
        print("[+] Collection dex + size and name codes of method completed successfully [+]\n")    
        time.sleep(1)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    
    
    try:
        count_Ok=0
        count_NO=0
        number_operations_final= (len(lista_filtrata_finale)  + len(lista_filtrata_file_dump) + len(lista_filtrata_finale_code))/3
        print(f"[?] Number of operation to recover all methods: {str(int(number_operations_final))} [?]\n")
        print("===========================================================================")
        #print(lista_filtrata_finale[5])
        #print(lista_filtrata_finale_code[5])
        #print(lista_filtrata_file_dump[5])

        for body,file_dump,code in zip(lista_filtrata_finale,lista_filtrata_file_dump,lista_filtrata_finale_code):
            flag=recover_body_dex(body,file_dump)
            if flag==0:
                try:
                    ok=rename_file(code)
                    if ok==0:
                        print("[+] dex2jar converted successfully [+]\n")
                        count_Ok = count_Ok + 1
                    else:
                        print("[-] dex2jar converted failed [-]\n")
                except Exception:
                    count_NO = count_NO + 1
            else:
                count_NO = count_NO + 1
           
        
        print(f"Total number of Body: {str(int(number_operations_final))}")
        print(f"Total number Body recovered successfully: {str(count_Ok)}")
        print(f"Total number Body recovered unsuccessfully: {str(count_NO)}\n")

    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    

    try:
        delete_junk()
        print("[+] Cleaning temp file completed [+]\n")
    except Exception as e:
        print(f"[-] Cleaning temp file failed: {e} [-]\n")

    

