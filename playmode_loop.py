"""
    Данный раздел на данный момент описан псевдокодом
"""

def playmode_loop_iteration(sensors, ui):
    #camera.make_snapshot()
    for res in resourses:
        res.update_data()
    camera_image_modifications = []
    for sensor in sensors:
        data = sensor.acquire_data()
        preprocessed_data = sensor.preprocess_data(data)
        results = sensor.get_results(preprocessed_data)
        cc_sender.send_results(sensor.id, results)
        ui.change_labels(sensor.id, results)
        if # если сенсор является camera_sensor: 
            camera_image_modifications.append(sensor.image_modifications)
    ui.update_display(camera.snapshot, camera_image_modifications)
