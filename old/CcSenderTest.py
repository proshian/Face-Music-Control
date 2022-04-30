import mido

from CcSender import CcSender

port = mido.open_output(mido.get_output_names()[-1])

cc_sender = CcSender(5, port)
all_data = [
    {"data": [0.2, 0.8, 0.9], "min": 0, "max": 1, "bias": 0},
    {"data": [0.1, 0.4], "min": 0, "max": 1, "bias": 3}]

cc_sender.send(all_data)
"""
Тест корректен.
В этом тесте ожидаются сообщения:
control_change channel=3 control=0 value=25 time=0
control_change channel=3 control=1 value=102 time=0
control_change channel=3 control=2 value=114 time=0
control_change channel=3 control=3 value=13 time=0
control_change channel=3 control=4 value=51 time=0
"""