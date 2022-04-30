all_data = [
    {"data": [0.2, 0.8, 0.9], "min": 0, "max": 1},
    {"data": [0.1, 0.4], "min": 0, "max": 1}]

max_midi_CC = 127
data = []

for entry in all_data:
    #entry_data = [round((el - entry["min"])/entry["max"] * max_midi_CC) for el in entry["data"]]
    #data = [*data, *entry_data]
    for el in entry["data"]:
        processed_el = round((el-entry["min"]) /
                                entry["max"] * max_midi_CC)
        data.append(processed_el)

print(data)