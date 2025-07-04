import arduino_serial
import time


class ArduinoController:
    def __init__(self,port = 'dev/ttyACM0',baud_rate = 9600, timeout = 1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
    
    def connect(self):
        try:
            self.ser = arduino_serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2) # Arduinoの起動を待つ
            print(f"[{self.port}] Serial connection established successfully.")

            # Arduinoからの初期メッセージを受信（例: "Arduino Ready!"）
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                print(f"[{self.port}] Arduino says: {response}")
            return True
        except arduino_serial.SerialException as e:
            print(f"[{self.port}] Error connecting to Arduino: {e}")
            print("Please check:")
            print(f"  - Is Arduino connected to {self.port}?")
            print(f"  - Is the baud rate ({self.baud_rate}) correct?")
            print("  - Do you have permissions to access the serial port? (e.g., sudo usermod -a -G dialout $USER and reboot)")
            self.ser = None
            return False
        
    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"[{self.port}] Serial connection closed.")
        self.ser = None

    def send_command(self, command):
        if not self.ser or not self.ser.is_open:
            print(f"[{self.port}] Not connected to Arduino. Please call connect() first.")
            return None

        try:
            self.ser.write(command.encode('utf-8'))
            print(f"[{self.port}] Sent: {command}")
            time.sleep(0.1) # Arduinoからの返信を待つ

            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                return response
            return None # 返信がない場合
        except Exception as e:
            print(f"[{self.port}] Error sending command or receiving response: {e}")
            return None

# このファイルが直接実行された場合のテストコード
if __name__ == "__main__":
    # ここは、実際にArduinoが接続されているポートに置き換えてください
    # 例: '/dev/ttyACM0' または '/dev/ttyUSB0'
    arduino_port = '/dev/ttyACM0'

    controller = ArduinoController(port=arduino_port)

    if controller.connect():
        try:
            print("\n--- Testing LED control ---")
            # LED ON
            response = controller.send_command('1')
            if response:
                print(f"Arduino response: {response}")
            time.sleep(1) # 1秒待機

            # LED OFF
            response = controller.send_command('0')
            if response:
                print(f"Arduino response: {response}")
            time.sleep(1) # 1秒待機

            # 不明なコマンドを送信
            response = controller.send_command('X')
            if response:
                print(f"Arduino response: {response}")

        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            controller.disconnect()
    else:
        print("Failed to connect to Arduino. Exiting test.")
