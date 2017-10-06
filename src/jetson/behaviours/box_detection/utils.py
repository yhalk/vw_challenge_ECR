import numpy as np

def angle_between_points(p1, p2):
    '''
       Calculates the angle between two points

       arguments:
         p1 is the location of the object
         p2 is the straight line from the robot
       returns:
         the angle in degrees
    '''
    # angle_1 = np.arctan2(*p1[::-1])
    # angle_2 = np.arctan2(*p2[::-1])
    # return np.rad2deg((angle_1 - angle_2) % (2 * np.pi))
    p1 = [(p1[0] - p2[0]), p1[1]]
    p2 = [0, p1[1]]
    distance_p1 = np.sqrt(np.sum(np.power(p1,2)))
    distance_p2 = np.sqrt(np.sum(np.power(p2,2)))
    combined_distance = distance_p1 * distance_p2
    p1_p2_1 = p1[0] * p2[0]
    p1_p2_2 = p1[1] * p1[1]
    combined_points = p1_p2_1 + p1_p2_2

    cos_theta = combined_points / combined_distance

    if p1[0] < p2[0]:
        return np.rad2deg(np.arccos(cos_theta))
    else:
        return 0- np.rad2deg(np.arccos(cos_theta))

def distance_between_points(p0, p1):
    '''
       Calculates the distance between two points
    '''
    return np.sqrt(np.power(p0[0] - p1[0], 2) + np.power(p0[1] - p1[1], 2))

def calculate_angle_and_distance(width, x1, x2, y1, y2):

    angle = angle_between_points(((x1+x2)/2.0,(y1+y2)/2.0), (width/2.0, 0.0))
    focal_length_onboard_camera = 1.0 # in mm
    average_real_object_height = 1.0 # in mm
    object_height = distance_between_points([x1,y1], [x1,y2])
    sensor_height = 314.2 # in mm
    #distance_between_robot_and_object = (51.525 * 123) / distance_between_points([x1,y1], [x2,y1])
    #approximate distance is width of the object times focal length divided by width of the image
    distance_between_robot_and_object = 132 * 450 / distance_between_points([x1,y1], [x2,y1])
    #distance_between_robot_and_object = distance_between_robot_and_object * 1.5
    return angle, distance_between_robot_and_object
