# import serial.tools.list_ports as stl
# from ampy.pyboard import Pyboard
# from ampy.files import Files
#
#
# def __get_upload_port():
#    com_ports = stl.comports()
#    devices = [port.device for port in com_ports]
#    devices.sort()
#    return devices[-1]
#
#
# def upload_file(local_path: str, remote_path: str) -> None:
#    esp_port = __get_upload_port()
#    print(f"Found esp device at port {esp_port}")
#    pyb = Pyboard(esp_port, rawdelay=1)
#    f = Files(pyb)
#    print(f.ls())
#    with open(local_path, 'rb') as local_file:
#        f.put(remote_path, local_file.read())
