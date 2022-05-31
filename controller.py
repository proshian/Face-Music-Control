from cc_sender import CcSender


class Controller():
    def __init__(self, viz_list, cc_sender: CcSender, sensors, resources, ui) -> None:
        self.viz_list = viz_list
        self.cc_sender = cc_sender
        self.sensors = sensors
        self.resources = resources
        self.ui = ui
    
    

    def loop(self):
        for resource in self.resources:
            resource.update_scaling_factor()
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
            self.ui._update_labels(sensor.id, results)
        for vizualizer in self.viz_list:
            vizualizer.visualize()