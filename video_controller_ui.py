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
        print("video controller run")
        return self.video_filter.nextFrame()
        
    def getFileTypes(self):
        return self.filetypes

    def selectFile(self, file):
        print("video controller selectFile ", file)
        return self.video_filter.selectVideo(file)

    def exportData(self, out_path_name):
        print("video controller exportData ", out_path_name)
        threading.Thread(target=(lambda: self.video_filter.exportVideo(None, out_path_name))).start()
        


class VideoUI(ui.UI):
    def __init__(self, controller, task_frame_rate) -> None:
        super().__init__(controller, task_frame_rate)
        
        #ui objects definition
        self.last_time = 1
        self.panedWindow = tk.PanedWindow(self.window, orient = tk.VERTICAL)  # orient panes horizontally next to each other

        self.params_frame = tk.Frame(master=self.panedWindow)
        #self.label = tk.Label(master=self.params_frame, text="0")
        #self.entry = tk.Entry(master=self.params_frame)

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
            bg="blue",
            fg="yellow",
            command=self.selectFile
        )
        self.button_export = tk.Button(
            master=self.params_frame,
            text="Export File",
            width=25,
            height=5,
            bg="blue",
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
                    #slider = ui.Slider("brightness", 0, 100, 100)
                    self.label = tk.Label(master=self.params_frame, text=slider.name)
                    self.label.pack()
                    self.sliderComponent, current_value = slider.buildComponent(self.params_frame)
                    self.sliderComponent.bind("<ButtonRelease-1>", slider.eventCallback)
        

        self.image.pack()
        #self.button.bind("<Button-2>", self.callbackSampleEvent)
        self.window.bind("<Key>", self.callbackSampleEvent)

    def stop(self):
        print("stopping")
        self.running = False
        #time.sleep(1)
        self.window.quit()

    def run(self):
        while self.running:
            #start_time = time.perf_counter()

            frame = super().run()
            if frame is not None:
                try:
                    im = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=im)
                    self.image.configure(image=imgtk)
                    self.image.image = imgtk

                except Exception as e:
                    print(e)
                    
                #self.image.update()

            #end_time = time.perf_counter()
            #self.last_time = end_time - start_time
            #print("run")
            #return frame

    def selectFile(self, path = None):
        fps = super().selectFile(path)
        if fps is None:
            fps = 1000

        self.task_frame_rate =  int((1/fps) / 0.001) 
        #frame_rate = self.last_time * 1000
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

    

def handle_click(event):
    print("The button was clicked!")

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

"""
window = tk.Tk()
label = tk.Label(master=window, text="0")
entry = tk.Entry()

def callback():
    value = int(label["text"])
    label["text"] = f"{value - 1}"
    print(value)

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=callback
)
label.pack()
entry.pack()
button.pack()




button.bind("<Button-2>", handle_click)
window.bind("<Key>", handle_keypress)

window.mainloop()
"""

# Bind keypress event to handle_keypress()



