import serial
import time
import traceback


class USBSerial:
    def __init__(self, path):

        # シリアル通信設定　ボーレートはArudinoと合わせる
        try:
            self.serialport = serial.Serial(
                port=path,
                baudrate=19200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.5,
            )
        except serial.SerialException:
            print(traceback.format_exc())

        # 受信バッファ、送信バッファクリア
        self.serialport.reset_input_buffer()
        self.serialport.reset_output_buffer()
        time.sleep(1)

    # データ送信関数
    def send_serial(self, cmd):

        print("send data : {0}".format(cmd))
        try:
            # rstrip()で明示的に改行コードを削除
            cmd.rstrip()
            # 改行コードを付与　バイナリに変換して送信
            self.serialport.write((cmd + "\n").encode("utf-8"))
        except serial.SerialException:
            print(traceback.format_exc())

    # データ受信関数
    def receive_serial(self):

        try:
            rcvdata = self.serialport.readline()
        except serial.SerialException:
            print(traceback.format_exc())

        # 受信データを文字列に変換　改行コードを削除
        return rcvdata.decode("utf-8").rstrip()


if __name__ == "__main__":
    path = '/dev/ttyACM0'

    uno = USBSerial(path)
    while True:
        uno.send_serial("relay:on")
        time(2)
        uno.send_serial("relay:off")
        time(2)