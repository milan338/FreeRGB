class SomeOtherEffect():
    def __init__(self):
        self.sendSerial()

    def sendSerial(self):
        print('serial direct')

    @staticmethod
    def effectData():
        effect_name = 'Some other effect'
        return effect_name
