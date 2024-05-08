import numpy as np

class OnlineSelection:
    
    def __init__(self, selecred_trials):
        self.selected_trials = []
        for trial in selecred_trials:
            self.selected_trials.append(True) if trial == 1 else self.selected_trials.append(False)  
            
    def getSelectedTrial(self):
        return self.selected_trials 
        