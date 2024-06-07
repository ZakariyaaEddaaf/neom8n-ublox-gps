import os
import datetime
import serial
import pynmea2
import time

class BaseLogger:
    def __init__(self, gps_port, baudrate=115200, timeout=1):
        self.gps_port = gps_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.gps_serial_interface = None
        self.log_file = None

    def open_serial(self, port):
        try:
            serial_interface = serial.Serial(port, self.baudrate, timeout=self.timeout)
            self.print_log(f"Opened serial port {port} at {self.baudrate} baudrate.")
            return serial_interface
        except serial.SerialException as e:
            self.print_log(f"Error opening serial port {port}: {e}")
            return None

    def close_serial(self, serial_interface):
        if serial_interface and serial_interface.is_open:
            serial_interface.close()
            self.print_log(f"Closed serial port {serial_interface.port}.")

    def create_log_file(self):
        log_folder = "ublox-gps-log"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
            self.print_log(f"Created folder {log_folder}.")
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(log_folder, f"{date_string}.nmea")
        self.log_file = open(filename, "a")
        self.print_log(f"Log file created at {filename}")

    def write_to_log_file(self, data):
        if self.log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_file.write(f"{timestamp} - {data}\n")

    def print_log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {message}")

    def parse_nmea_sentence(self, nmea_sentence):
        try:
            if nmea_sentence.startswith('$GNGGA'):
                msg = pynmea2.parse(nmea_sentence)
                latitude = msg.latitude
                longitude = msg.longitude
            else:
                latitude, longitude = None, None
        except pynmea2.ParseError as e:
            self.print_log(f"NMEA Parse error: {e}")
            latitude, longitude = None, None
        return latitude, longitude

    def main(self):
        try:
            self.gps_serial_interface = self.open_serial(self.gps_port)

            if not self.gps_serial_interface:
                self.print_log("Error: GPS serial port could not be opened. Exiting...")
                return

            self.create_log_file()

            while True:
                try:
                    if self.gps_serial_interface and self.gps_serial_interface.is_open:
                        line = self.gps_serial_interface.readline().decode('ascii', errors='ignore')
                        if line:
                            self.print_log(f"RX: {line.strip()}")
                            self.write_to_log_file(line.strip())
                        else:
                            no_data_msg = "RX: No GPS data coming in. No data received."
                            self.print_log(no_data_msg)
                            self.write_to_log_file(no_data_msg)
                            time.sleep(1)
                except serial.SerialException as e:
                    self.print_log(f"Serial Error: {e}")
                except Exception as e:
                    self.print_log(f"Error: {e}")
        except KeyboardInterrupt:
            self.print_log("Keyboard interrupt detected, Exiting ...")
        finally:
            self.close_serial(self.gps_serial_interface)
            if self.log_file:
                self.log_file.close()
                self.print_log("Closed log file.")

if __name__ == "__main__":
    gps_module = BaseLogger('/dev/ttyUSB0', baudrate=115200)
    gps_module.main()
