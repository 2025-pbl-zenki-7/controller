from gpiozero import DigitalOutputDevice, AngularServo
from time import sleep

from schemas import TeaType, TeaData


DROP_TIME = 0.15
POUR_TIME = 1


class ConveyorMotor:
    def __init__(self, pin1: int, pin2: int):
        self.p1: DigitalOutputDevice = DigitalOutputDevice(pin=pin1)
        self.p2: DigitalOutputDevice = DigitalOutputDevice(pin=pin2)

    def __del__(self):
        self.p1.close()
        self.p2.close()

    def drop(self):
        self.p1.on()
        self.p2.off()
        sleep(DROP_TIME)


class LiftServo:
    def __init__(self, pin: int):
        self.servo: AngularServo = AngularServo(pin, min_angle=10, max_angle=170)

    def __del__(self):
        self.servo.close()

    def down(self):
        self.servo.angle = 10

    def up(self):
        self.servo.angle = 170


class Kettle:
    def __init__(self, pin: int):
        self.relay: DigitalOutputDevice = DigitalOutputDevice(pin=pin)
        self.relay.off()

    def __del__(self):
        self.relay.close()

    def pour(self):
        self.relay.on()
        sleep(POUR_TIME)
        self.relay.off()


class TeaServer:
    def __init__(self):
        self.__conveyor_motors = [
            ConveyorMotor(pin1=17, pin2=27),  # Tea1
            ConveyorMotor(pin1=22, pin2=23),  # Tea2
            ConveyorMotor(pin1=24, pin2=25),  # Tea3
        ]
        self.__lift_servo = LiftServo(pin=18)  # Lift servo
        self.__kettle = Kettle(pin=4)  # Kettle relay

    def __del__(self):
        for motor in self.__conveyor_motors:
            del motor
        del self.__lift_servo
        del self.__kettle

    def serve_tea(self, tea_data: TeaData):
        tea_type: int
        match tea_data.type:
            case TeaType.TEA1:
                tea_type = 0
            case TeaType.TEA2:
                tea_type = 1
            case TeaType.TEA3:
                tea_type = 2

        # NOTE: Haven't implemented yet
        # extraction_time = tea_data.extraction_time
        extraction_time = 20

        self.__conveyor_motors[tea_type].drop()
        self.__lift_servo.down()
        self.__kettle.pour()
        sleep(extraction_time)
        self.__lift_servo.up()
