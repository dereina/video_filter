import ui
import filter
import tkinter as tk
from PIL import Image, ImageTk
import time
import threading

class VideoController(ui.ControllerInterface):
    def __init__(self, video_filter, filetypes = ( ('video files', '*.avi'), ('text files', '*.txt'), ('All files', '*.*') )) -> None:
        super().__init__()
        self.video_filter = video_filter
        self.filetypes = filetypes

    def main(self):
        print("video controller main")

    def callbackSample(self):
        print("video controller callbackSample")

    def callbackSampleEvent(self, event):
        print("video controller callbackSampleEvent", event)

    def getUIMetadata(self):
        out =[]
        for filter in self.video_filter.getFilters():
            ls = filter.getUIMetadata()
            if len(ls):
                out.append(ls)

        return out

    def run(self):
        return self.video_filter.nextFrame()
        
    def getFileTypes(self):
        return self.filetypes

    def stopCurrent(self):
        self.video_filter.stop()

    def selectFile(self, file):
        print("video controller selectFile ", file)
        return self.video_filter.selectVideo(file)
    


    def exportData(self, out_path_name):
        print("video controller exportData ", out_path_name)
        threading.Thread(target=(lambda: self.video_filter.exportVideo(None, out_path_name))).start()
        

class VideoUI(ui.UI):
    def __init__(self, controller, task_frame_rate) -> None:
        super().__init__(controller, task_frame_rate)
        self.last_time = 1
        self.panedWindow = tk.PanedWindow(self.window, orient = tk.VERTICAL)

        self.params_frame = tk.Frame(master=self.panedWindow)
        self.image_frame = tk.Frame(master=self.panedWindow)

        self.panedWindow.add(self.image_frame)
        self.panedWindow.add(self.params_frame)
        
        self.panedWindow.pack(fill = tk.BOTH, expand = True)  

        self.image = tk.Label(master=self.image_frame)
        self.image.image = None

        self.button_select = tk.Button(
            master=self.params_frame,
            text="Select File",
            width=25,
            height=5,
            bg="green",
            fg="yellow",
            command=self.selectFile
        )
        self.button_export = tk.Button(
            master=self.params_frame,
            text="Export File",
            width=25,
            height=5,
            bg="orange",
            fg="yellow",
            command=self.exportData
        )
        self.button_select.pack()
        self.button_export.pack()

        self.params_frame.pack(side=tk.RIGHT)
        self.image_frame.pack(side=tk.LEFT)
        listList = controller.getUIMetadata()
        for l in listList:
            for slider in l:
                if isinstance(slider, ui.Slider):
                    self.label = tk.Label(master=self.params_frame, text=slider.name)
                    self.label.pack()
                    self.sliderComponent, current_value = slider.buildComponent(self.params_frame)
                    self.sliderComponent.bind("<ButtonRelease-1>", slider.eventCallback)

        self.image.pack()
        #self.button.bind("<Button-2>", self.callbackSampleEvent)
        self.window.bind("<Key>", self.callbackSampleEvent)

    def run(self):
        while self.running:
            frame = super().run()
            if frame is not None:
                #try:
                    im = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=im)
                    self.image.configure(image=imgtk)
                    self.image.image = imgtk

                #except Exception as e:
                #    print(e)
        
        self.window.quit()

    def selectFile(self, path = None):
        self.controller.stopCurrent()
        fps = super().selectFile(path)
        if fps is None:
            fps = 1000

        self.task_frame_rate =  int((1/fps) / 0.001) 
        if self.task_frame_rate< 1:
            self.task_frame_rate= 1
        
        return self.task_frame_rate

    def callbackSample(self):
        print("callbackSample ")
        self.controller.callbackSample()
        pass

    def callbackSampleEvent(self, event):
        print("callbackSampleEvent ",  event)
        self.controller.callbackSampleEvent(event)
        pass

    

