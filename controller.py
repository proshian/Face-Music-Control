class Controller():
    def __init__(self, viz_list, cc_sender, sensors, reources):
        self.viz_list = viz_list
        self.cc_sender = cc_sender
        self.sensors = sensors
        self.reources = reources
    
    

    def loop(self):
        for resource in self.reources:
            resource.update_cur_data()
        for sensor in self.sensors:
            raw_data = sensor.acquire_raw() 
            if raw_data is None:
                break
            input_data = sensor.preprocess(raw_data)
            if input_data is None:
                break
            results = sensor.get_results(input_data)
            self.cc_sender.send(sensor.id, results)
            # ui.change_labels(sensor.id, results)
        for vizualizer in self.viz_list:
            vizualizer.visualize()