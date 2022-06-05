# Face Music Control

[<img src = ".\READMEmaterials\flags\gb.svg" width="16" height="12">&nbsp; Click here for this document in English](README.md)

Face Music Control - это программа на языке python, позволяющая управлять звучанием музыкального инструмента с помощью распознавания эмоций. Она использует виртуальный MIDI-порт для отправки MIDI CC-сообщений с амплитудой, пропорциональной вероятностям эмоций, распознаваемым свёрточной нейронной сетью по лицеой экспрессии. Чтобы управлять параметрами DAW, мы обычно перемещаем ползунки MIDI-контроллера. Подход Face Music Control аналогичен, но MIDI-контроллер виртуальный, и им управляет нейронная сеть.


## Требования для работы программы

Очевидные требования:
* Наличие камеры на компьютере
* Наличие python интерпретатора на компьютере

### Библиотеки
Чтобы установить все необходимые библиотеки, необходимо выполнить команду:

```bash
pip install -r requirements.txt
```

### Драйвер виртуального MIDI порта **(Только для Windows)**
Для Windows требуется установить драйвер для создания виртуальных MIDI портов. Возможные решения:
* [LoopBe1](https://www.nerds.de/en/download.html)
<br> После установки LoopBe1 вирутальный MIDI порт будет на Вашем компьютере пока Вы не удалите драйвер.
* [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
<br> Это программа, позволяющая манипулировать драйвером virtualMIDI (устанавливается автоматически с loopMIDI). В случае loopMIDI чтобы виртуальный MIDI порт был на компьютере необходимо, чтобы loopMIDI был запущен.

**Если вы используете linux или macOS, Face Music COntrol сам создает виртуальный MIDI порт, и сторонние драйверы не нужны**

## Запуск

Откройте main.py интерпритатором python. Программа тестировалась python 3.10.4.

<!--
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
-->
## Лицензия
Garri Proshian © [MIT](https://choosealicense.com/licenses/mit/) 2020