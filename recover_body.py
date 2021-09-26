from Config import *
import os,sys
import time
import binascii
from struct import unpack
import sys
from pathlib import Path
import shutil,glob
import getpass
username=getpass.getuser()

def extract_code_dex(start_dex,end_dex,file_to_read):
    a=[]
    sub_end=end_dex[2:]
    running=False
    try:
        with open(file_to_read,"rb") as f:
            n = 0          
            b = f.read(16)  
            while b:
                s1 = " ".join([f"{i:02x}" for i in b]) # hex string
                s1 = s1[0:23] + " " + s1[23:]         # insert extra space between groups of 8 hex values
                s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in b]) # ascii string; chained comparison
                stringa=f"{n * 16:08x} "
                string_long=f"{s1:<48}"
                if start_dex in stringa:
                    running=True
                
                if sub_end in stringa:
                    running=False

                n = n+1
                b = f.read(16)

                if running:
                    a.extend([i.strip() for i in string_long.split(',')])
                    #print(a)

    except Exception as e:
        print(__file__, ": ", type(e).__name__, " - ", e, sep="", file=sys.stderr)
        pass
    return a


def listToString(s): 
    str1 = " " 
    return (str1.join(s))   


def recover_body_dex(lista_da_scan,lista_filtrata_file_dump):
    try:
        start_dex=lista_da_scan[-3].split()
        start_dex=start_dex[0]
        file_size=lista_da_scan[-2]
        file_size_final=file_size.split()[1] + file_size.split()[2] + file_size.split()[3]+file_size.split()[4]
        binary = binascii.unhexlify(str(file_size_final))
        result = unpack("<I", binary)[0]
        hex_size = "%08x" % result
        integer= int(start_dex,16)
        integer2=int(hex_size,16)
        hex1=hex(integer)
        hex2=hex(integer2)
        hex_final=hex(int(hex1,16) + int(hex2,16))
        body_lista=extract_code_dex(start_dex,hex_final,lista_filtrata_file_dump)
        body_finale=listToString(body_lista).replace(" ","")
        file_partenza1=copy_apk_to_tmp+"\\"+"file.txt" 
        with open(file_partenza1,"w") as file2:
            file2.write(body_finale)
        try:
            command=f'bash.exe -c "xxd -r -p {file_partenza} {file_arrivo}" '
            os.system(command)
            return 0

        except Exception as e:
            print(f"[-] Error: {e} [-]\n")
            return 1

    except Exception as e:
        print(f"[-] Error: {e} [-]\n")
        return 1     

def delete_junk():
    path=copy_apk_to_tmp+"\\*"
    fileNames = glob.glob(path)
    for filename in fileNames:
        try:
            os.remove(filename)
        except:
            shutil.rmtree(filename)

def rename_file(code):
    ok=0
    Path(body_dex_method).mkdir(parents=True, exist_ok=True)
    lista_non_so=[]
    with open(log,"r") as file4:
        lines=file4.readlines()
        for line in lines:
            lista_non_so.append(line)
            if code in line:
                indice=lista_non_so.index(line)
                break   
    
    method_name1=lista_non_so[indice-3].replace("Class name: ","")
    method_name1=method_name1.replace("\n","")
    method_name=lista_non_so[indice-2].replace("Target method name: ","")
    method_name=method_name.replace("\n","")
    #print(method_name)
    os.system(f"copy {file_body} {body_dex_method}")
    name_old=f"{body_dex_method}\\body.dex"
    name_new=f"{body_dex_method}\\{method_name1}_{method_name}.dex"
    try:
        os.rename(name_old,name_new)
        try:
            command_convert_to_jar=f"{convert2jar} -f -o {body_dex_method}\\{method_name}.jar {name_new}"
            os.system(command_convert_to_jar)
            #print("[+] dex2jar converted successfully [+]\n")
        except Exception as e:
            ok=1
            pass
            #print("[-] dex2jar converted failed [-]\n")
    except Exception as e:
        print(f"[-] File renamed failed  {e} [-]")
    
    return ok



def extract_methods(nome_metodo):
    running=False
    testo=[]
    if system() == 'Linux':
        file_log=log_Linux
    else:
        file_log=log


    with open(file_log,"r") as f:
        lines=f.readlines()
        for line in lines:
            if nome_metodo in line:
                running=True
            if "Hook method name:" in line:
                running=False
            if running:
                testo.append(line)
           
    
    testo_primo=testo[0].replace("Target method name: ","").replace("\n","")
    testo_secondo=testo[1].replace("Signature: ","").replace("\n","")
    nome_metodo_finale=testo_primo+testo_secondo

    return nome_metodo_finale


def substitute_body_method(NI,NF,path_smali,body_ok,class_name,method_name,nome_dir_body_protect):
    if system() == 'Linux':
        nome_dir_body_protect=nome_dir_body_protect+"/"
        dummy_file=f"/home/{username}/Scrivania/prova.smali"
    else:
        dummy_file=f"C:\\Users\\{username}\\OneDrive\\Desktop\\prova.smali"
        nome_dir_body_protect=nome_dir_body_protect+"\\"
    
    lines_to_remove=range(NI+1,NF)
    is_skipped = True
    current_index = 0
    with open(path_smali, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        for line in read_obj:
            if current_index not in lines_to_remove :
                write_obj.write(line)
            else:
                if is_skipped:
                    for element in body_ok:
                        if "hook(L" in element:
                            pass
                        else:
                            write_obj.write("    " + element)
                            write_obj.write("\n")
                    is_skipped=False
            current_index += 1
    
    finale=f"{final}{class_name}.smali"
    os.rename(dummy_file,finale)
    
    if system() == 'Linux':
        os.system(f"cp {finale} {nome_dir_body_protect}")
        os.remove(finale)
    else:
        os.system(f"copy {finale} {nome_dir_body_protect}")
        os.remove(finale)
    
    

def substitute_methods(nome_metodo,body_ok,nome_dir_body_protect):
    class_name=nome_metodo.split("_")[0]
    method_name=nome_metodo.split("_")[1]
    for root, dirs, files in os.walk(nome_dir_body_protect):
        for file_found in files:
            file_found_no_smali=file_found.replace(".smali","")
            if class_name == file_found_no_smali:
                path_smali=os.path.join(root, file_found)
                numero_inizio=""
                numero_fine=""
                nome_metodo_finale=extract_methods(method_name)
                #print(nome_metodo_finale)
                running=True
                a_file = open(path_smali,"r")
                for number, line in enumerate(a_file):
                    if nome_metodo_finale in line and ".method" in line:
                        #print("FOUND")
                        numero_inizio=number
                        running=False
                    
                    if ".end method" in line:
                        running=True
                        numero_fine=number
                    
                    if running:
                        if numero_inizio != "" and numero_fine != "":
                            numero_inizio_finale=numero_inizio
                            numero_fine_finale=numero_fine
                            break
                

                #print(nome_metodo_finale)
                substitute_body_method(int(numero_inizio_finale),int(numero_fine_finale),path_smali,body_ok,class_name,method_name,nome_dir_body_protect)


def listToString1(s): 
    str1 = "" 
    for ele in s: 
        str1 += "/"+ele  
    return str1 

def remove_injector(nome_dir_body_protect):
    if os.path.getsize(file_injector) > 0:
        #nome="/media/claudio/SharingBoot/sharing/Analisi/puzzle_1.22/smali/br/com/cjdinfo/puzzle/"
        first_check="checkVirtualEnvironment"
        second_check="checkAppSignature"
        for root, dirs, files in os.walk(nome_dir_body_protect):
            for file_found in files:
                if system() == 'Linux':
                    path_smali_completed=os.path.join(root, file_found)
                else:
                    path_smali_completed=os.path.join(root, file_found)
                    path_smali_completed=path_smali_completed.replace("\\","/").split("/")[1:]
                    path_smali_completed=listToString1(path_smali_completed)
                    path_smali_completed=f"/mnt/c/{path_smali_completed}"
                    
        
                if system() == 'Linux':
                    command = f"sed -i '/{first_check}/d' {path_smali_completed}" 
                    command2= f"sed -i '/{second_check}/d' {path_smali_completed}"
                else:
                    command= f'bash.exe -c  "sed -i "/{first_check}/d" {path_smali_completed}"'
                    command2= f'bash.exe -c  "sed -i "/{second_check}/d" {path_smali_completed}"'
                    
                os.system(command)
                os.system(command2)
    else:
        pass

def listToString2(s): 
    str1 = "" 
    for ele in s: 
        str1 += "\\"+ele  
    return str1 

def built_apk():
    if system() == 'Linux':
        dir_main=main_dir_Linux
    else:
        dir_main=main_dir

    nome_apk_modified=nome_apk.replace(".apk","")
    for root, dirs, files in os.walk(dir_main):
        for dirs_found in dirs:
            if nome_apk_modified in dirs_found:
                apk_pattern=os.path.join(root, dirs_found)

    if system() == 'Linux':
        comando=f"apktool b -d -f {apk_pattern}/"
        os.system(comando)
        for root, dirs, files in os.walk(f"{apk_pattern}/dist"):
            for files_found in files:
                apk_pattern_final=os.path.join(root, files_found)
                os.system(f"cp {apk_pattern_final} {outcomes}")
    else:
        apk_pattern=apk_pattern.replace("\\","/").split("/")[1:]
        apk_pattern=listToString1(apk_pattern)
        apk_pattern=f"/mnt/c/{apk_pattern}"
        print(apk_pattern)
        comando=f'bash.exe -c  "apktool b -d -f {apk_pattern}/ " '
        os.system(comando)
        #copy apk into outcomes
        apk_pattern=apk_pattern.split("/")[3:]
        apk_pattern=f"C:{listToString2(apk_pattern)}"
        
        for root, dirs, files in os.walk(f"{apk_pattern}\\dist"):
            for files_found in files:
                apk_pattern_final=os.path.join(root, files_found)
                comando=f"copy {apk_pattern_final}   {outcomes}"
                #comando=f'bash.exe -c  "cp {apk_pattern_final}  {outcomes_linux_APK}" '
                os.system(comando)

def deleteUtilHelper(numero_inizio_finale,numero_fine_finale,path_smali_completed,class_name,nome_dir_body_protect):
    dummy_file=f"C:\\Users\\{username}\\OneDrive\\Desktop\\prova.smali"
    if numero_inizio_finale == numero_fine_finale:
        class_name=class_name.replace(".smali","")
        is_skipped = True
        current_index = 0
        with open(path_smali_completed, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            for line in read_obj:
                if current_index != numero_inizio_finale:
                    write_obj.write(line)
                current_index += 1
    else:
        class_name=class_name.replace(".smali","")
        lines_to_remove=range(numero_inizio_finale,numero_fine_finale)
        is_skipped = True
        current_index = 0
        with open(path_smali_completed, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            for line in read_obj:
                if current_index not in lines_to_remove :
                    write_obj.write(line)
                current_index += 1
        
    finale=f"C:\\Users\\{username}\\OneDrive\\Desktop\\{class_name}.smali"
    os.rename(dummy_file,finale)
    os.system(f"copy {finale} {nome_dir_body_protect}")
    os.remove(finale)
    

def delete_last_things(nome_dir_body_protect):
    third_check="UtilHelper"
    first_check="checkVirtualEnvironment"
    second_check="checkAppSignature"
    #Al posto di final metterai la dir di smali con tutti i file
    for root, dirs, files in os.walk(nome_dir_body_protect):
        for file_found in files:
            if file_found.endswith(".smali"):
                path_smali_completed=os.path.join(root, file_found)
                #print(path_smali_completed)
                #Check UtilHelper and other JavaCheck
                count=0
                with open(path_smali_completed,"r") as files:
                    lines=files.readlines()
                    for number_check,line in enumerate(lines):
                        if first_check in line:
                            #print("first check")
                            #print(str(number_check)+ " " + line)
                            numero_inizio_finale=number_check
                            numero_fine_finale=number_check
                            deleteUtilHelper(int(numero_inizio_finale),int(numero_fine_finale),path_smali_completed,file_found,nome_dir_body_protect) 
                        if second_check in line:
                            #print("second check")
                            #print(str(number_check)+ " " + line)
                            numero_inizio_finale=number_check
                            numero_fine_finale=number_check
                            deleteUtilHelper(int(numero_inizio_finale),int(numero_fine_finale),path_smali_completed,file_found,nome_dir_body_protect) 
                        if third_check in line:
                            #print("third check")
                            count=count+1

                for i in range(count):
                    numero_inizio=""
                    numero_fine=""
                    running=True

                    a_file = open(path_smali_completed,"r")

                    for number, line in enumerate(a_file):
                        if third_check in line:
                            numero_inizio=number
                            numero_fine=int(numero_inizio) + 15
                            running=False

                        if number == numero_fine:
                            running = True
                            numero_fine=number
                        
                        if running:
                            if numero_inizio != "" and numero_fine != "":
                                numero_inizio_finale=numero_inizio
                                numero_fine_finale=numero_fine
                                #print(numero_inizio_finale)
                                #print(numero_fine_finale)
                                deleteUtilHelper(int(numero_inizio_finale),int(numero_fine_finale),path_smali_completed,file_found,nome_dir_body_protect) 
                                break


def delete_dir():
    if system() == 'Linux':
        path=copy_apk_to_tmp_Linux+"/*"
    else:
        path=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\puzzle_1.22\\smali\\embedded\\*"
    fileNames = glob.glob(path)
    for filename in fileNames:
        try:
            os.remove(filename)
        except:
            shutil.rmtree(filename)
    
    command=f"rmdir C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\puzzle_1.22\\smali\\embedded"
    os.system(command)

'''
################1 Times compare the method's code################################################

def rename_file(nome_codice,trovato):
    #print(nome_codice)
    Path(body_dex_method).mkdir(parents=True, exist_ok=True)
    lista_non_so=[]
    with open(log,"r") as file4:
        lines=file4.readlines()
        for line in lines:
            lista_non_so.append(line)
            if nome_codice in line:
                indice=lista_non_so.index(line)
                break
    
    method_name=lista_non_so[indice-3].replace("Class name: ","")
    method_name=method_name.replace("\n","")
    #print(method_name)
    os.system(f"copy {file_body} {body_dex_method}")
    if trovato==0:
        name_old=f"{body_dex_method}\\body.dex"
        name_new=f"{body_dex_method}\\{method_name}.dex"
        try:
            os.rename(name_old,name_new)
            time.sleep(1)
            try:
                command_convert_to_jar=f"{convert2jar} -f -o {body_dex_method}\\{method_name}.jar {name_new}"
                print(command_convert_to_jar)
                os.system(command_convert_to_jar)
                #print("[+] dex2jar converted successfully [+]\n")
            except Exception as e:
                pass
                print("[-] dex2jar converted failed [-]\n")
            print("[+] Body recovered successfully [+]\n")
        
        except Exception as e:
            print(f"[-] File renamed failed  {e} [-]")
    else:
        name_old=f"{body_dex_method}\\body.dex"
        name_new=f"{body_dex_method}\\{method_name}{str(trovato)}.dex"
        try:
            os.rename(name_old,name_new)
            time.sleep(1)
            try:
                command_convert_to_jar=f"{convert2jar} -f -o {body_dex_method}\\{method_name}{str(trovato)}.jar {name_new}"
                print(command_convert_to_jar)
                os.system(command_convert_to_jar)
                print("[+] dex2jar converted successfully [+]\n")

            except Exception as e:
                pass
                print("[-] dex2jar converted failed [-]\n")
            print("[+] Body recovered successfully [+]\n")
        
        except Exception as e:
            print(f"[-] File renamed failed {e} [-]")



def extract_code_dex(start_dex,end_dex,file_to_read,sub_code):
    a=[]
    sub_end=end_dex[2:]
    running=False
    try:
        with open(file_to_read,"rb") as f:
            n = 0          
            b = f.read(16)  
            while b:
                s1 = " ".join([f"{i:02x}" for i in b]) # hex string
                s1 = s1[0:23] + " " + s1[23:]         # insert extra space between groups of 8 hex values
                s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in b]) # ascii string; chained comparison
                stringa=f"{n * 16:08x} "
                string_long=f"{s1:<48}"
                #string_long=f"{n * 16:08x}  {s1:<48}  |{s2}|"
                if start_dex in stringa:
                    #print(string_long)
                    running=True
                
                if sub_end in stringa:
                    #print(string_long)
                    running=False

                n = n+1
                b = f.read(16)

                if running:
                    a.extend([i.strip() for i in string_long.split(',')])
                    #print(a)

    except Exception as e:
        print(__file__, ": ", type(e).__name__, " - ", e, sep="", file=sys.stderr)
        pass
    return a
                    
def delete_junk():
    path=copy_apk_to_tmp+"\\*"
    fileNames = glob.glob(path)
    for filename in fileNames:
        try:
            os.remove(filename)
        except:
            shutil.rmtree(filename)

def listToString(s): 
    str1 = " " 
    return (str1.join(s))   

def recover_body_dex(lista_da_scan,path_dump,sub_code):

    try:
        start_dex=lista_da_scan[-3].split()
        start_dex=start_dex[0]
        file_size=lista_da_scan[-2]
        file_size_final=file_size.split()[1] + file_size.split()[2]+ file_size.split()[3]+file_size.split()[4]
        binary = binascii.unhexlify(str(file_size_final))
        result = unpack("<I", binary)[0]
        hex_size = "%08x" % result
        integer= int(start_dex,16)
        integer2=int(hex_size,16)
        hex1=hex(integer)
        hex2=hex(integer2)
        hex_final=hex(int(hex1,16) + int(hex2,16))
        body_lista=extract_code_dex(start_dex,hex_final,path_dump,sub_code)
        body_finale=listToString(body_lista).replace(" ","")
        username=getpass.getuser()
        file_partenza1=copy_apk_to_tmp+"\\"+"file.txt" 
        with open(file_partenza1,"w") as file2:
            file2.write(body_finale)
        try:
            command=f'bash.exe -c "xxd -r -p {file_partenza} {file_arrivo}" '
            os.system(command)
            return 0
            #Path(body_dex_method).mkdir(parents=True, exist_ok=True)
            #command2=f'bash.exe -c "cp {file_arrivo} {file_arrivo}" '
        except Exception as e:
            print(f"[-] Error: {e} [-]\n")
            return 1
    except Exception as e:
        print(f"[-] Error: {e} [-]\n")
        return 1            
'''