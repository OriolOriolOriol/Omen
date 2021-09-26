from remove_all_file import delete
from omen import starting
from Config import *
import time



if __name__=="__main__":
    start = time.time()
    starting()
    error,error1=delete(nome_apk)
    if error == 0 and error1==0:
        print("[+] Deleting temporary files completed successfully [+]\n")
    if error == 1:
        print(f"[-] Error found in removing temp files in the main dir[-]\n")
    if error1 == 1:
        print(f"[-] Error found in removing temp files in the outcomes dir[-]\n")
    if error == 1 and error1==1:
        print(f"[-] Error found in all cases[-]\n")

    end = time.time()
    print (f"[+] Running time: {str(end - start)} [+]")
   