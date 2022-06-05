# Face Music Control

[<img src = ".\READMEmaterials\flags\ru.svg" width="16" height="12">&nbsp; Кликните, чтобы прочитать этот документ на русском](README.ru.md)

Face Music Control is a python program for controlling the sound of a musical instrument via emotion recognition. It uses a virtual MIDI port to send MIDI CC Messages of amplitudes proportional to the probabilities of emotions recognised by a convolutional neural network based on facial expression. To control DAW parameters, we usually move sliders of a MIDI controller. Face Music Control's approach is similar, except the MIDI controller is virtual, operated by a neural network.

## Requirements
Obvious requirements are
* A camera on your computer
* A python interpretor

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


**If you use linux or macOS, Face Music Control creates a virtual MIDI port by itself and third-party drivers are not needed**

## Launching

Run main.py. The program was tested with python 3.10.4

## Settings mode


## Play mode
<!--
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
-->
## License
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
