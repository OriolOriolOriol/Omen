from Config import *
from recover_body import *
import getpass
import os
from androguard.core.bytecodes.apk import APK
from pathlib import Path
from platform import system
import filecmp,glob,time
import itertools

username=getpass.getuser()

def protect_apk2_smali():
    if system() == 'Linux':
        Path(outcomes_linux_Linux).mkdir(parents=True, exist_ok=True)
        comando=f"apktool d -r -f {apkLinux}"
        os.system(comando)
        a = APK(apkLinux)
        
    else:
        Path(outcomes_linux).mkdir(parents=True, exist_ok=True)
        comando=f'bash.exe -c  "apktool d -r -f {apk_linux} " '
        os.system(comando)
        a = APK(apk)

    nome_app=a.get_filename()
    if system() == 'Linux':
        nome_app=nome_app.split("/")[-1]
    else:
        nome_app=nome_app.split("\\")[-1]
    nome_app=nome_app.replace(".apk","")
    nome_package=a.get_package()
    nome_package=nome_package.split(".")[-1]
    if system() == 'Linux':
        path=main_dir_Linux+nome_app
    else:
        path=main_dir+nome_app
    for root, dirs, files in os.walk(path):
        for dir_found in dirs:
            if nome_package == dir_found:
                path_smali=os.path.join(root, nome_package)
                nome_dir_body_protect=path_smali
    
    return nome_dir_body_protect


def dex2smali_body_extracted(nome_dir_body_protect):
    if system() == 'Linux':
        path_method_extracted=body_dex_method + "/"
    else:
        Path(outcomes_smali_windows).mkdir(parents=True, exist_ok=True)
        path_method_extracted=body_dex_method + "\\"

    lista_nomi_methods=[]
    lista_path_nomi_methods=[]
    for root, dirs, files in os.walk(nome_dir_body_protect):
        for file_found in files:
            path_smali_completed=os.path.join(root, file_found)
            if system()== 'Linux':
                path_smali_completed=path_smali_completed.split("/")[-1].replace(".smali","")
            else:
                path_smali_completed=path_smali_completed.split("\\")[-1].replace(".smali","")

            #print("Nome Body: " + path_smali_completed)
            #print("Path  of Body: " + path_smali_completed_real_path)
            for root, dirs, files in os.walk(path_method_extracted):
                for file_found1 in files:
                    if file_found1.endswith(".dex") and  path_smali_completed in file_found1:
                        if system()== 'Linux':
                            path_body_method_completed=pattern_linux_smali_body_extracted_Linux + file_found1
                        else:
                            path_body_method_completed=pattern_linux_smali_body_extracted + file_found1 
                        #print(path_body_method_completed)
                        if system() == 'Linux':
                            os.system(permissione_dex2smali_Linux)
                            command=f"{dex2smali_Linux} {path_body_method_completed} --output {outcomes_linux_Linux}{file_found1}" 
                        else:
                            command= f'bash.exe -c  "{dex2smali} {path_body_method_completed} --output {outcomes_linux}{file_found1} " '

                        os.system(command)
                                  
    return lista_nomi_methods


def list_path_smali_body_extracted():
    lista_file_smali=[]
    if system() == 'Linux':
        outcomes_smali=outcomes_linux_Linux
    else:
        outcomes_smali=outcomes_smali_windows
    for root, dirs, files in os.walk(outcomes_smali):
        for directory in dirs:
            path_smali_code=os.path.join(root, directory)
            if system() == 'Linux':
                pattern=path_smali_code+"/"
            else:
                pattern=path_smali_code+"\\"
            os.chdir(pattern)
            for file1 in glob.glob("*.smali"):
                path_file_smali_body_extracted=os.path.join(pattern, file1)
                lista_file_smali.append(path_file_smali_body_extracted)
    
    return lista_file_smali

def filter_body_extracted(lista_file_smali):
    if system() == 'Linux':
        Path(final_outcomes_LINUX).mkdir(parents=True, exist_ok=True)
        final_outcomes=final_outcomes_LINUX
    else:
        Path(final_outcomes_windows).mkdir(parents=True, exist_ok=True)
        final_outcomes=final_outcomes_windows

    for element in lista_file_smali:
        if system() == 'Linux':
            name_file=element.split("/")[-2].replace(".dex","")
        else:
            name_file=element.split("\\")[-2].replace(".dex","")
        name_file=name_file+".smali"
        #print(name_file)
        if system() == 'Linux':
            os.system(f"cp {element} {final_outcomes}{name_file}")
        else:
            os.system(f"copy {element} {final_outcomes}{name_file}")
    
    lista_file_smali_last=[]
    for root, dirs, files in os.walk(final_outcomes):
        for file_found in files:
            path_file_smali_body_extracted=os.path.join(root, file_found)
            lista_file_smali_last.append(path_file_smali_body_extracted)


    lista=[]
    #lista_f1=[]
    for f1, f2 in itertools.combinations(lista_file_smali_last, 2):
        try:
            if filecmp.cmp(f1, f2,shallow=False) == True:
                #print(f"SI {f1}  ----- {f2}\n")
                os.remove(f2)
    
        except Exception:
            pass

    for root, dirs, files in os.walk(final_outcomes):
        for file_found in files:
            path_file_smali_body_extracted=os.path.join(root, file_found)
            lista.append(path_file_smali_body_extracted)
    
    return lista    



def repackaging():
    try:
        nome_dir_body_protect=protect_apk2_smali()
        print("\n[+] Conversion apk protect in smali completed [+]\n")
    except Exception as e:
        print(f"\n[-] Error found {e} [-]\n")

    try:
        lista_names_methods=dex2smali_body_extracted(nome_dir_body_protect)
        print("[+] Conversion body extracted in smali completed [+]\n")
        time.sleep(1)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
        
    
    try:
        lista_file_smali=list_path_smali_body_extracted()
        filtred_list_body=filter_body_extracted(lista_file_smali)
        print("[+] Filtering body extracted completed [+]\n")
        time.sleep(1)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    

    try:
        for element in filtred_list_body:
            if system() == 'Linux':
                nome_file=element.split("/")[-1].split(".")[-2]
            else:
                nome_file=element.split("\\")[-1].split(".")[-2]

            nome_file=nome_file.replace('1','')
            nome_file=nome_file.replace('2','')
            nome_file=nome_file.replace('3','')
            nome_metodo=nome_file
            #print(nome_file)
            register=False
            lettura=[]
            with open(element,"r") as file_reading:
                lines=file_reading.readlines()
                for line in lines:
                    #print(line)
                    if "hook(L" in line:
                        register=True
                    
                    if ".end method" in line:
                        register=False
                    
                    if register:
                        lettura.append(line)
            
            lettura = map(lambda s: s.strip(), lettura)
            body_ok=lettura
            substitute_methods(nome_metodo,body_ok,nome_dir_body_protect)
        print("[+] Methods body changed successfully [+]\n")
        time.sleep(1)
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    
    try:
        remove_injector(nome_dir_body_protect)
        delete_last_things(nome_dir_body_protect)
        delete_dir()
        print("[+] Deleting injector from apk completed successfully [+]\n")
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")
    

    try:
        '''
        destinazione="C:\\Users\\claud\\OneDrive\\Desktop\\Analisi\\puzzle_1.22\\smali\\br\\com\\cjdinfo\\puzzle\\"
        cartella="C:\\Users\\claud\\OneDrive\\Desktop\\cartellaaa\\"
        for root, dirs, files in os.walk(cartella):
            for dir_found in dirs:
                if dir_found == "puzzle":
                    path_smali=os.path.join(root, dir_found)
                    for root, dirs, files in os.walk(path_smali):
                        for file_found in files:
                            path_smali_file=os.path.join(root, file_found)
                            command=f"copy {path_smali_file} {destinazione}"
                            os.system(command)
        '''
        
        built_apk()
        print("[+] Apk built successfully [+]\n")
        
    except Exception as e:
        print(f"[-] Error found {e} [-]\n")




