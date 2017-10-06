from Vision.vision_commands import publish_vision_info
import math


def rad_to_deg(rad):
    return rad*(180/math.pi)

def deg_to_rad(deg):
    return deg*(math.pi/180)



def new_estimated_position(d_moved, a_moved, d_last_seen, a_last_seen):
    rad_last_seen = deg_to_rad(a_last_seen)
    x_old = d_last_seen * math.asin(rad_last_seen)
    y_old = d_last_seen * math.acos(rad_last_seen)
    x_new = x_old + d_moved * math.asin(rad_last_seen)
    y_new = x_new + d_moved * math.acos(rad_last_seen)
    d_new = math.sqrt(x_new*x_new + y_new*y_new)
    a_new = math.atan2(y_new, x_new)
    return (d_new, rad_to_deg(a_new))

    
