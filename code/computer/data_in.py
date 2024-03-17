from time import sleep
import serial

class stats_serial():
    def __init__(self, serial_port:str, baudrate:int):
        self.__serial_port = serial_port
        self.__baudrate = baudrate
        self.__serial_interface:serial.Serial

    def open(self):
        self.__serial_interface = serial.Serial(self.__serial_port, self.__baudrate, timeout=1)
        self.reset()

    def reset(self):
        self.__serial_interface.dtr = False
        self.__serial_interface.reset_input_buffer()
        self.__serial_interface.flush()
        self.__serial_interface.dtr = True
        while self.out() == None:
            sleep(0.5)

    def out(self) -> int | None:
        self.__serial_interface.reset_input_buffer()
        for _ in range(3):
            try:
                return int(str(
                    self.__serial_interface.readline()
                )[2:][:-5])
            except ValueError:
                pass
        return None
    def close(self):
        self.__serial_interface.close()

if __name__ == "__main__":
    SERIAL_PORT = "/dev/ttyUSB0" 
    BAUDRATE = 115200
    
    ser = stats_serial(SERIAL_PORT, BAUDRATE)
    ser.open()
    while True:
        print(ser.out())
