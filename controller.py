from PyQt5.QtGui import QImage, QPixmap

def np_RGB_to_QPixmap(np_RGB):
    height, width, _ = np_RGB.shape
    bytesPerLine = 3 * width
    qImg = QImage(np_RGB.data, width, height, bytesPerLine, QImage.Format_RGB888)
    qpixmap = QPixmap(qImg)
    return qpixmap


class Controller():
    def __init__(
            self, camera, cc_sender, sensors,
            reources, image_label = None):
        self.camera = camera
        self.cc_sender = cc_sender
        self.image_label = image_label
        self.sensors = sensors
        self.reources = reources
    
    def set_image_label(self, image_label):
        self.image_label = image_label

    def loop(self):
        for resource in self.reources:
            resource.update_cur_data()
        cvImg = self.camera.get_cur_data()
        self.image_label.setPixmap(np_RGB_to_QPixmap(cvImg))