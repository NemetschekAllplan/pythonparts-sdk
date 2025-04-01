"""
Encrypt a PythonPart script
"""

import os
import glob

import tkinter as tk

from tkinter import filedialog

import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from BuildingElementService import BuildingElementService
from ControlPropertiesUtil import ControlPropertiesUtil
from CreateElementResult import CreateElementResult

print('Load EncryptPythonPartScript.py')


def check_allplan_version(_build_ele: BuildingElement,
                          _version:   float) -> bool:
    """
    Check the current Allplan version

    Args:
        _build_ele: the building element.
        _version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Support all versions
    return True


def initialize_control_properties(build_ele     : BuildingElement,
                                  ctrl_prop_util: ControlPropertiesUtil,
                                  doc           : AllplanElementAdapter.DocumentAdapter) -> None:
    """ initialize the control properties

    Args:
        build_ele     : building element
        ctrl_prop_util: control properties
        doc           : document
    """

    modify_control_properties(build_ele, ctrl_prop_util, "", 1001, doc)
    modify_control_properties(build_ele, ctrl_prop_util, "", 1002, doc)
    modify_control_properties(build_ele, ctrl_prop_util, "", 1003, doc)


def modify_control_properties(build_ele     : BuildingElement,
                              ctrl_prop_util: ControlPropertiesUtil,
                              _value_name   : str,
                              event_id      : int,
                              _doc          : AllplanElementAdapter.DocumentAdapter) -> bool:
    """ modify the control properties

    Args:
        build_ele     : building element
        ctrl_prop_util: control properties
        _value_name   : name of the modified value
        event_id      : event ID
        doc           : document

    Returns:
        update the property palette
    """

    if event_id == 1001:
        ctrl_prop_util.set_text("FileButton", build_ele.File.value)

        return True

    if event_id == 1002:
        ctrl_prop_util.set_text("DirectoryButton", build_ele.Directory.value)

        return True

    if event_id == 1003:
        ctrl_prop_util.set_text("TargetDirectoryButton", build_ele.TargetDirectory.value)

        return True

    return True


def on_control_event(build_ele: BuildingElement,
                     event_id: int) -> bool:
    """ handle the control event from a button click

    Args:
        build_ele:  the building element.
        event_id:   event id of control.

    Returns:
        update the property palette
    """

    if event_id == 1001:
        root = tk.Tk()
        root.withdraw()

        print(os.path.dirname(build_ele.File.value))

        build_ele.File.value = filedialog.askopenfilename(defaultextension='.py', filetypes=[('py file','*.py'), ('All files','*.*')],
                                                          initialdir = os.path.dirname(build_ele.File.value))

        root.destroy()

        return True

    if event_id == 1002:
        root = tk.Tk()
        root.withdraw()

        build_ele.Directory.value = filedialog.askdirectory(initialdir = build_ele.Directory.value)

        root.destroy()

        return True

    if event_id == 1003:
        root = tk.Tk()
        root.withdraw()

        build_ele.TargetDirectory.value = filedialog.askdirectory(initialdir = build_ele.TargetDirectory.value)

        root.destroy()

        return True

    if event_id == 1010:
        if build_ele.FileOrDirectory.value == 1:
            encrypt_file(build_ele.File.value, build_ele.TargetDirectory.value)
        else:
            encrypt_directory(build_ele.Directory.value, build_ele.TargetDirectory.value)

        BuildingElementService.write_data_to_default_favorite_file([build_ele])

        AllplanUtil.ShowMessageBox("File(s) successfully encrypted, log available in trace window", AllplanUtil.MB_OK)

    return True


def create_element(_build_ele, _doc) -> CreateElementResult:
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
        result of the created element
    """

    return CreateElementResult()


def encrypt_file(file_name  : str,
                 target_path: str):
    """ encrypt a file

    Args:
        file_name:   name of the file
        target_path: target path
    """

    print("encrypt: ", file_name)

    with open(file_name, "r", encoding="utf_8_sig") as file:
        code = file.read()

    base_name = os.path.basename(file_name)

    code = AllplanUtil.EncryptString(code, base_name.rsplit(".", 1)[-1])

    base_name = base_name.replace(".py", ".pye")

    with open(target_path + "\\" + base_name, "w", encoding="utf_8") as file:
        file.write(code)


def encrypt_directory(directory_name: str,
                      target_path   : str):
    """ encrypt a file

    Args:
        directory_name: name of the directory
        target_path:    target path
    """

    print("")
    print("-----------------------------")

    for file_name in glob.glob(directory_name + "\\*"):
        if file_name.endswith("__pycache__"):
            continue

        if file_name.endswith(".py"):
            encrypt_file(file_name, target_path)

        elif os.path.isdir(file_name):
            sub_target_path = target_path + "\\" + os.path.basename(file_name)

            if not os.path.exists(sub_target_path):
                os.makedirs(sub_target_path)

            encrypt_directory(file_name, sub_target_path)
