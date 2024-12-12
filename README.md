# Face Music Control

[<img src = ".\READMEmaterials\flags\ru.svg">&nbsp; Кликните, чтобы прочитать этот документ на русском](README.ru.md)

Face Music Control is a Python application for controlling the sound of a musical instrument via emotion recognition. It uses a virtual MIDI port to send MIDI CC Messages of amplitudes proportional to the probabilities of emotions recognised by a convolutional neural network based on facial expression. To control DAW parameters, we usually move sliders of a MIDI controller. Face Music Control's approach is similar, except the MIDI controller is virtual, operated by a neural network.


> [!Note]
> This program functions as intended. However, it is an older project, and while I recently (December 2024) performed an update to ensure it still works, I am not fully satisfied with the code quality. It does not reflect my current coding standards or practices. I am sharing this project to showcase its functionality, but please keep in mind that it is a legacy project.



## Motivation
When improvising or composing music, conventional interfaces for controlling sound (pedals, sliders, etc.) are inconvenient and rarely applicable. During the process of music creation, musicians often lack the focus needed to search for the right tone and adjust the sound parameters of their instrument. However, in these contexts, it is particularly important for the character of the sound to align with the musician's emotional state. I could not find any existing solutions for controlling an instrument's sound based on the musician's emotions. Therefore, I created this program.


## Additional applications
* A new kind of interaction with an instrument can be a self-contained performance
* Since the lighting equipment is controlled by MIDI events, Face Music Control can be used to complement the visuals of concerts

## Requirements

### Hardware and Software
- A camera on your computer
- Python 3.11.5 (other versions may work but are untested)
- A DAW (Digital Audio Workstation)
- Tested OS: Windows (Linux and macOS are expected to work, but were not tested)
- A virtual MIDI port driver (**Windows-only**; see below)

### Dependencies
Install required libraries with:
```bash
pip install -r requirements.txt
```

### Virtual MIDI port driver **(Windows only)**
Windows users must install a virtual MIDI port driver to enable communication with the DAW (Windows doesn't have a built-in driver for virtual MIDI ports). Possible solutions:
* [LoopBe1](https://www.nerds.de/en/download.html)
<br> Once LoopBe1 is installed, a virtual MIDI port will be on your computer until the driver is uninstalled.
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
<br> It is a program that allows you to manipulate virtualMIDI driver that comes with loopMIDI. If you chose loopMIDI over LoopBe1 you have to run loop MIDI to have a virtual MIDI port on your computer.

**If you use Linux or MacOS, Face Music Control creates a virtual MIDI port by itself, and there is no need for third-party drivers.**

## Launching

run `main.py` from the root of this project:
```bash
python main.py
```

## Usage
### Setting mode
To bind a sound parameter and an emotion:
* Open the setting mode in Face Music Control and MIDI mapping mode in a DAW
* Successively press the DAW graphic interface element responsible for the sound parameter and the button with a graphic representation of the emotion, which should control the sound parameter.
When all the required sound parameters are mapped to a corresponding emotion, you should exit MIDI mapping mode, and then exit Face Music Control setting mode. 

### Play mode
The sound is controlled in play mode.

In the video demonstration below, happiness controls the echo, and anger controls the distortion.

https://user-images.githubusercontent.com/98213116/172071460-583846ca-99f1-4817-84aa-8ef4403bfec4.mp4

> [!Note]
> The sound in the video in the README is off by default, but **it can be turned on.**

> [!Note]
> The demonastration showcases the functionality, but is outdated: the program now uses a better model for emotion recognition (such exaggeration of facial expressions is no longer needed) and the UI has become cleaner.


*All demonstrations are in the project directory: [READMEmaterials/demonstrations](READMEmaterials/demonstrations). If the video does not display, you can find it there ([happiness-echo_anger-distortion.mp4](READMEmaterials/demonstrations/happiness-echo_anger-distortion.mp4)).


## Face Music Control achievements
Competitions:
* Undergraduate Paper Contest of the 11th Congress of Young Scientists - win in 6 categories:
(Big Data and Machine Learning, Data Analytics, Artificial Intelligence in Industry, Speech Technologies and Machine Learning, Financial Big Data, Deep Learning and Generative Artificial Intelligence)
* NeuroTech Cup - 3rd place

Conferences:
* 11th Congress of Young Scientists
* Samara Neuroweek 2020

Publications:
* A publication in the Proceedings of the 11th Congress of Young Scientists

## License
Harry Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020
