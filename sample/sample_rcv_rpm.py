import serial
import json


class RcvRpm:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)  # Initialize UART
        self.rpm = [0, 0]

    def serial_receive(self):
        while True:
            byte_data = self.ser.readline()
            # print(f"Received raw data: {byte_data}")  # デバッグ用の表示
            if byte_data == b'':
                continue

            try:
                str_data = byte_data.decode('utf-8').strip()  # 空白を削除
                # print(f"Decoded data: {str_data}")  # デバッグ用の表示
                json_data = json.loads(byte_data.decode('utf-8'))
                self.rpm[0] = float(json_data["rpm_l"])
                self.rpm[1] = float(json_data["rpm_r"])

                print(f"left rpm = {self.rpm[0]} right rpm = {self.rpm[1]}")  # デバッグ用の表示

            except (json.JSONDecodeError, KeyError) as e:  
                print(f"Invalid data received: {e}")  # デバッグ用の表示       
    
def main(args=None):
    rcv_rpm = RcvRpm()
    rcv_rpm.serial_receive()

if __name__ == '__main__':
    main()
    