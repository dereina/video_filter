from abc import ABC, abstractmethod
from subprocess import call
import tkinter as tk
import utils

class ControllerInterface(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def callbackSample(self):
        pass

    @abstractmethod
    def callbackSampleEvent(self, event):
        pass

    @abstractmethod
    def run(self):
        pass

class UI(ControllerInterface):
    def __init__(self, controller, task_frame_rate) -> None:
        super().__init__()
        self.controller = controller
        self.task_frame_rate = task_frame_rate
        #ui objects definition
        self.window = tk.Tk()
        
        self.window.after(self.task_frame_rate, self.run)  # reschedule event in task_frame_rate seconds

    @utils.timeit
    def run(self):
        print("run")
        self.controller.run()
        self.window.after(self.task_frame_rate, self.run)

    def main(self):
        self.window.mainloop()

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



