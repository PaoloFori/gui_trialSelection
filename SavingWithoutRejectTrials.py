import mne
import numpy as np
import scipy.io as sio

class Header:
    def __init__(self):
        self.TYP = []
        self.POS = []
        self.DUR = []

    def configure(self, typ, pos, dur):
        self.TYP = typ
        self.POS = pos
        self.DUR = dur
    
    def setTyp(self, typ):
        self.TYP = typ

    def setPos(self, pos):
        self.POS = pos

    def setDur(self, dur):
        self.DUR = dur


class SavingWithoutRejectionTrials:
    def __init__(self, path, n_trials=20):
        self.path = path
        self.OFF = 32768
        self.event_id = [730,731,781,786,897,898]
        self.header = Header()
        self.n_trials = n_trials

        self.trials_selected = [False] * self.n_trials

        self.loadData()

        self.arrangeData()

    def loadData(self):
        self.data = mne.io.read_raw_gdf(self.path)
        self.signal = self.data.get_data().T

    def arrangeData(self):
        events = mne.events_from_annotations(self.data)
        c_dict = events[1]
        reversed_dict = {v: k for k, v in c_dict.items()}
        annotations = events[0]
        c_annotations = []
        for a in annotations:
            c_annotations.append([a[0], int(reversed_dict[a[2]])])

        TYP = []
        POS = []
        DUR = []

        for i in range(len(c_annotations)):
            if i == 0:
                TYP.append(1)
                POS.append(c_annotations[i][0])
                DUR.append(len(self.signal) - c_annotations[i][0])
            else:
                if c_annotations[i][1] in self.event_id:
                    c_event = c_annotations[i][1]
                    TYP.append(c_annotations[i][1])
                    POS.append(c_annotations[i][0])
                    c_start = c_annotations[i][0]
                elif c_annotations[i][1] == c_event + self.OFF:
                    c_end = c_annotations[i][0]
                    DUR.append(c_end - c_start)

        self.header.configure(TYP, POS, DUR)
    
    def save(self, output_path, trials_selected):
        self.trials_selected = trials_selected

        fix = [index for index, element in enumerate(self.header.TYP) if element == 786]
        cue = [index for index, element in enumerate(self.header.TYP) if (element == 730 or element == 731)]
        cf  = [index for index, element in enumerate(self.header.TYP) if element == 781]
        hit = [index for index, element in enumerate(self.header.TYP) if (element == 897 or element == 898)]

        for i in range(len(fix)):
            if not self.trials_selected[i]:
                self.header.TYP[fix[i]] = 0
                self.header.POS[fix[i]] = 0
                self.header.DUR[fix[i]] = 0
                self.header.TYP[cue[i]] = 0
                self.header.POS[cue[i]] = 0
                self.header.DUR[cue[i]] = 0
                self.header.TYP[cf[i]]  = 0
                self.header.POS[cf[i]]  = 0
                self.header.DUR[cf[i]]  = 0
                self.header.TYP[hit[i]] = 0
                self.header.POS[hit[i]] = 0
                self.header.DUR[hit[i]] = 0

        
        sio.savemat(output_path, {'signal': self.signal, 'header': self.header})

