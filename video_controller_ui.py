import ui
import filter
import tkinter as tk

class VideoController(ui.ControllerInterface):
    def __init__(self, video_filter) -> None:
        super().__init__()
        self.video_filter = video_filter

    def main(self):
        print("video controller main")

    def callbackSample(self):
        print("video controller callbackSample")

    def callbackSampleEvent(self, event):
        print("video controller callbackSampleEvent", event)

    def run(self):
        print("video controller run")
        pass

class VideoUI(ui.UI):
    def __init__(self, controller, task_frame_rate) -> None:
        super().__init__(controller, task_frame_rate)
        #ui objects definition
        self.label = tk.Label(master=self.window, text="0")
        self.entry = tk.Entry(master=self.window)

        self.button = tk.Button(
            master=self.window,
            text="Click me!",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command=self.callbackSample
        )
        self.label.pack()
        self.entry.pack()
        self.button.pack()

        self.button.bind("<Button-2>", self.callbackSampleEvent)
        self.window.bind("<Key>", self.callbackSampleEvent)


    def callbackSample(self):
        print("VideoUI callbackSample ")
        super().callbackSample()
        pass

    def callbackSampleEvent(self, event):
        print("VideoUI callbackSampleEvent ",  event)
        super().callbackSampleEvent(event)
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



