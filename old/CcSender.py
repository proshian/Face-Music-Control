import mido

class CcSender:
    """
    Протестировать модуль отдельно => ввести в программу
    """

    def __init__(self, param_num, port = None):
        if port == None:
            port_name = mido.get_output_names()[-1]
            port = mido.open_output(port_name)
            print(f"ATTENTION! CcSender opened port \
                  with name: {port_name} as a default port")
        self.port = port
        self.param_num = param_num
    
    
    def change_port(self, port):
        """
        Закрывает порт, хранящийся в self.port
        Записывает port в self.port
        """
        self.port.close()
        self.port = port
    

    def _preprocess_el(el, min_, max_):
        return round((el-min_) / (max_-min_) * CcSender.max_midi_cc)


    def _preprocess_all_data(self, all_data):
        """
        Предполагается, что данные могут поступать от разных источников
        Каждый источник формирует словарь с тремя ключами:
            data - список необработанных данных
            min - минимальное возможное значение элементов data
            max - максимальное возможное значение элементов data
            bias - прибавляется к индексам массива,
                чтобы получить номер CC события - controller
        Данная функция получет список all_data описанных выше словарей
        Возвращает список посылаемых значений  
        """
        data = [0] * self.param_num
        
        for entry in all_data:
            for el_i, el in enumerate(entry["data"]):
                processed_el = CcSender._preprocess_el(
                    el, entry["min"], entry["max"])
                data[el_i + entry["bias"]] = processed_el
                print(el, processed_el, el_i+entry["bias"])
        return data


    def send(self, all_data, channel_ = 3):
        """
        Принимает данные в виде списка словарей с ключами:
           data - список необработанных данных
            min - минимальное возможное значение элементов data
            max - максимальное возможное значение элементов data
            bias - прибавляется к индексам массива,
                чтобы получить номер CC события - controller
        Посылает соответсвующие MIDI сообщения
        """
        data = self._preprocess_all_data(all_data)
        for index, value_ in enumerate(data):
            message = mido.Message(
                'control_change', channel = channel_, 
                control = index, value = value_)
            print(message)
            self.port.send(message)
    

    def learn(self, control_, channel_ = 3):
        """
        Дергает "ползунок" control_
        Те единожды посылает сигнал амплитудой amplitude


        Альтернативная реализация метода learn:
        Запустить цикл, "поднимающий и опускающий" ползунок,
        пока self.learning_control не изменится.
        В процессе обучения self.learning_control равен
            номеру обучаемого параметра
        """
        amplitude = 10
        message = mido.Message(
            'control_change', channel = channel_, 
            control = control_, value = amplitude)
        self.port.send(message)


    max_midi_cc = 127