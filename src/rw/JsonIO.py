import json

from os import path


class JsonIO():
    def __init__(self, filename):
        self.base_path = path.dirname(__file__)
        # self.json_path = path.abspath(
        #     path.join(self.base_path, 'preferences.json'))
        self.json_path = path.abspath(
            path.join(self.base_path, filename))

        with open(self.json_path, 'r') as file:
            self.data = json.load(file)

        # self.writeEntry('thing')
        # self.writeEntry(entry)

    def readEntry(self, entry):
        try:
            # print(self.data[entry])
            return self.data[entry]
        except:
            return None
        print(self.data['AdvancedMode'])

    def writeEntry(self, menu, layout, entry, entry_name, command):
        self.new_json = {
            'text': entry_name,
            'command': command}
        self.data[menu][layout][entry] = self.new_json

        try:
            with open(self.json_path, 'w') as file:
                file.write(json.dumps(self.data, indent=4, sort_keys=True))
            return 1
        except:
            return 0


if __name__ == '__main__':
    # JsonIO()
    main = JsonIO('menus.json').readEntry('main_menu')
    print(main)
    for key, other in main.items():
        print(key)
        print(other)
        JsonIO('menus.json').readEntry(key)
        for element, attributes in other.items():
            print(attributes)
        # for thing, contents in key:
        #     print(thing)
