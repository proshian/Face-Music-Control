# Face Music Control

[<img src = ".\READMEmaterials\flags\ru.svg" width="16" height="12">&nbsp; Кликните, чтобы прочитать этот документ на русском](README.ru.md)

Русская версия README пока отстает от английской.

Face Music Control is a python program that allows you to control the sound of a musical instrument using facial expression emotion recognition.

It uses a virtual MIDI port to send MIDI CC Messages of amplitudes proportional to the probabilities of emotions recognised by a concolutional neural network. The MIDI messages may be recieved by a DAW you use to control parameters in it.

To sum up, usually parameters in a DAW are controlled by a real MIDI controller which is controlled by a human. In this project the approach is similar, but the MIDI controller is virtual and it controlled by a neural network. 

## Requirements

An obvious requirements are
* having a camera on your computer
* python interpretor installed

### Libraries
Install all the required libraries with this command:

```bash
pip install -r requirements.txt
```

### Virtual MIDI port driver **(Windows only)**
Windows requires a driver to be installed to create virtual MIDI ports. Possible solutions:
* [LoopBe1](https://www.nerds.de/en/download.html)
<br> Once LoopBe1 is installed a virtual MIDI port will be on your computer until the driver is uninstalled.
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
<br> It is a program that allows manipulating virtualMIDI driver that comes with loopMIDI. If you chose loopMIDI over LoopBe1 for a virtual MIDI port to be on your computer the loopMIDI must be running


**If you use linux or macOS, Face Music Control creates virtual MIDI ports by itself and third-party drivers are not needed**

## Launching

Run main.py. THe program was tested with python 3.10.4

## Settings mode

## Play mode
<!--
## Использование


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
-->
## License
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
