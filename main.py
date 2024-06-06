
from Gui import Gui
from BagReader import BagReader
import os
from OnlineSelection import OnlineSelection

subject = 'h7'

dir_bag = '/home/paolo/cvsa_ws/record/' + subject + '/bag'
dir_gdf = '/home/paolo/cvsa_ws/record/' + subject + '/gdf'
dir_mat = '/home/paolo/cvsa_ws/record/' + subject + '/mat_selectedTrials'

for c_file in os.listdir(dir_bag):
    if c_file.endswith(".bag"):
        bag = BagReader(dir_bag + '/' + c_file)
        trials_cf = bag.get_trials_cf()
        trials_cue = bag.get_trials_cue()
        trials_to_keep = OnlineSelection(bag.get_trials_to_keep()).getSelectedTrial()

        n_trials = len(trials_to_keep)
        samplingRate_video = 30
        gui = Gui(trials_cue, trials_cf, trials_to_keep, n_trials, samplingRate_video, c_file[0:-4], dir_gdf, dir_mat)
        





