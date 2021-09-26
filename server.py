from ppadb.client import Client as AdbClient
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
for device in devices:
    device.shell("./data/local/tmp/frida-server")