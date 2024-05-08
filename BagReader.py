# class to read a bag with deined topics
import rosbag
# TODO: eog is from the mat or gdf file --> eog channel: 19

class BagReader:
    def __init__(self, bag_file):
        self.bag_file = bag_file
        self.cvsa_info = {'left_coords':[], 'right_coords':[], 'face_image' : [], 'right_radius':[], 'left_radius':[], 'blink':[], 'count_blink':[], 
                          'nsecs':[], 'nose_coords':[], 'distance_left2nose':[], 'distance_right2nose':[], 'seq':[]}
        self.event_info = {'event': [], 'nsecs':[]}

        self.trials_cf = {'left_coords':[], 'right_coords':[], 'face_image' : [], 'right_radius':[], 'left_radius':[], 'blink':[], 'count_blink':[], 
                          'nsecs':[], 'nose_coords':[], 'distance_left2nose':[], 'distance_right2nose':[], 'seq':[], 'id_trial': []}
        self.trials_cue = {'left_coords':[], 'right_coords':[], 'face_image' : [], 'right_radius':[], 'left_radius':[], 'blink':[], 'count_blink':[],
                           'nsecs':[], 'nose_coords':[], 'distance_left2nose':[], 'distance_right2nose':[], 'seq':[], 'id_trial': []}
        self.trials_to_keep = []
        self.read_bag()
        self.merge_data()

        #print(f'Number of trials len: {len(self.trials_cf["id"])}, last trial: {self.trials_cf["id"][-1]}, first trial: {self.trials_cf["id"][0]}')
        #print(f'Number left coords trial 0: {len(self.trials_cf["left_coords"][0])}, right coords: {len(self.trials_cf["right_coords"][0])}')

    def read_bag(self):
        bag = rosbag.Bag(self.bag_file)

        for topic, msg, t in bag.read_messages():
            if topic == '/cvsa/eye':
                c_nsecs = msg.header.stamp.secs*1000000000 + msg.header.stamp.nsecs
                c_left_coords = [msg.left_pupil.x, msg.left_pupil.y, msg.left_pupil.z]
                c_right_coords = [msg.right_pupil.x, msg.right_pupil.y, msg.right_pupil.z]
                c_nose_points = [[msg.nose_points[0].x, msg.nose_points[0].y, msg.nose_points[0].z], 
                                 [msg.nose_points[1].x, msg.nose_points[1].y, msg.nose_points[1].z]]
                c_blink = msg.blink
                c_count_blink = msg.count_frame_blinking
                c_distance_left2nose = msg.distance_left
                c_distance_right2nose = msg.distance_right
                c_img = msg.face_image
                c_radius_r = msg.right_radius
                c_radius_l = msg.left_radius
                c_seq = msg.header.seq
                
                self.cvsa_info['left_coords'].append(c_left_coords)
                self.cvsa_info['right_coords'].append(c_right_coords)
                self.cvsa_info['face_image'].append(c_img)
                self.cvsa_info['right_radius'].append(c_radius_r)
                self.cvsa_info['left_radius'].append(c_radius_l)
                self.cvsa_info['blink'].append(c_blink)
                self.cvsa_info['count_blink'].append(c_count_blink)
                self.cvsa_info['nsecs'].append(c_nsecs)
                self.cvsa_info['nose_coords'].append(c_nose_points)
                self.cvsa_info['distance_left2nose'].append(c_distance_left2nose)
                self.cvsa_info['distance_right2nose'].append(c_distance_right2nose)
                self.cvsa_info['seq'].append(c_seq)
            if topic == '/events/bus':
                c_nsecs = msg.header.stamp.secs*1000000000 + msg.header.stamp.nsecs
                c_event = msg.event
                self.event_info['event'].append(c_event)
                self.event_info['nsecs'].append(c_nsecs)
            if topic == "/cvsa/trials_keep":
                self.trials_to_keep = msg.trials_to_keep

        bag.close()

    def merge_data(self):

        if len(self.event_info['event']) != len(self.event_info['nsecs']):
            return ValueError("Event and event_nsecs have different lengths")

        cf_start = []
        cf_end = []
        cue_start = []
        cue_end = []
        for i in range(len(self.event_info['event'])):
            if self.event_info['event'][i] == 781:
                cf_start.append(self.event_info['nsecs'][i])
            if self.event_info['event'][i] == 33549:
                cf_end.append(self.event_info['nsecs'][i])
            if self.event_info['event'][i] in [730, 731]:
                cue_start.append(self.event_info['nsecs'][i])
            if self.event_info['event'][i] in [730+32768, 731+32768]:
                cue_end.append(self.event_info['nsecs'][i])

        idx_trial = 0
        c_left_coords = []
        c_right_coords = []
        c_img = []
        c_radius_l = []
        c_radius_r = []
        c_blink = []
        c_count_blink = []
        c_nsecs = []
        c_nose_points = []
        c_distance_left2nose = []
        c_distance_right2nose = []
        c_seq = []
        
        in_cue = False
        for i in range(len(cf_start)):
            for j in range(len(self.cvsa_info['nsecs'])):
                if cue_start[i] <= self.cvsa_info['nsecs'][j] and cue_end[i] >= self.cvsa_info['nsecs'][j]:
                    in_cue = True
                    c_left_coords.append(self.cvsa_info['left_coords'][j])
                    c_right_coords.append(self.cvsa_info['right_coords'][j])
                    c_img.append(self.cvsa_info['face_image'][j])
                    c_radius_l.append(self.cvsa_info['left_radius'][j])
                    c_radius_r.append(self.cvsa_info['right_radius'][j])
                    c_blink.append(self.cvsa_info['blink'][j])
                    c_count_blink.append(self.cvsa_info['count_blink'][j])                    
                    c_nsecs.append(self.cvsa_info['nsecs'][j])
                    c_nose_points.append(self.cvsa_info['nose_coords'][j])
                    c_distance_left2nose.append(self.cvsa_info['distance_left2nose'][j])
                    c_distance_right2nose.append(self.cvsa_info['distance_right2nose'][j])
                    c_seq.append(self.cvsa_info['seq'][j])
                elif cf_start[i] <= self.cvsa_info['nsecs'][j] and cf_end[i] >= self.cvsa_info['nsecs'][j]:
                    if in_cue:
                        in_cue = False
                        self.trials_cue['id_trial'].append(idx_trial)
                        self.trials_cue['left_coords'].append(c_left_coords)
                        self.trials_cue['right_coords'].append(c_right_coords)
                        self.trials_cue['face_image'].append(c_img)
                        self.trials_cue['right_radius'].append(c_radius_r)
                        self.trials_cue['left_radius'].append(c_radius_l)
                        self.trials_cue['blink'].append(c_blink)
                        self.trials_cue['count_blink'].append(c_count_blink)
                        self.trials_cue['nsecs'].append(c_nsecs)
                        self.trials_cue['nose_coords'].append(c_nose_points)
                        self.trials_cue['distance_left2nose'].append(c_distance_left2nose)
                        self.trials_cue['distance_right2nose'].append(c_distance_right2nose)
                        self.trials_cue['seq'].append(c_seq)
                        c_left_coords = []
                        c_right_coords = []
                        c_img = []
                        c_radius_l = []
                        c_radius_r = []
                        c_blink = []
                        c_count_blink = []
                        c_nsecs = []
                        c_nose_points = []
                        c_distance_left2nose = []
                        c_distance_right2nose = []
                        c_seq = []
                    c_left_coords.append(self.cvsa_info['left_coords'][j])
                    c_right_coords.append(self.cvsa_info['right_coords'][j])
                    c_img.append(self.cvsa_info['face_image'][j])
                    c_radius_l.append(self.cvsa_info['left_radius'][j])
                    c_radius_r.append(self.cvsa_info['right_radius'][j])
                    c_blink.append(self.cvsa_info['blink'][j])
                    c_count_blink.append(self.cvsa_info['count_blink'][j])                    
                    c_nsecs.append(self.cvsa_info['nsecs'][j])
                    c_nose_points.append(self.cvsa_info['nose_coords'][j])
                    c_distance_left2nose.append(self.cvsa_info['distance_left2nose'][j])
                    c_distance_right2nose.append(self.cvsa_info['distance_right2nose'][j])
                    c_seq.append(self.cvsa_info['seq'][j])
                elif cf_end[i] < self.cvsa_info['nsecs'][j]:
                    self.trials_cf['id_trial'].append(idx_trial)
                    self.trials_cf['left_coords'].append(c_left_coords)
                    self.trials_cf['right_coords'].append(c_right_coords)
                    self.trials_cf['face_image'].append(c_img)
                    self.trials_cf['right_radius'].append(c_radius_r)
                    self.trials_cf['left_radius'].append(c_radius_l)
                    self.trials_cf['blink'].append(c_blink)
                    self.trials_cf['count_blink'].append(c_count_blink)
                    self.trials_cf['nsecs'].append(c_nsecs)
                    self.trials_cf['nose_coords'].append(c_nose_points)
                    self.trials_cf['distance_left2nose'].append(c_distance_left2nose)
                    self.trials_cf['distance_right2nose'].append(c_distance_right2nose)
                    self.trials_cf['seq'].append(c_seq)
                    c_left_coords = []
                    c_right_coords = []
                    c_img = []
                    c_radius_l = []
                    c_radius_r = []
                    c_blink = []
                    c_count_blink = []
                    c_nsecs = []
                    c_nose_points = []
                    c_distance_left2nose = []
                    c_distance_right2nose = []
                    c_seq = []
                    idx_trial += 1
                    break

    def get_trials_cf(self):   
        return self.trials_cf   

    def get_trials_cue(self):
        return self.trials_cue       
    
    def get_cvsa_info(self):
        return self.cvsa_info

    def get_event_info(self):
        return self.event_info
    
    def get_trials_to_keep(self):
        return self.trials_to_keep