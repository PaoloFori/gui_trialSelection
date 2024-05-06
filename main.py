
from Gui import Gui
from BagReader import BagReader
import os


dir_bag = '/home/paolo/cvsa_ws/record/bag'
dir_gdf = '/home/paolo/cvsa_ws/record/gdf'
dir_mat = '/home/paolo/cvsa_ws/record/mat/manualSelectionTrials'

for c_file in os.listdir(dir_bag):
    if c_file.endswith(".bag"):
        bag = BagReader(dir_bag + '/' + c_file)
        trials_cf = bag.get_trials_cf()
        trials_cue = bag.get_trials_cue()

        n_trials = 20
        samplingRate_video = 30
        gui = Gui(trials_cue, trials_cf, n_trials, samplingRate_video, c_file[0:-4], dir_gdf, dir_mat)
        





