import serial
import time


class ArduinoController:
    def __init__(self,port = 'dev/ttyACM0',baud_rate = 9600, timeout = 1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
    
    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2) #arduinoの起動時間
            print(f"[{self.port}] シリアル通信できました")

            # Arduinoからの初期メッセージを受信（例: "Arduino Ready!"）
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                print(f"[{self.port}] Arduino says: {response}")
            return True
        except serial.SerialException as e:
            print(f"[{self.port}] 接続エラー: {e}")
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
            self.ser.write(command)
            print(f"[{self.port}] Sent: {command}")
            time.sleep(1) # Arduinoからの返信を待つ

            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                return response
            return None # 返信がない場合
        except Exception as e:
            print(f"[{self.port}] Error sending command or receiving response: {e}")
            return None

if __name__ == "__main__":
    arduino_port = '/dev/ttyACM0'

    arduino = ArduinoController(port=arduino_port)

    if arduino.connect():
        try:
            print("\n--- Testing relay control ---")
            # RELAY ON
            response = arduino.send_command('relay:on')
            if response:
                print(f"Arduino response: {response}")
            time.sleep(5) # 1秒待機

            # RELAY OFF
            response = arduino.send_command('relay:off')
            if response:
                print(f"Arduino response: {response}")
            time.sleep(5) # 1秒待機

            # 不明なコマンドを送信
            response = arduino.send_command('X')
            if response:
                print(f"Arduino response: {response}")

        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
        finally:
            arduino.disconnect()
    else:
        print("Failed to connect to Arduino. Exiting test.")