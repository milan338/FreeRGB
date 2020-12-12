class SerialDirect():
    def __init__(self):
        self.sendSerial()

    def sendSerial(self):
        print('serial direct')

    @staticmethod
    def effectData():
        effect_name = 'Serial Direct'
        return effect_name
