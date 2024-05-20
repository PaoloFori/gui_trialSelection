from BagReader import BagReader
import os
import numpy as np

dir_bag = '/home/paolo/cvsa_ws/record/c7/bag'

for c_file in os.listdir(dir_bag):
    if c_file.endswith(".bag"):
        bag = BagReader(dir_bag + '/' + c_file)
        
        trials_cf = bag.get_trials_cf()
        
        print(f'File: {c_file}')
        
        for i in range(len(trials_cf['id_trial'])):
            l_coords = trials_cf['left_coords'][i]
            r_coords = trials_cf['right_coords'][i]
            
            prev_l_coords = l_coords[0]
            prev_r_coords = r_coords[0]
            
            vel_l = []
            vel_r = []
            
            for j in range(1, len(l_coords)):
                c_l_coords = l_coords[j]
                c_r_coords = r_coords[j]
                
                c_vel_l = (c_l_coords[0] - prev_l_coords[0], c_l_coords[1] - prev_l_coords[1])
                c_vel_r = (c_r_coords[0] - prev_r_coords[0], c_r_coords[1] - prev_r_coords[1])
                
                vel_l.append(c_vel_l)
                vel_r.append(c_vel_r)
                
                prev_l_coords = c_l_coords
                prev_r_coords = c_r_coords
                
            print(f' Trial {i} vel_l:{np.mean(vel_l)} +- {np.std(vel_l)}, vel_r:{np.mean(vel_r)} +- {np.std(vel_r)}')
        
        print(bag.get_trials_to_keep())
            
            