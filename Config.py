#TODO: Look the real name of guestapp(for extract method use the container's package name)

import getpass
from platform import system


username=getpass.getuser()
nome_apk="puzzle_1.22.apk"
package_name_apk="com.example.trustedcontainervirtualapp" #run the guestapp in the container
package_name_apk1="br.com.cjdinfo.puzzle"
package_name_container="com.example.trustedcontainervirtualapp"


if system() == 'Linux':
    apkLinux=f"/media/{username}/SharingBoot/sharing/Analisi/Utility/apk/{nome_apk}"
    outcomes_linux_Linux=f"/media/{username}/SharingBoot/sharing/Analisi/Outcomes/smali_temp_body/"
    main_dir_Linux=f"/media/{username}/SharingBoot/sharing/Analisi/"
    outcomes=f"/media/{username}/SharingBoot/sharing/Analisi/Outcomes/"
    body_dex_method=f"/media/{username}/SharingBoot/sharing/Analisi/Outcomes/body_dex_method"
    pattern_linux_smali_body_extracted_Linux=f"/media/{username}/SharingBoot/sharing/Analisi/Outcomes/body_dex_method/"
    permissione_dex2smali_Linux=f"chmod +x /media/{username}/SharingBoot/sharing/Analisi/Utility/baksmali"
    dex2smali_Linux=f"bash {main_dir_Linux}Utility/baksmali d"
    final_outcomes_LINUX=f"{outcomes}smali_body/"
    log_Linux=f"{outcomes}log.txt"
    aapt_output_file=f"{outcomes}aapt_output_file.txt"
    copy_apk_to_tmp_Linux=f"{main_dir_Linux}tmp"
    final=f"/home/{username}/Scrivania/"
    
else:
    file_partenza=f"/mnt/c/Users/{username}/OneDrive/Desktop/Analisi/tmp/file.txt"
    file_arrivo=f"/mnt/c/Users/{username}/OneDrive/Desktop/Analisi/tmp/body.dex"
    outcomes_linux=f"Outcomes/smali_temp_body/"
    pattern_linux_smali_body_extracted=f"/mnt/c/Users/{username}/OneDrive/Desktop/Analisi/Outcomes/body_dex_method/"
    apk_linux=f"/mnt/c/Users/{username}/OneDrive/Desktop/Analisi/Utility/apk/{nome_apk}"
    outcomes_linux_APK=f"/mnt/c/Users/{username}/OneDrive/Desktop/Analisi/outcomes/"
    

    convert2jar=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\dex2jar-2.0\\d2j-dex2jar.bat"
    copy_apk_to_tmp=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\tmp"
    file_body=copy_apk_to_tmp+"\\"+"body.dex"
    body_dex_method=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Outcomes\\body_dex_method"
    apk=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Utility\\apk\\{nome_apk}"
    path_fridump=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\fridump\\"
    main_dir=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\"
    fridump=f"python {path_fridump}fridump.py -U -s {package_name_apk1}"
    dump=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\dump"
    pattern=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\js\\findAndBackupAndHook.js"
    outcomes=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Outcomes\\"
    outcomes_smali_windows=f"{outcomes}smali_temp_body\\"
    final_outcomes_windows=f"{outcomes}smali_body\\"
    aapt_output_file=f"{outcomes}aapt_output_file.txt"
    log=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Outcomes\\log.txt"
    lista_processi=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\tmp\\list_process.txt"
    aapt=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Utility\\aapt.exe"
    dexdump=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Utility\\dexdump.exe"
    apktool_extract=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Utility\\apktool.bat d -r -f"
    apktool_repack=f"C:\\Users\\{username}\\OneDrive\\Desktop\\Analisi\\Utility\\apktool.bat b -d -f"
    dex2smali=f"./Utility/baksmali d"
    final=f"C:\\Users\\{username}\\OneDrive\\Desktop\\"
    file_injector=f"{outcomes}{nome_apk}_injector_found.txt"