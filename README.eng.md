# Face Music Control

[<img src = ".\READMEmaterials\flags\ru.svg" width="16" height="12">&nbsp; Кликните, чтобы прочитать этот документ на русском](README.md)

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
Windows requires a driver installation to create virtual MIDI ports. Possible solutions:
* [LoopBe1](https://www.nerds.de/en/download.html)
<br> Once LoopBe1 is installed, a virtual MIDI port will be on your computer until the driver is uninstalled.
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
<br> It is a program that allows you to manipulate virtualMIDI driver that comes with loopMIDI. If you chose loopMIDI over LoopBe1 you have to run loop MIDI to have a virtual MIDI port on your computer.

**If you use linux or macOS, Face Music Control creates a virtual MIDI port by itself, and three is no need for third-party drivers.**

## Launching

Run main.py. The program was tested with python 3.10.4

## Setting mode
To bind a sound parameter and an emotion, you need to:
* Open the setting mode in Face Music Control and MIDI mapping mode in a DAW
* Successively press the DAW graphic interface element responsible for the sound parameter and the button with a graphic representation of the emotion, which should control the sound parameter.
When all the required sound parameters are mapped to a corresponding emotion, you should exit MIDI mapping mode, and then exit Face Music Control setting mode. 

## Play mode (demo) 
The sound is controlled in play mode.

In the video demonstration below, happiness controls the echo, and anger controls the distortion.

https://user-images.githubusercontent.com/98213116/172071460-583846ca-99f1-4817-84aa-8ef4403bfec4.mp4

*Sound on the video in the README is off by default, but **it can be turned on.***

*All demos are in the project directory: [READMEmaterials/demonstrations](READMEmaterials/demonstrations). If the video does not display, you can find it there ([happiness-echo_anger-distortion.mp4](READMEmaterials/demonstrations/happiness-echo_anger-distortion.mp4)).

<!--
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
-->
## Face Music Control achievements
Competitions:
* Undergraduate Paper Contest of the 11th Congress of Young Scientists - win in 6 categories:
(Big Data and Machine Learning, Data Analytics, Artificial Intelligence in Industry, Speech Technologies and Machine Learning, Financial Big Data, Deep Learning and Generative Artificial Intelligence)
* NeuroTech Cup - 3rd place

Conferences:
* 11th Congress of Young Scientists
* Samara Neuroweek 2020

A publication in the Proceedings of the 11th Congress of Young Scientists (will be published by the end of 2022)

## License
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
