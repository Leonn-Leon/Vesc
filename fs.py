from serial.tools import list_ports

def get_serials():
    return [port.device for port in list_ports.comports()]