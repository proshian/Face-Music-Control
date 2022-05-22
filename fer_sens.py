import os

from tensorflow.keras.models import model_from_json 

from sensor import Sensor

"""
class FerSensor(Sensor):
    def preprocess
    
    def load_nn(dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        # загрузим модель
        model = model_from_json(open(os.path.join(dir_, model_name), "r").read())
        # загрузим веса
        model.load_weights(os.path.join(dir_, weights_name))
        return model
"""

def load_nn(dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
    # загрузим модель
    model = model_from_json(open(os.path.join(dir_, model_name), "r").read())
    # загрузим веса
    model.load_weights(os.path.join(dir_, weights_name))
    return model

icons_dir = 'emojis/'
emotions = ["happy", "sad", "angry", "neutral", "surprised"]
emotions_icons = [os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]

fer_sens = Sensor( 
    emotions, emotions_icons,
    load_nn('models/KMUnet/KmuNet_drop_0.5/').predict, 0, 1)