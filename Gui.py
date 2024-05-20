import tkinter as tk
from PIL import Image as PILImage
from PIL import ImageTk 
import PIL
from sensor_msgs.msg import Image
import numpy as np
import math
from time import sleep
import cv2 as cv

from SavingWithoutRejectTrials import SavingWithoutRejectionTrials

class Gui:
    def __init__(self, trials_cue, trials_cf, trials_to_keep, n_trials, samplingRate_video, file_name, dir_gdf, dir_save, video_size=(500,500)):
        self.n_trials = n_trials
        self.trials_cf = trials_cf
        self.trials_cue = trials_cue
        self.samplingRate_video = samplingRate_video
        self.video_size = video_size
        self.file_name = file_name
        self.dir_gdf = dir_gdf
        self.dir_save = dir_save
        

        # create the window
        self.root = tk.Tk()
        self.root.title("Run: " + file_name)
        self.root.geometry("800x600")

        # create the canvas frame with the scroll bars
        self.canvas = tk.Canvas(self.root)
        vsb = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        hsb = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        hsb.pack(side = "bottom", fill = "x")
        vsb.pack(side = "right", fill = "y")
        self.canvas.pack(expand = True, fill = "both")
        self.canvas.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        

        # create the frame with the thing to display 
        self.display = tk.Frame(self.canvas)
        self.display.grid(row=0, column=0)
        self.var_checkbutton = self.checkButtons() 
        self.selected_trials = [False] * self.n_trials

        [self.video_buttons_cue, self.video_buttons_cf] = self.buttonsVideo()

        self.auto_selection = self.buttonAuto()
        self.trials_to_keep = trials_to_keep

        self.saveButton()

        self.nextButton()

        self.canvas.create_window((0, 0), window=self.display, anchor='nw')
        
        self.root.mainloop()

    def callback_next(self):
        print("Next")
        self.root.destroy()

    def nextButton(self):
        button = tk.Button(self.display, text="Next", command=self.callback_next)
        button.grid(row=4, column=3)


    def callback_save(self):
        print("Saving")
        saving = SavingWithoutRejectionTrials(self.dir_gdf + '/' + self.file_name + '.gdf', self.n_trials)
        saving.save(self.dir_save + '/' + self.file_name + '.mat', self.selected_trials)
        self.root.destroy()

    def saveButton(self):
        button = tk.Button(self.display, text="Save and next", command=self.callback_save)
        button.grid(row=3, column=3)
    
    def callback_tick(self):
        for i, var in enumerate(self.var_checkbutton):
            if var.get():
                self.selected_trials[i] = True
                print(f"Trial {i} selected")
            if not var.get() and self.selected_trials[i]:
                self.selected_trials[i] = False
                print(f"Trial {i} unselected")
            
    def checkButtons(self):
        var_checkbutton = []
        options = ["Trial {}".format(i) for i in range(0, self.n_trials)]
        tk.Message(self.display, text="Select the trials without eye movement").grid(row=0, column=0)
        for option in options:
            var = tk.BooleanVar()
            var_checkbutton.append(var)
            c_checkButton = tk.Checkbutton(self.display, text=option, variable=var, onvalue=True, offvalue=False, command =self.callback_tick)
            c_checkButton.grid(row=options.index(option)+1, column=0)
        return var_checkbutton

    def callBack_auto(self):
        if self.auto_selection.get():
            for i in range(self.n_trials):
                if self.trials_to_keep[i]:
                    self.var_checkbutton[i].set(True)
                    self.selected_trials[i] = True
                else:
                    self.var_checkbutton[i].set(False)
                    self.selected_trials[i] = False

    def buttonAuto(self):
        var = tk.BooleanVar()
        button = tk.Checkbutton(self.display, text="Automatic Selection", variable=var, onvalue=True, offvalue=False, command=self.callBack_auto)
        button.grid(row=0, column=3)
        return var

    def playVideo(self, video_buttons, trials, idx_trial):
        c_images = trials['face_image'][idx_trial]
        c_distance_left2nose = trials['distance_left2nose'][idx_trial]
        c_distance_right2nose = trials['distance_right2nose'][idx_trial]
        c_right_coords = trials['right_coords'][idx_trial]
        c_left_coords = trials['left_coords'][idx_trial]
        c_blink = trials['count_blink'][idx_trial]
        print(f"   len: {len(c_images)}")

        for i in range(len(c_images)):
            c_image = c_images[i]
            tmp = np.frombuffer(c_image.data, dtype=np.uint8)
            image_data = tmp.reshape((c_image.height, c_image.width, int(tmp.size/(c_image.height*c_image.width))))
            image_data = cv.cvtColor(image_data, cv.COLOR_BGR2RGB)
            '''
            cv.putText(image_data, f"Distance left: {c_distance_left2nose[i]}", 
                       (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.putText(image_data, f"Distance right: {c_distance_right2nose[i]}", 
                       (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv.putText(image_data, f"right coords: {c_right_coords[i][0]}, {c_right_coords[i][1]},", (10, 90), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.putText(image_data, f"left coords: {c_left_coords[i][0]}, {c_left_coords[i][1]}", (10, 120), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv.putText(image_data, f"Blink: {c_blink[i]}", (10, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            '''
            
            cv.circle(image_data, (int(c_right_coords[i][0]), int(c_right_coords[i][1])), 5, (0, 0, 255), 1)
            cv.circle(image_data, (int(c_left_coords[i][0]),  int(c_left_coords[i][1])), 5, (0, 0, 255), 1)
            
            # reshape to have always the same size
            if i == 0:
                c_h = c_image.height
                c_w = c_image.width
            else:
                image_data = cv.resize(image_data, (c_w, c_h))
                
            pil_image = PILImage.fromarray(image_data)
            pil_image = pil_image.resize(self.video_size, PIL.Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(image=pil_image)

            self.canvas_video.delete("all")
            self.canvas_video.create_image(0, 0, image=tk_image, anchor='nw')

            self.video.update()
            self.video.after(int(1/self.samplingRate_video*1000))

        sleep(1.0)
        self.video.destroy()
        video_buttons[idx_trial].config(state=tk.NORMAL)


    # cue_cf: 0 if cue and 1 if cd
    def callBack_video(self, trial, cue_cf):
        t = 'cue' if cue_cf == 0 else 'cf'
        print(f"Playing video {t} of trial {trial}")

        self.video = tk.Toplevel(self.root)
        self.video.title(f"Video {t} of trial {trial}")
        self.canvas_video = tk.Canvas(self.video, width=self.video_size[0], height=self.video_size[1])
        self.canvas_video.pack(expand = True, fill = "both")
        self.canvas_video.bind('<Configure>', lambda e: self.canvas_video.configure(scrollregion=self.canvas_video.bbox('all')))

        self.playVideo(self.video_buttons_cue, self.trials_cue, trial) if cue_cf == 0 else self.playVideo(self.video_buttons_cf, self.trials_cf, trial)
        

    def buttonsVideo(self):
        video_buttons_cf = []
        video_buttons_cue = []
        tk.Message(self.display, text="Cues").grid(row=0, column=1)
        tk.Message(self.display, text="Continous feedback").grid(row=0, column=2)
        for i in range(self.n_trials):
            c_button_cue = tk.Button(self.display, text=f"{self.trials_cue['target'][i]}", command=lambda idx = i : self.callBack_video(idx, 0))
            c_button_cue.grid(row=i+1, column=1)
            c_button_cf = tk.Button(self.display, text=f"Trial {i}", command=lambda idx = i : self.callBack_video(idx, 1))
            c_button_cf.grid(row=i+1, column=2)
            video_buttons_cf.append(c_button_cf)
            video_buttons_cue.append(c_button_cue)
        return video_buttons_cue, video_buttons_cf