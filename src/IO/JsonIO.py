import json

from os import path


class JsonIO():
    def __init__(self, filename, *args, **kwargs):
        self.base_path = path.dirname(__file__)
        # self.json_path = path.abspath(
        #     path.join(self.base_path, 'preferences.json'))
        self.json_path = path.abspath(
            path.join(self.base_path, filename))

        with open(self.json_path, 'r') as file:
            self.data = json.load(file)

        self.writeEntry('thing')

    def readEntry(self, entry):
        try:
            return self.data[entry]
        except:
            return None
        print(self.data['AdvancedMode'])

    def writeEntry(self, entry):
        # modify file here
        try:
            with open(self.json_path, 'w') as file:
                file.write(json.dumps(self.data, indent=4, sort_keys=True))
            return 1
        except:
            return 0


if __name__ == '__main__':
    JsonIO()
