import os
import datetime
import serial 
import pynmea2

class UbloxGPS:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_interface = None
        self.log_file = None

    def open_serial(self):
        try:
            self.serial_interface = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Opened serial port {self.port} at {self.baudrate} baudrate.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            if self.serial_interface and self.serial_interface.is_open:
                self.serial_interface.close()

    def close_serial(self):
        if self.serial_interface and self.serial_interface.is_open:
            self.serial_interface.close()
            print(f"Closed serial port {self.port}.")
        if self.log_file:
            self.log_file.close()
            print("Closed log file.")

    def create_log_file(self):
        log_folder = "ublox-gps-log"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(log_folder, f"{date_string}.nmea")
        self.log_file = open(filename, "a")

    def write_to_log_file(self, data):
        if self.log_file:
            self.log_file.write(data + "\n")

    def parse_nmea_sentence(self, nmea_sentence):
        try:
            if nmea_sentence.startswith('$GNGGA'):
                msg = pynmea2.parse(nmea_sentence)
                latitude = msg.latitude
                longitude = msg.longitude
            else:
                latitude, longitude = None, None
        except pynmea2.ParseError as e:
            print(f"NMEA Parse error: {e}")
            latitude, longitude = None, None
        return latitude, longitude

    def main(self):
        try:
            self.open_serial()
            self.create_log_file()
            while True:
                try:
                    line = self.serial_interface.readline().decode('ascii', errors='replace')
                    if line.startswith('$GNGGA'):
                        latitude, longitude = self.parse_nmea_sentence(line)
                        print(f"Latitude: {latitude}, Longitude: {longitude}")
                        if latitude is not None and longitude is not None:
                            self.write_to_log_file(line.strip())
                except serial.SerialException as e:
                    print(f"Serial Error: {e}")
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            self.close_serial()
            print("Keyboard interrupt detected, Exiting ...")

if __name__ == "__main__":
    gps_module = UbloxGPS('/dev/ttyACM0', baudrate=115200)
    gps_module.main()
