"""Creating a workspace for Visual Studio Code"""

import codecs
import os
import tkinter as tk
from tkinter import filedialog

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil
from BuildingElementPaletteService import BuildingElementPaletteService

print('Load CreateVisualStudioCodeWorkspace.py')

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_interactor(coord_input, _pyp_path, _show_pal_close_btn, _str_table_service,
                      build_ele_list, build_ele_composite, control_props_list, _modify_uuid_list):
    """ Create the interactor """

    return CreateWorkspace(coord_input, build_ele_list, build_ele_composite,  control_props_list)


class CreateWorkspace():
    """ create the workspace """

    def __init__(self, coord_input, build_ele_list, build_ele_composite,  control_props_list):
        """ initialize """

        self.build_ele_list = build_ele_list

        self.is_created = False

        self.palette_service = BuildingElementPaletteService(build_ele_list, build_ele_composite,
                                                             "VSC Workspace",
                                                             control_props_list, "")

        self.palette_service.show_palette("VSC Workspace")

        coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Create a workspace for Visual Studio Code"))


    def on_preview_draw(self):
        """
        Handles the preview draw event
        """


    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """


    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()

        return True


    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            build_ele:  the building element.
            name:       the name of the property.
            value:      new value for property.

        Returns:
            True/False if palette refresh is necessary
        """
        update_palette = self.palette_service.modify_element_property(page, name, value)
        if update_palette:
            self.palette_service.update_palette(-1, False)
        if name == "FileButton___DialogButton___":
            self.execute()
        return True


    def execute(self):
        """ handle the button click """

        file_name = self.build_ele_list[0].FileButton.value

        if self.build_ele_list[0].FileButton.value in {None, "", "Select Folder"}:
            return False

        self.is_created = True

        #Remove extension
        file_name, _ = os.path.splitext(file_name)
        file_name = file_name + ".code-workspace"

        text = \
           r'''{
    "folders": [
            {
                "name": "PythonPartsFramework",
                "path": "$etc$\\PythonPartsFramework"
            },
            {
                "name": "PythonPartsExampleScripts",
                "path": "$usr$\\PythonPartsExampleScripts"
            },
            {
                "name": "PythonParts",
                "path": "$usr$\\Library\\Examples\\PythonParts" '''

        if self.build_ele_list[0].AddNodeVisualScripts.value: # These are located in ETC fodler
            text += \
               r'''
            },
            {
                "name": "VisualScripts",
                "path": "$etc$\\VisualScripts"
            },
            {
                "name": "VisualScripting",
                "path": "$etc$\\Examples\\VisualScripting"'''

        text += \
           r'''
           }
    ],
    "settings": {
        "python.languageServer":"Pylance",'''

        text += '''
            "pylint.args": ["--rcfile=$etc$PythonPartsFramework\\\\pylintrc"],'''

        text += '''
        "python.autoComplete.extraPaths": [
            "$prg$",
            "$etc$PythonPartsFramework\\\\GeneralScripts",
            "$etc$PythonPartsFramework\\\\TestHelper",
            "$etc$PythonPartsFramework",
            "$etc$VisualScripts",
            "$etc$PythonParts-site-packages",
            "$usr$PythonParts-site-packages",
            "$std$PythonParts-site-packages",
        ],

        "python.defaultInterpreterPath": "$prg$\\\\Python\\\\python.exe",

        "files.exclude": {
            "**/*_bul.xml": true,
            "**/*_chn.xml": true,
            "**/*_eng.xml": true,
            "**/*_fra.xml": true,
            "**/*_grc.xml": true,
            "**/*_hol.xml": true,
            "**/*_hrv.xml": true,
            "**/*_ita.xml": true,
            "**/*_jpn.xml": true,
            "**/*_pol.xml": true,
            "**/*_prt.xml": true,
            "**/*_rum.xml": true,
            "**/*_rus.xml": true,
            "**/*_slk.xml": true,
            "**/*_spa.xml": true,
            "**/*_svn.xml": true,
            "**/*_tch.xml": true,
            "**/*_trk.xml": true,
            "**/*_ung.xml": true,
            "**/*pyproj": true,
            "**/*sln": true,
            "**/*__py*": true,
            "**/.vs": true,
        },
        "python.analysis.extraPaths": [
            "$prg$",
            "$etc$PythonPartsFramework\\\\GeneralScripts",
            "$etc$PythonPartsFramework\\\\TestHelper",
            "$etc$PythonPartsFramework",
            "$etc$VisualScripts\\\\TestUtil",
            "$etc$VisualScripts",
            "$etc$PythonParts-site-packages",
            "$usr$PythonParts-site-packages",
            "$std$PythonParts-site-packages",
        ],
        "files.trimTrailingWhitespace": true,
        "python.analysis.stubPath": "$etc$PythonPartsFramework\\\\InterfaceStubs",
    },

    "extensions": {
        "recommendations": [
            "ms-python.python",
            "ms-python.pylint",
            "Allplan.PythonPartTools",
            "chouzz.vscode-better-align",
            "redhat.vscode-xml",
        ]
    },
    "launch": {
        "version": "0.2.0",
        "configurations": [
        {
            "name": "Attach to Allplan",
            "connect": {
                "port": 5678,
                "host": "localhost",
            },
            "request": "attach",
            "type": "debugpy",
            "justMyCode": false,
        },
        ]
    },
}'''

        prg_path = AllplanSettings.AllplanPaths.GetPrgPath().replace("\\", "\\\\")
        etc_path = AllplanSettings.AllplanPaths.GetEtcPath().replace("\\", "\\\\")
        usr_path = AllplanSettings.AllplanPaths.GetUsrPath().replace("\\", "\\\\")
        std_path = AllplanSettings.AllplanPaths.GetStdPath().replace("\\", "\\\\")

        text = text.replace("$prg$", prg_path).replace("$etc$", etc_path).replace("$usr$", usr_path).replace("$std$", std_path)

        try:
            with codecs.open(file_name, "w") as file:
                file.write(text)

            file.close()

        except Exception as e:
            AllplanUtil.ShowMessageBox("An Error Occured, please see stack trace for more info.", AllplanUtil.MB_OK)
            return

        AllplanUtil.ShowMessageBox("Workspace created Successfully", AllplanUtil.MB_OK)
        if not self.build_ele_list[0].UsePylint.value:
            return



    def process_mouse_msg(self, _mouse_msg, _pnt, _msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """

        if self.is_created:
            self.palette_service.close_palette()

        return not self.is_created
