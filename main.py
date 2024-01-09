import flet as ft
import batch_resizer as br
from pathlib import Path

def main(page: ft.Page):
    def resizeProcess(src, dest, percent):
        destFolder = br.copyImagesFolder(src, str(dest))
        br.parseAndResize(destFolder, percent)

    def openFolder(e: ft.FilePickerResultEvent):
        folderField.value = e.path
        if not folderField.value:
            saveField.value = Path(folderField.value).parent.absolute()
        page.update()

    def saveFolder(e: ft.FilePickerResultEvent):
        saveField.value = e.path
        page.update()
            
    def resize(e):
        if not folderField.value:
            message.value = "PLEASE SELECT A FOLDER"
            message.color = "RED"
            page.update()
        else:
            goButton.disabled = True
            bar.visible = True
            message.value = "IN PROGRESS"
            message.color = "yellow"
            page.update()
            resizeProcess(folderField.value, saveField.value, int(slider.value))
            message.value = "DONE"
            message.color = "green"
            goButton.disabled = False
            bar.visible = False
            page.update()
        

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