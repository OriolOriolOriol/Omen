from Config import *
import os,glob
import shutil

def delete(nome_apk):
    error = 0 
    nome_apk=nome_apk.replace(".apk","")
    for root, dirs, files in os.walk(main_dir):
        try:
            for dir_found in dirs:
                path_smali_completed=os.path.join(root, dir_found)
                if dir_found == "dump":
                    fileNames = glob.glob(path_smali_completed)
                    for filename in fileNames:
                        try:
                            os.remove(filename)
                        except:
                            shutil.rmtree(filename)

                if nome_apk in dir_found:
                    fileNames = glob.glob(path_smali_completed)
                    for filename in fileNames:
                        try:
                            os.remove(filename)
                        except:
                            shutil.rmtree(filename)
        except Exception as e:
            error=1
            pass
    
    error1=0
    for root, dirs, files in os.walk(outcomes):
        try:
            for dir_found in dirs:
                path_smali_completed=os.path.join(root, dir_found)
                fileNames = glob.glob(path_smali_completed)
                for filename in fileNames:
                    try:
                        os.remove(filename)
                    except:
                        shutil.rmtree(filename)

        except Exception as e:
            for root, dirs, files in os.walk(outcomes):
                try:
                    for dir_found in dirs:
                        path_smali_completed=os.path.join(root, dir_found)
                        command=f'bash.exe -c "rm -rf  {path_smali_completed} " '
                        os.system(command)
                except Exception:
                    error1=1
                    pass

            pass
    
    for root, dirs, files in os.walk(outcomes):
        for files_found in files:
            if "log.txt" in files_found or "log" in files_found:
                os.remove(log)
            else:
                pass
    
    return error,error1


        
    