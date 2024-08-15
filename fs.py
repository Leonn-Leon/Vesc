from serial.tools import list_ports

def get_serials():
    return [i.split()[0] for i in list_ports.comports()]