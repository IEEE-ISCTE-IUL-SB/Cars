import RPi.GPIO


class Car:

    def __init__(self):
        '''
            Setups every pin and gpio setting needed for control
        '''
        self.servo_average = 7.5
        self.pwm_frequency_engine = 50
        self.pwm_frequency_servo = 50

        # Board Pins
        self.servo_pin = 33
        self.engine_pin_1 = 11
        self.engine_pin_2 = 12
        self.pwm_engine_pin = 7

        # GPIO setup
        self.io = RPi.GPIO
        self.io.setmode(self.io.BOARD)
        self.io.setup(self.servo_pin, self.io.OUT)
        self.io.setup(self.engine_pin_1, self.io.OUT)
        self.io.setup(self.engine_pin_2, self.io.OUT)
        self.io.setup(self.pwm_engine_pin, self.io.OUT)

        # PWM pin setup
        self.pwm_servo = self.io.PWM(self.servo_pin, self.pwm_frequency_servo)
        self.pwm_servo.start(self.servo_average)
        self.pwm_engine = self.io.PWM(self.pwm_engine_pin, self.pwm_frequency_engine)
        self.pwm_engine.start(0)

    def rotate(self, input):
        '''
            Rotates the steering of the car based on input. input is an int between 0 and 1
        :param input:
        :return: none
        '''
        self.pwm_servo.ChangeDutyCycle(round((self.servo_average + input + input*0.5), 2))

    def forward(self):
        '''
            Sets the h bridge to propel the car forward
        :return:none
        '''
        self.io.output(self.engine_pin_1, True)
        self.io.output(self.engine_pin_2, False)

    def reverse(self):
        '''
            Sets the h bridge to propel the car backwards
        :return:
        '''
        self.io.output(self.engine_pin_1, False)
        self.io.output(self.engine_pin_2, True)

    def stop(self):
        '''
            Sets the h bridge to stop the car
        :return:
        '''
        self.io.output(self.engine_pin_1, False)
        self.io.output(self.engine_pin_2, False)

    def speed(self, percent):
        '''
            Sets the speed of the speed of the engine based on percent. percent varies between 0 and 1
        :param percent:
        :return:
        '''
        self.pwm_engine.ChangeDutyCycle(percent * 100)

    def finish(self):
        '''
            Stops the pwm signals from the raspberry and cleans the gpio setup.
        :return:
        '''
        self.pwm_servo.stop()
        self.pwm_engine.stop()
        self.io.cleanup()