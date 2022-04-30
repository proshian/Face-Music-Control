from distutils import dir_util
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
import mido  # убрать этот импорт, когда CcSender будет написан и интегророван
import tkinter as tk #k, PhotoImage, mainloop, TOP, LEFT, Frame
from tkinter import ttk
#ImageFont и ImageDraw используются для добавления текста на изображение
from PIL import Image, ImageTk, ImageFont, ImageDraw
import time
import subprocess
import os


def open_loop_midi():
    # планируется так: если loopmidi не открыт, 
    # 1) попросить пользователя открыть
    # 2) напомнить ему, что он может указать положеие программы,
    # чтобы в будущем не было необходимости открывать руками
    loopMIDI_location = r'C:\Program Files (x86)\Tobias Erichsen\loopMIDI\loopMIDI.exe'
    subprocess.Popen(loopMIDI_location)

    # строчка ние выводит список процессов
    # то же самое, как если бы мы в командной строке написали tasklist
    # лучше использовать psutil, потому что результат будет кросплатформенным
    tasklist = [line.decode('cp866', 'ignore') for line in subprocess.Popen('tasklist', stdout=subprocess.PIPE).stdout]
    # print(*tasklist)

open_loop_midi()

port = mido.open_output(mido.get_output_names()[-1])

# список эмоций, рапознаваемых нейронной сетью.
emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

# получим словарь
emotion_dict = {emotions[i] : i for i in range(len(emotions))}

def send_CC (val, emotion):
    port.send(mido.Message('control_change', channel = 3, control = emotion_dict[emotion], value = val))

def send_all_predicted_emotions (predictions):
    for emotion, index in emotion_dict.items():
        CC_val = int(round(predictions[0][index] * 127))
        send_CC(CC_val, emotion)

# dir = 'models/facial-expression-detection-2/'
dir = 'models/unknown_initial/'
# dir = 'models/facial-expression-detection-2-72_3/'
# dir = 'models/KMUnet/KmuNet_drop_0.5/'
# dir = 'models/KMUnet/last_conv_3x3_and_avg_pool_stopped_at_60/'


# загрузим модель
model = model_from_json(open(os.path.join(dir, 'fer.json'), "r").read())
# загрузим веса
model.load_weights(os.path.join(dir, 'fer.h5'))

# для детекции лица загрузим каскад Хаара
face_haar_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

# создадим объект VideoCapture. Его аргумент - индекс используемой камеры.
cap=cv2.VideoCapture(0)


def preprocessing(images):
    return images
    """
    a = []
    for image in images:
            a.append(image.reshape(48,48,1))
    return a
    """

def predictor_and_sender():
    
    ###### захватим изображение с камеры
    
    # success = True, если удалось захватить изображение,иначе - False.
    # 2-ое возвращаемое значение - захваченное изображение в виде numpy array или None
    # Реализовано так, потому что numpy ndarray не приводится к булевым переменным        
    success,orig_img=cap.read()                        
    if not success: # если не удалось захватить изображение, пропускаем итерацию
        return
    
    # Получим версию захваченного избражения в оттенках серого (модель работает с серыми изображениями)
    gray_img= cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)


    # детекция лица с помощью каскада Хаара
    # результат функции ниже - ndarray, содержащий ndarray'и
    # с координатами найденных лиц в формате:
    # (координата x, координата y (считаются от верхнего левого угла),
    #     ширина рамки с лицом, высота) 
    faces_detected = face_haar_cascade.detectMultiScale(orig_img, 1.32, 5)

    for (x,y,w,h) in faces_detected:

        # выделим рамкой участок с лицом, который обработает модель
        cv2.rectangle(orig_img,(x,y),(x+w,y+h),(114,106,106),thickness=4)

        font_height = 20
        font_padding = 3

        # создадим контур и заливку рамки для текста
        cv2.rectangle(
            orig_img,(x,y),(x+w,y-font_height-font_padding * 2),(114,106,106),thickness=-1)
        
        cv2.rectangle(
            orig_img,(x,y),(x+w,y-font_height-font_padding * 2),(114,106,106),thickness=4)

        # Наложим поверх найденного лица полупрозрачную маску:

        # 1) Запишем часть, содержащую лицо в паеременную sub_img
        sub_img = orig_img[y:y+h, x:x+w]

        # 2) Создадим белый квадрат такого же размера, как sub_img
        white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

        # 3) Сложим лицо с белым квадратом с коффицинтами 0.9 и 0.1
        res = cv2.addWeighted(sub_img, 0.85, white_rect, 0.15, 1.0)

        # 4) Перезапишим участок с лицом на "приглушенную версию"
        orig_img[y:y+h, x:x+w] = res


        # обрежем часть изображения, содержащую лицо
        cut_gray=gray_img[y:y+w,x:x+h] 

        # изменим размер изображений на 48*48 пискселей, тк на таких обучалась модель
        cut_gray=cv2.resize(cut_gray,(48,48)) 

        # преобразуем изобр. в оттенках серого в трехмерный numpy array
        img_pixels = image.img_to_array(cut_gray)

        # Уведичим размерность.
        # Это формальность, связаная с форматом входных данных модели.
        # Те у нас батч из одного элемента
        img_pixels = np.expand_dims(img_pixels, axis = 0)        
        img_pixels /= 255

        # получим массив с вероятностями для каждой из 6-и эмоций
        predictions = model.predict(preprocessing(img_pixels))
        #print(predictions)
        """
        # Я решил прибавлять страх к злости
        predictions[0][emotion_dict['angry']] \
            += predictions[0][emotion_dict['fear']]
        """

        max_index = np.argmax(predictions[0])  # номер наиболее вероятной эмоции
        
        predicted_emotion = emotions[max_index]  # наиболее вероятная эмоция        
        

        
        # выведем в видео-поток наиболее вероятную эмоцию и ее вероятность
        """
        cv2.putText(
            orig_img,
            # f"{predicted_emotion}  {predictions[0][max_index]:.3f}",
            f"{predicted_emotion}  {int(predictions[0][max_index]*100)}%",
            (int(x), int(y - font_padding)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        """
        
        font = ImageFont.truetype("arial.ttf", font_height)
        img_pil = Image.fromarray(orig_img)
        draw = ImageDraw.Draw(img_pil)
        draw.text(
            (int(x + font_padding), int(y - font_height - font_padding)),
            f"{predicted_emotion}  {predictions[0][max_index]*100:.0f}%",
            font = font, fill = (255, 255, 255, 255))
        orig_img = np.array(img_pil)

        
        
        send_all_predicted_emotions(predictions)
        
        for i in range(len(probability_labels)):
            if(i == max_index):
                probability_labels[i].configure(foreground = "red")
            else:
                probability_labels[i].configure(foreground = "black")
            probability_labels[i].configure(text = f"{emotions[i]}:\n{predictions[0][i]:.3f}\n")
            
    
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(orig_img)
    
    return img
    
    #if cv2.waitKey(10) == ord('q'): # при нажатии 'q', выйдем из цикла, после чего выполнение программы завершится
    #    return




# creating tkinter window 
root = tk.Tk() 
root.config(background="#FFFFFF")
root.wm_title("Face Music Control")
root.maxsize(790, 500)
root.attributes("-topmost", True) # чтобы всегда было поверх других окон

emojis = []

for emotion in emotions:
    emojis.append(tk.PhotoImage(file = fr".\emojis\{emotion}.png") )
    # при необходимости к PhotoImage можно применять subsample(x,y)
    # subsample изменяет размер изображения, используя каждый x-ый пиксель по горизонтали и y-ый по вертикали


# генерация функции, посылающей единожды определенную эмоцию.
# функции, которые выполняются по клику на кнопку, 
# принимают только один параметр, который не должен использоваться
# поэтому нужна функция, которая для каждой кнопки сгенерит свою функцию
def get_mapper(emotion_to_map):
    def mapper(event):
        send_CC(1,emotion_to_map)
    return mapper


button_frame = tk.Frame(root)
button_frame.config(background="#FFFFFF")
button_frame.pack(side=tk.RIGHT, padx = 28, expand = 1,  fill=tk.Y)

emoji_frame = tk.Frame(button_frame)

buttons = []

probability_frame = tk.Frame(button_frame)
probability_frame.config(background="#FFFFFF")

probability_labels = []

for i in range (len(emotions)):
    buttons.append(ttk.Button(emoji_frame, image = emojis[i]))
    buttons[i].bind('<Button-1>', get_mapper(emotions[i]))
    buttons[i].pack(side=tk.TOP)
    
    probability_labels.append(ttk.Label(probability_frame, background="#FFFFFF") )
    probability_labels[i].pack()

probability_frame.pack()


running = True  # Global flag. 
                # Если False, прекращает итерирование predictor_and_sender

def scanning():
    if running:  # Only do this if the Stop button has not been clicked
        img = predictor_and_sender()  # произведем итерацию FMC и вернем изображение с выделенным лицом и подписанной эмоцией
        imgtk = ImageTk.PhotoImage(image = img)
        l.imgtk = imgtk
        l.configure(image=imgtk)
        
    # After 50 milliceconds, call scanning again (create a recursive loop)
    root.after(50, scanning)


stop_image = tk.PhotoImage(file = r".\emojis\stop.png")
run_image = tk.PhotoImage(file = r".\emojis\run.png")
# subsample is to resize image to fit on button

play_button = ttk.Button(button_frame, image = stop_image)

def change_state(event):
    global running
    if running == True:
        running = False
        play_button.config(image=run_image)
        probability_frame.pack_forget()
        emoji_frame.pack(side=tk.BOTTOM)
        
        instructions = tk.PhotoImage(file = r".\emojis\instructions.png")
        l.imgtk = instructions
        l.configure(image = instructions)
    else:
        running = True
        probability_frame.pack()
        play_button.config(image=stop_image)
        emoji_frame.pack_forget()

play_button.bind('<Button-1>', change_state)

play_button.pack(side=tk.BOTTOM, anchor= tk.S)


#Graphics window
imageFrame = tk.Frame(root)
imageFrame.config(background="#FFFFFF")
imageFrame.pack(side=tk.RIGHT, expand=False)

# добавим Label в окно root 
l = tk.Label(imageFrame)
l.pack() 

# вместо строчки ниже
# можно было бы написать scanning()
# но scanning имеет смысл только после начала mainloop
root.after(50, scanning)


tk.mainloop()

#cap.release()