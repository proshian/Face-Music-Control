import os
import random
from functools import partial

from sensor import Sensor


def get_3_rand_vals(names):
    return [random.uniform(0, 1) for _ in names]

def create_random_vg():
    names = ["rand 1", "rand 2", "rand 3"]
    icon_locations = [os.path.join("icons","numbers", f"{num}.svg") for num in range(1,4)]

    rand_sens = Sensor( 
        names, icon_locations,
        partial(get_3_rand_vals, names), 0, 1)
    
    return rand_sens

rand_sens = create_random_vg()