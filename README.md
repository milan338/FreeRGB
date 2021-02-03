FreeRGB is a highly customisable user interface to control any type of LED lighting, built using Python and PyQt.

## Navigation

- [Navigation](#navigation)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [First install](#first-install)
  - [Updating](#updating)
- [Usage](#usage)
  - [Running](#running)
  - [Creating addons](#creating-addons)
- [Contributing](#contributing)
- [Screenshots](#screenshots)
- [ToDo](#todo)
- [License](#license)

## Features

- **Expandable**: Through an easy to use addon system, it is possible to add a limitless range of functionality to FreeRGB, from supporting new types of devices, to creating brand new user-interfaces. Control any device through any communication interface.
- **Customisable**: Through the UI editor, FreeRGB allows creating a custom interface comprised of buttons whose actions are completely custom.
- **Scalable**: Whether you need to control 1 or 100 lighting devices, you can do that. You can also control multiple individual lighting zones per device.
- **Cross-Platform**: Being built using Python and PyQt, any device that supports these should also support FreeRGB. You can control any device through any means of communication, whether it be serial or MQTT, either out-of-the-box or through the addon system.

## Installation

### Prerequisites

- **Python** >= 3.8

### First install

First, you'll need to clone the repo.
```
git clone
```

You'll need to then install the required dependencies. It's a good idea to setup a venv for this.
```
pip install -r requirements.txt
```

### Updating

If you've already cloned the repo and wish to update, simply run
```
git pull origin master
```

## Usage

### Running

To run FreeRGB, you just need to run
```
python FreeRGB.py
```

If using a venv, remember to activate it before running.

Please see the wiki for more information about using the application.

### Creating addons

Addons can be created to:
- Support a new type of device i.e. Yeelight
- Support a new commincation interface i.e. MQTT
- Support running new effect i.e. Colour picker

Please see the wiki for more information about the types of addons that can be created,
and how to create and integrate them.

## Contributing

Before contributing, please ensure you've read the [code of conduct](CODE_OF_CONDUCT.md).

If you'd like to contribute to the project, please see the [guidelines](CONTRIBUTING.md).

## Screenshots

## ToDo

- [ ] Support for MQTT communication
- [ ] Background service allowing other applications to control lighting
- [ ] Built-in updates
- [ ] Distribution through package deployment
- [ ] CI pipelines

## License

[GNU General Public License (version 3)](LICENSE)
