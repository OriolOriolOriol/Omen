import frida
import time
import threading

#Attach to device
#device= frida.get_remote_device()
device= frida.get_usb_device()
print(f"Tipo di device: {device}")

pending=[]
sessions=[]
scripts=[]
event=threading.Event()


def my_message_handler(message,payload):
    print(message,payload)


def on_spawned(spawn):
    print("On_spawned: ", spawn)
    pending.append(spawn)
    event.set()


def spawn_added(spawn):
    print("Spawn_added: ", spawn)
    event.set()
    if(spawn.identifier.startswith('com.example.trustedcontainervirtualapp:p0')):
        print("Attach to new VirtualApp process")
        session=device.attach(spawn.pid)
        script=session.create_script(open("findAndBackupAndHook.js").read())
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
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

    


device.on('spawn-added', spawn_added)
device.on('spawn-removed', spawn_removed)
device.on('child-added', on_spawned)
device.on('child-removed', on_spawned)
device.on('process-crashed', on_spawned)
device.on('output', on_spawned)
device.on('uninjected', on_spawned)
device.on('lost', on_spawned)

device.enable_spawn_gating()
event = threading.Event()
print('Enabled spawn gating')


#spawn new processes
pid=device.spawn(["com.example.trustedcontainervirtualapp"])

#device.resume(pid)
session=device.attach(pid)
print(f"Attached to pid: {pid}")

script=session.create_script(open("findAndBackupAndHook.js").read())
script.on('message', on_message)
script.load()


device.resume(pid)
print("Resume app ok")

input()