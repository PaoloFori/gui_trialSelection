import numpy as np

class AutomaticSelection:
    def __init__(self, trials_cf):
        self.trials_cf = trials_cf
        self.trialNOTrejected = []

    
    def set_tresholds(self, th_right, th_left):
        self.th_right = th_right
        self.th_left = th_left


    def compute_rejection(self):
        count_trial2reject = np.zeros(len(self.trials_cf['id_trial']))

        for trial in self.trials_cf['id_trial']:
            left_coords = self.trials_cf['left_coords'][trial]
            right_coords = self.trials_cf['right_coords'][trial]

            for i in range(len(left_coords)):
                if i == 0:
                    continue 
                d_left = self.compute_distance(left_coords[i-1], left_coords[i])
                d_right = self.compute_distance(right_coords[i-1], right_coords[i])
                #print(f'Distance left: {d_left}, right: {d_right}')
                if d_left > self.th_left and d_right > self.th_right:
                    count_trial2reject[trial] += 1
        
        #print(f'Trials to reject counter: {count_trial2reject.tolist()}')
        self.trialNOTrejected = [1 if value == 0 else 0 for value in count_trial2reject]
        #print(f'Trials to reject: {self.trialNOTrejected}')

    def compute_distance(self, p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def get_trialNOTrejected(self):
        return self.trialNOTrejected