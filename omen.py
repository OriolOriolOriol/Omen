#TODO: Command monkey: adb -s emulator-5554 shell monkey -p  com.example.trustedcontainervirtualapp -v 1000
#TODO: Remove file (log file after used)
from extract_Code import run_extraction_injector
from extraction import extraction
from repackaging import repackaging
from Config import *

from ppadb.client import Client as AdbClient
import os,sys
import frida
import time
import threading
from pathlib import Path
import colorama
from colorama import Fore
colorama.init()

try:
    device= frida.get_usb_device()
    print(f"[+] Device: {device} [+]\n")
    event=threading.Event()
except Exception:
    print("[-] Emulator offline [-]\n")

def intro():
    blue=Fore.GREEN
    print(blue+"\t\t\t\t+=======================================+")
    print(blue+"\t\t\t\t|..................OMEN.................|")
    print(blue+"\t\t\t\t+---------------------------------------+")
    print(blue+"\t\t\t\t|#Author: Claudio Rimensi               |")
    print(blue+"\t\t\t\t|#Date of creation: 22/07/2021          |")
    print(blue+"\t\t\t\t|#The premature optimization is a root  |")
    print(blue+"\t\t\t\t|of all evil.. :)                       |")
    print(blue+"\t\t\t\t+=======================================+")
    print(blue+"\t\t\t\t|..................OMEN.................|")
    print(blue+"\t\t\t\t+---------------------------------------+")

def my_message_handler(message,payload):
    print(message,payload)


def on_spawned(spawn):
    print("On_spawned: ", spawn)
    pending.append(spawn)
    event.set()


def spawn_added(spawn):
    print("Spawn_added: ", spawn)
    event.set()
    if(spawn.identifier.startswith(package_name_apk)):
        print("Attach to new VirtualApp process")
        session=device.attach(spawn.pid)
        script=session.create_script(open(pattern).read())
        script.on('message', on_message)
        script.load()
        device.resume(spawn.pid)


def spawn_removed(spawn):
    print("Spawn removed", spawn)
    event.set()


def on_message(spawn, message, data):
    print('on_message:', spawn, message, data)
   

def on_message(message, data):
    if message['type'] == 'send':
        print("[+] Method Found [+]")               
        with open(log,"a") as f:
            f.write("[+] findAndBackupAndHook method [+]\n")
            f.write(message['payload'])
            f.write("\n=============================\n")
        #print("[*] {0}".format(message['payload']))
    else:
        print(message)



def run():
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        emulatores = client.devices()
        for emulatore in emulatores:
            print(f"[+] Devices FOUND! {emulatore} [+]\n")
            pending=[]
            sessions=[]
            scripts=[]
            event=threading.Event()
            device.on('spawn-added', spawn_added)
            device.on('spawn-removed', spawn_removed)
            device.on('child-added', on_spawned)
            device.on('child-removed', on_spawned)
            device.on('process-crashed', on_spawned)
            device.on('output', on_spawned)
            device.on('uninjected', on_spawned)
            device.on('lost', on_spawned)
            device.enable_spawn_gating()
            print('[+] Enabled spawn gating [+]\n')
            #spawn new processes
            pid=device.spawn([package_name_apk])
            print("[+] Launching app... [+]\n")
            session=device.attach(pid)
            print(f"[+] Attached to pid: {pid} [+]\n")
            script=session.create_script(open(pattern).read())

            script.on('message', on_message)
            script.load()
            device.resume(pid)
            print("[+] App launched. Loading exploit... [+]\n")
            print("\n====================================================================================================\n")
            input()

    except frida.ServerNotRunningError:
        print("[-] Frida server is not running! Exiting... [-]\n")
    except frida.NotSupportedError:
        print("[-] Unable to find application. Please, install it first! [-]\n")
    except frida.ProcessNotFoundError:
        print("[-] Unable to find process. Launch the app and try again! [-]\n")
    except KeyboardInterrupt:
        time.sleep(1)
        print(Fore.GREEN +"\n[?] Searching for injection functions [?]\n")
        print(Fore.WHITE)
        run_extraction_injector()
        print(Fore.GREEN + "\n[?] Searching for extracted methods [?]\n")
        print(Fore.WHITE)
        time.sleep(2)
        extraction()
        time.sleep(2)
        print(Fore.GREEN + "\n[?] Starting Repackaging... [?]\n")
        print(Fore.WHITE)
        repackaging()
       


def starting():
    intro()
    time.sleep(1)
    print(Fore.WHITE + " ")
    comando = f"frida-ps -U > {lista_processi}"
    os.system(comando)
    trovato=0
    with open(lista_processi,"r") as reading:
        reading.readline()
        for read in reading:
            if package_name_apk in read:
                trovato=1
    
    if trovato ==0:
        print("[-] Package name not found [-]")
        sys.exit(0)
    else:
        print("[+] Package name Found [+]")
        Path(outcomes).mkdir(parents=True, exist_ok=True)
        run()

    time.sleep(2)
   
    