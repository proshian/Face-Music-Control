# Face Music Control

Face Music Control is a python program that allows you to control the sound of a musical instrument using facial expression emotion recognition.

[Кликните, чтобы прочитать этот документ на русском](README.ru.md)

## Requirements

An obvious requirement is having a camera on your computer

### Libraries
The command to install all the required libraries:

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

<!--
## Использование


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
-->
## License
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
