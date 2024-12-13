from cc_sender import CcSender


class Controller():
    """
    Is responsible for interaction between objects of Resource, Sensor,
    Visualizer classes and cc_sender.

    This is a class, not just a function, because it is allowed to change
    the set of resources, sensors and visualizers during the program's work.
    """
    def __init__(self, viz_list, cc_sender: CcSender, sensors, resources, ui) -> None:
        self.viz_list = viz_list
        self.cc_sender = cc_sender
        self.sensors = sensors
        self.resources = resources
        self.ui = ui
    

    def loop(self):
        for resource in self.resources:
            resource.update_cur_data()
        for sensor in self.sensors:
            raw_data = sensor.acquire_raw() 
            if raw_data is None:
                continue
            results = sensor.get_results_from_raw(raw_data)
            if results is None:
                continue
            self.cc_sender.send(sensor.id, results)
            self.ui._update_labels(sensor.id, results)
        for vizualizaiotn_assembler in self.viz_list:
            vizualizaiotn_assembler.visualize()
