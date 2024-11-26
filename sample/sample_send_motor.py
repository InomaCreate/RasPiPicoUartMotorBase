import curses
import json
import serial

class SendMotor:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)  # Initialize UART
        self.r_speed = 80
        self.l_speed = 80
    
    def key_detect(self, stdscr):
        # Cursesのセットアップ
        stdscr.nodelay(True)  # 非ブロッキングモードを設定
        stdscr.clear()
        stdscr.addstr(0, 0, "キーを押してください（'q'で終了）")
        stdscr.addstr(1, 0, "i:前進, k:後進")
        stdscr.addstr(2, 0, "e:モーター停止")
        stdscr.addstr(3, 0, "a:speed up left, b:speed up right")
        stdscr.addstr(4, 0, "z:speed down left, x:speed down right")

        while True:
            key = stdscr.getch()  # キー入力を取得
            if key != -1:  # キーが押されている場合
                if key == ord('q'):  # 'q'キーの場合
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, "終了します")
                    stdscr.refresh()
                    self.ser.close()
                    break

                elif key == ord('i'):
                    json_string = "start$" + json.dumps({"v_r": self.r_speed, "v_l": self.l_speed})
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"motor send!!: {json_string}")
                    self.ser.write(json_string.encode('utf-8'))
                    self.ser.write(b'\r\n')

                elif key == ord('k'):
                    json_string = "start$" + json.dumps({"v_r": -1*self.r_speed, "v_l": -1*self.l_speed})
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"motor send!!: {json_string}")
                    self.ser.write(json_string.encode('utf-8'))
                    self.ser.write(b'\r\n')

                elif key == ord('s'):
                    self.r_speed = self.r_speed + 5
                    if self.r_speed > 100:
                        self.r_speed = 100
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"right motor speed set: {self.r_speed}")

                elif key == ord('x'):
                    self.r_speed = self.r_speed - 5
                    if self.r_speed < 0:
                        self.r_speed = 0
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"right motor speed set: {self.r_speed}")

                elif key == ord('a'):
                    self.l_speed = self.l_speed + 5
                    if self.l_speed > 100:
                        self.l_speed = 100
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"left motor speed set: {self.l_speed}")

                elif key == ord('z'):
                    self.l_speed = self.l_speed - 5
                    if self.l_speed < 0:
                        self.l_speed = 0
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"left motor speed set: {self.l_speed}")

                elif key == ord('e'):
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"emergency stop")
                    self.ser.write(b'emergency_stop\r\n')


                else:
                    self.clear_line(stdscr, 5)  # 5行目をクリア
                    stdscr.addstr(5, 0, f"キーコード: {key}")

                stdscr.refresh()

    def clear_line(self, stdscr, row):
        max_y, max_x = stdscr.getmaxyx()
        stdscr.addstr(row, 0, " " * (max_x - 1))  # 空白文字で上書き
        stdscr.refresh()

def main(stdscr):
    # Cursesのセットアップ
    motor = SendMotor()
    motor.key_detect(stdscr)  # stdscrを渡してkey_detectを実行


if __name__ == '__main__':
    # Cursesのラッパーを使用して実行
    curses.wrapper(main)
