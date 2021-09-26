from Config import *
from read_code_smali import Read_code_smali
import sys,os,time
import glob,zipfile
from platform import system
import shutil
from pathlib import Path

def is_tool(name):
    from shutil import which
    return which(name) is not None



def run_Code_extract(newname,APKpath,APP_code,nome_apk):
    lista_dex=[]
    file_code_txt= APP_code + nome_apk + ".txt"
    with zipfile.ZipFile(newname,"r") as zip_ref:
        zip_ref.extractall(APKpath)
    

    if system() == 'Linux':
        considered=f"{APKpath}/*.dex"
    else:
        considered=f"{APKpath}\\*.dex"

    for file_dex in glob.glob(considered):
        lista_dex.append(file_dex)
    
    if len(lista_dex) > 0:
        count=0
        for i in lista_dex:
            if count == 0:
                if system() == 'Linux':
                    answer=is_tool("dexdump")
                    if answer == "False":
                        command0=f"sudo apt install dexdump"
                        os.system(command0)
                        command = f"dexdump -d   {i}   >  {file_code_txt}"
                    else:
                        command = f"dexdump -d   {i}   >  {file_code_txt}"
                else:
                    command = f"{dexdump} -d   {i}   >  {file_code_txt}"

                result0 = os.popen(command)
                time.sleep(20)
            else:
                if system() == 'Linux':
                    answer=is_tool("dexdump")
                    if answer == "False":
                        command0=f"sudo apt install {dexdump}"
                        os.system(command0)
                        command = f"{dexdump} -d   {i}   >>  {file_code_txt}"
                    else:
                        command = f"{dexdump} -d   {i}   >>  {file_code_txt}"
                else:
                    command = f"{dexdump} -d   {i}   >>  {file_code_txt}"
                
                result1 = os.popen(command)
                time.sleep(20)
            
            count = count + 1
        
        if os.stat(file_code_txt).st_size != 0:
            return 0
        else:
            return 1
    else:
        return 1


def delete_junk():
    if system() == 'Linux':
        path=copy_apk_to_tmp_Linux+"/*"
    else:
        path=copy_apk_to_tmp+"\\*"
    fileNames = glob.glob(path)
    for filename in fileNames:
        try:
            os.remove(filename)
        except:
            shutil.rmtree(filename)


def run_extraction_injector():
    if system() == 'Linux':
        Path(copy_apk_to_tmp_Linux).mkdir(parents=True, exist_ok=True)
    else:
        Path(copy_apk_to_tmp).mkdir(parents=True, exist_ok=True)
    
    print("[?] Manifest extraction & component information from apk file... [?]\n")
    if system() == 'Linux':
        answer=is_tool("aapt")
        if answer == "False":
            command0=f"sudo apt install aapt"
            os.system(command0)
            command = f"aapt l -a  {apkLinux} >   {aapt_output_file}"
        else:
            command = f"aapt l -a  {apkLinux} >   {aapt_output_file}"
    else:
        command = f"{aapt} l -a  {apk} >   {aapt_output_file}"

    result = os.popen(command)
    time.sleep(30)
    if os.stat(aapt_output_file).st_size != 0:
        print("[+] The Manifest extraction worked!!! [+]\n")
        if system() == 'Linux':
            os.system(f"cp {apkLinux} {copy_apk_to_tmp_Linux} ")
        else:
            os.system(f"copy {apk} {copy_apk_to_tmp} ")
        portion = os.path.splitext(nome_apk)
        if portion[1] == ".apk":
            if system() == 'Linux':
                new_name=copy_apk_to_tmp_Linux + "/" + portion[0] + ".zip"
                old_name=copy_apk_to_tmp_Linux + "/" + nome_apk
            else:
                new_name=copy_apk_to_tmp + "\\" + portion[0] + ".zip"
                old_name=copy_apk_to_tmp + "\\" + nome_apk
            
            os.rename(old_name,new_name)
            print("[+] Rename file successfully [+]")
            print("\n[?] Code Smali extraction [?]\n")
            if system() == 'Linux':
                flag=run_Code_extract(new_name,copy_apk_to_tmp_Linux,outcomes,nome_apk)
            else:
                flag=run_Code_extract(new_name,copy_apk_to_tmp,outcomes,nome_apk)
            if flag == 0:
                print ("[+] Extracting the code file successfully！[+]")
                delete_junk()
                print("\n[?] Reading Code smali... [?]\n")
                for r,d,f in os.walk(outcomes):
                    for files in f:
                        if nome_apk in files:
                            path_file_dex=os.path.join(r,files)
                
               
                Read_code_smali(path_file_dex,nome_apk)

            else:
                print("[-] Unable to extract smali code from dex file..!! [-]")
            
    else:
        print("[-] Manifest file extraction failed!!! [-]\n")
        sys.exit(0)

