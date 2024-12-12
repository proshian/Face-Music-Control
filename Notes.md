# TODO
* [] Окно про выбор MIDI порта перед созданием cc_sender'а, которое возникает, если нет доступных MIDI портов. Раз в n миллисекунд происходит проверка на наличие порта. Когда  порт появляется, данное окно закрывается и открывается FmcUi.

# Notes
There used to be an `all_resources` property in the Resource class. 
It used to be populated in `__init__` via `Resource.all_resources.append(self)`.

`Sensor` also had an `all_sensors` property that was populated in `__init__` similarly.

There used to be a `rand_sens.py` that outputed a random number. It was used for testing.


В конце файла fer_sens.py есть альтернативнаое создание списка эмоций и модели (соответствует тому, что исопльзовалось на КМУ).