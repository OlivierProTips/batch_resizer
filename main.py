import flet as ft
from pathlib import Path
from os import path, walk
from datetime import datetime
from shutil import copytree
from PIL import Image

def main(page: ft.Page):
        
    def printMessage(msg, color):
        message.value = msg
        message.color = color
        page.update()

    def copyImagesFolder(_src_folder: str, _dest_folder: str):
        # Step 1: copy images folder
        while _src_folder.endswith(path.sep):
            _src_folder = _src_folder[:-1]
        while _dest_folder.endswith(path.sep):
            _dest_folder = _dest_folder[:-1]

        _folder_name = path.basename(_src_folder)
        _timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
        _dest_folder = path.join(_dest_folder, _folder_name + "_" + str(_timestamp))

        if path.exists(_dest_folder):
            printMessage("Destination folder already exists", "red")
            return None
        try:
            copytree(_src_folder, _dest_folder)
        except Exception as e:
            printMessage("Photos cannot be copied into destination", "red")
            return None
    
        return _dest_folder

    def parseAndResize(_dest_folder: str, _percent: int):
        # Step 2: Parse and resize images
        fileCpt = 0
        for root, _, files in walk(_dest_folder):
            for name in files:
                fileCpt += 1
                bar.value = fileCpt / len(files)
                page.update()
                fullname = str(path.join(root, name))
                try:
                    image = Image.open(fullname)
                    width, height = image.size
                    image.thumbnail((width * _percent // 100, height * _percent // 100))
                    image.save(fullname)
                except:
                    pass
  
    def resizeProcess(src, dest, percent):
        destFolder = copyImagesFolder(src, str(dest))
        if destFolder:
            parseAndResize(destFolder, percent)

    def openFolder(e: ft.FilePickerResultEvent):
        folderField.value = e.path
        if not saveField.value:
            saveField.value = Path(folderField.value).parent.absolute()
        page.update()

    def saveFolder(e: ft.FilePickerResultEvent):
        saveField.value = e.path
        page.update()
            
    def resize(e):
        if not folderField.value:
            printMessage("PLEASE SELECT A FOLDER", "RED")
        else:
            goButton.disabled = True
            bar.visible = True
            printMessage("IN PROGRESS", "yellow")
            resizeProcess(folderField.value, saveField.value, int(slider.value))
            goButton.disabled = False
            bar.visible = False
            printMessage("DONE", "green")

    page.title = 'Batch Resizer'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 800
    page.window_height = 350
    page.window_resizable = False
    page.padding=20
    
    selectFolder = ft.FilePicker(on_result=openFolder)
    selectSaveFolder = ft.FilePicker(on_result=saveFolder)
    page.overlay.append(selectFolder)
    page.overlay.append(selectSaveFolder)
    
    folderField = ft.TextField(label="Select photos folder", disabled=True, value="", expand=True)
    folderButton = ft.IconButton(ft.icons.FOLDER, 
                                 on_click=lambda _: selectFolder.get_directory_path(initial_directory=str(Path.cwd().absolute())),
                                 icon_color="blue")
    
    saveField = ft.TextField(label="Select destination folder", disabled=True, value="", expand=True)
    saveButton = ft.IconButton(ft.icons.FOLDER, 
                                 on_click=lambda _: selectSaveFolder.get_directory_path(initial_directory=str(Path.cwd().absolute())),
                                 icon_color="blue")
    
    sliderText = ft.Text(value="Select a size")
    slider = ft.Slider(min=10, 
                       max=90, 
                       divisions=8, 
                       value=10,
                       label="{value}%", 
                       expand=True,
                       thumb_color="blue")
    
    goButton = ft.IconButton(ft.icons.PLAY_ARROW_ROUNDED, on_click=resize, bgcolor="green")
    
    bar = ft.ProgressBar(width=400, visible=False, color="blue")
    message = ft.Text(value="")
    
    # Define layers
    page.add(
        ft.Row(
            [
                folderField,
                folderButton,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                saveField,
                saveButton,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                sliderText,
                slider,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                goButton,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                bar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    
if __name__ == '__main__':
    ft.app(target=main)