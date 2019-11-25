'''
Labels from each class to be detected
'''
sign_labels = ('speed_limit_begin',
               'speed_limit_end',
               'crosswalk',
               'parking_zone',
               'expressway_begin',
               'expressway_end',
               'sharp_turn_small',
               'sharp_turn_big',
               'barred_area',
               'pedestrian_island',
               'intersection_stop',
               'intersection_priority',
               'intersection_yield',
               'intersection_right',
               'intersection_left',
               'intersection_front',
               'no_passing_zone_begin',
               'no_passing_zone_end',
               'steep_uphill',
               'steep_downhill',
               'ground_speed_limit_begin',
               'ground_speed_limit_end',
               'ground_turn_left',
               'ground_turn_right',
               'pedestrian')

# Label map
label_map = {cl: i+1 for i, cl in enumerate(sign_labels)}
label_map['background'] = 0