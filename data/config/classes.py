'''
Labels from each class to be detected
'''

sign_labels = ('sign_speed_limit_start',
               'sign_speed_limit_end',
               'sign_crosswalk',
               'sign_parking_zone',
               'sign_expressway_start',
               'sign_expressway_end',
               'sign_barred_area',
               'sign_pedestrian_island',
               'sign_stop',
               'sign_yield',
               'sign_right',
               'sign_left',
               'sign_no_passing_start',
               'sign_no_passing_end',
               'pedestrian')

sign_labels_ext = ('speed_limit_begin',
               'speed_limit_end',
               'crosswalk',
               'parking_zone',
               'expressway_begin',
               'expressway_end',
               'sign_sharp_turn',
               'barred_area',
               'pedestrian_island',
               'intersection_stop',
               'sign_priority',
               'intersection_yield',
               'intersection_right',
               'intersection_left',
               'sign_forward',
               'no_passing_zone_begin',
               'no_passing_zone_end',
               'sign_uphill',
               'sign_downhill',
               'ground_speed_limit_begin',
               'ground_speed_limit_end',
               'ground_turn_left',
               'ground_turn_right',
               'pedestrian')

# Label map
label_map = {cl: i+1 for i, cl in enumerate(sign_labels)}
label_map['background'] = 0