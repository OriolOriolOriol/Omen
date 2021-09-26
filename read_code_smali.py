from platform import system
import os

def Read_code_smali(path_file_dex,nome_apk):
    rootPath = os.getcwd()
    if system() == 'Linux':
        path_outcome=f"{rootPath}/Outcomes/"
    else:
        path_outcome=f"{rootPath}\\Outcomes\\"
    
    path_outcome1= path_outcome + f"{nome_apk}_injector_found.txt"
    #TODO: Eliminare tale file

    with open(path_file_dex, "rU",encoding="latin1") as f:
        check_ENV=[]
        check_SIG=[]
        i = 0
        class_count = 0
        lines = f.readlines()
        lines_length = len(lines)
        while i <= lines_length - 3:

            while lines[i].find("invoke-static") >= 0 and lines[i].find("Lembedded/JavaIntegrityChecks") >= 0 and i <= lines_length - 3:
                
                if "checkVirtualEnvironment" in lines[i]:
                    method_name=lines[i-1].split(" ")
                    method_name_final=method_name[-1]
                    method_name_final=method_name_final.split(":")
                    invocation_control=lines[i]
                    invocation_control=invocation_control.split("invoke-static {},",1)[1]
                    invocation_control=invocation_control.split("//",1)[0]
                    stringa=f"\n[+] CheckVirtualEnvironment [+]:\n Method: {method_name_final[0]}\n Signature: {method_name_final[1]} Type of Control: {invocation_control} \n ======================================================================="
                    check_ENV.append(stringa)
                    #print(f"\n[+] CheckVirtualEnvironment [+]:\n Method: {method_name_final[0]}\n Signature: {method_name_final[1]} Type of Control: {invocation_control} \n =======================================================================")
                    i = i + 1
                
                if "checkAppSignature" in lines[i]:
                    method_name=lines[i-7].split(" ")
                    method_name_final=method_name[-1]
                    method_name_final=method_name_final.split(":")
                    invocation_control=lines[i]
                    invocation_control=invocation_control.split("},")[1]
                    invocation_control=invocation_control.split("//",1)[0]
                    stringa1=f"\n[+] checkAppSignature [+]:\n Method: {method_name_final[0]}\n Signature: {method_name_final[1]} Type of Control: {invocation_control} \n ======================================================================="
                    check_SIG.append(stringa1)
                    #print(stringa1)
                    i = i + 1
                
                i = i + 1
            



            i = i + 1
    
    if len(check_ENV) > 0 and len(check_SIG) > 0:
        print("[+] checkAppSignature & CheckVirtualEnvironment FOUND [+]\n")
        with open(path_outcome1, "w") as f:
            f.write("[!!!] CheckVirtualEnvironment [!!!]")
            for element in check_ENV:
                f.write(element)
            
            f.write("\n\n")
            f.write("[!!!] checkAppSignature [!!!]")
            for element in check_SIG:
                f.write(element)
    else:
        print("[-] No controls FOUND [-]\n")
    
    if os.stat(path_outcome1).st_size != 0:
        print("[+] Injector function FOUND [+]\n")
        os.remove(path_file_dex)
    else:
        print("[-] Error: Injector function NOT FOUND [-]\n")
    

    
    
    
        

        
            
         





#Read_code_smali("C:\\Users\\claud\\OneDrive\\Desktop\\Analisi\\Outcomes\\puzzle_1.22.apk.txt","puzzle_1.22.apk")