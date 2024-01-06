from tkinter import *
from tkinter import filedialog, Image
import customtkinter as ctk
import batch_resizer as br
from pathlib import Path
from multiprocessing import Process, freeze_support



p = None

def watch():
    global p
    if p:
        if not p.is_alive():
            # Update your progressbar to finished.
            bar.stop()
            bar.destroy()
            proc = None
            message.configure(text="DONE", text_color='green')
            goButton.configure(state="normal")
        else:
            # Re-schedule `watch` to be called again after 0.1 s.
            window.after(100, watch)

def resizeProcess(src, dest, percent):
    destFolder = br.copyImagesFolder(src, str(dest))
    br.parseAndResize(destFolder, percent)

def openFolder():
    global folder
    folder = filedialog.askdirectory(initialdir=Path.cwd)
    if folder:
        folderField.configure(state="normal")
        folderField.configure(placeholder_text=folder)
        folderField.configure(state="disabled")
        
def resize():
    if not 'folder' in globals() or not folder:
        message.configure(text="PLEASE SELECT A FOLDER", text_color='red')
    else:
        goButton.configure(state="disabled")
        bar.pack()
        bar.start()
        message.configure(text="IN PROGRESS", text_color='yellow')
        parentFolder = Path(folder).parent.absolute()
        global p
        p = Process(target=resizeProcess, args=(folder, parentFolder, int(slider.get())))
        p.start()
        watch()
        
def slider_event(value):
    sliderValueText.configure(text=" ".join([str(int(slider.get())), "%"]))

if __name__ == '__main__':
    freeze_support()
    window = ctk.CTk()

    window.title('Batch Resizer')
    window.geometry('800x250')
    window.resizable(False, False)
    # window.eval('tk::PlaceWindow . center')

    # Define layers
    layer1 = ctk.CTkFrame(window, fg_color='transparent')
    layer1.pack(expand=True, fill='x', pady=20)
    layer2 = ctk.CTkFrame(window, fg_color='transparent')
    layer2.pack(expand=True, fill='x')
    layer3 = ctk.CTkFrame(window, fg_color='transparent')
    layer3.pack(expand=True, fill='x')
    layerMessage = ctk.CTkFrame(window, fg_color='transparent')
    layerMessage.pack(fill='x')

    # Layer1: Folder selection
    folderText = ctk.CTkLabel(layer1)
    folderText.configure(text="Select photos folder")
    folderText.pack(side='left', fill='x', padx=(20, 0))

    folderField = ctk.CTkEntry(layer1)
    folderField.configure(state="disabled")
    folderField.pack(side='left', expand=True, fill='x', padx=20)

    folderButton = ctk.CTkButton(layer1)
    folderButton.configure(text="...", command=openFolder, width=20)
    folderButton.pack(side='left', padx=(0, 20))

    # Layer2: Size selection in %
    sliderText = ctk.CTkLabel(layer2)
    sliderText.configure(text="Select a size")
    sliderText.pack(side='left', fill='x', padx=(20, 0))

    slider = ctk.CTkSlider(layer2, from_=10, to=90, command=slider_event, number_of_steps=8)
    slider.set(10)
    slider.pack(side='left', fill='x', expand=True, padx=20)

    sliderValueText = ctk.CTkLabel(layer2)
    sliderValueText.configure(text=" ".join([str(int(slider.get())), "%"]))
    sliderValueText.pack(side='left', fill='x', padx=20)

    # Layer3: Go button
    goButton = ctk.CTkButton(layer3)
    goButton.configure(text="RESIZE",
                        command=resize)
    goButton.pack()

    # messageLayer: Message field
    message = ctk.CTkLabel(layerMessage)
    message.configure(text="")
    message.pack(side='bottom', fill='x', pady=(0, 20))

    bar = ctk.CTkProgressBar(layerMessage, mode="indeterminate")

    window.mainloop()