import mido
import rtmidi

from sensor import Sensor


class CcSender:
    """
    Протестировать модуль отдельно => ввести в программу
    """

    def __init__(self, sensors: list[Sensor]) -> None:
        port = rtmidi.MidiOut()
        port_name = "Face Music Control"
        try:
            port.open_virtual_port(port_name)
            print("ATTENTION! CcSender created a virtual port"
                  f"with name: {port_name} as a default port")
        except NotImplementedError:
            port_name = mido.get_output_names()[-1]
            port = mido.open_output(port_name)
            # port: mido.backends.rtmidi.Output
            print("ATTENTION! CcSender opened port"
                  f"with name: {port_name} as a default port")
        self.port = port

        self.biases = dict()
        self._set_biases(sensors)

        self.min_max = {sensor.id :
            {'min': sensor.min_possible,
             'max': sensor.max_possible} for sensor in sensors}
                
    
    def _set_biases(self, sensors: list[Sensor]) -> None:
        next_bias = 0
        for sensor in sensors:
            self.biases[sensor.id] = next_bias
            next_bias += len(sensor.names)
    
    def change_port(self, port):
        """
        Закрывает порт, хранящийся в self.port
        Записывает port в self.port
        """
        self.port.close()
        self.port = port
    

    def _preprocess_el(el, min_, max_):
        return round((el-min_) / (max_-min_) * CcSender.max_midi_cc)


    def _preprocess_sensor_data(self, sensor_id, data):
        min_max = self.min_max[sensor_id]
        prep_data = [
            CcSender._preprocess_el(d, min_max['min'], min_max['max'])
            for d in data]
        
        return prep_data


    def send(self, sensor_id, data, channel_ = 3):
        p_data = self._preprocess_sensor_data(sensor_id, data)
        for index, value_ in enumerate(p_data, self.biases[sensor_id]):
            message = mido.Message(
                'control_change', channel = channel_, 
                control = index, value = value_)
            # print(message)
            self.port.send(message)
    

    def learn(self, sensor_id, index, channel_ = 3, amplitude = 10):
        """
        Дергает "ползунок" control_ = index + bias
        Те единожды посылает сигнал амплитудой amplitude


        Альтернативная реализация метода learn:
        Завести поле learning_control
        Запустить цикл, "поднимающий и опускающий" ползунок,
        пока self.learning_control не изменится.
        В процессе обучения self.learning_control равен
            номеру обучаемого параметра
        """
        bias = self.biases[sensor_id]
        control_ = index + bias
        message = mido.Message(
            'control_change', channel = channel_, 
            control = control_, value = amplitude)
        self.port.send(message)


    max_midi_cc = 127