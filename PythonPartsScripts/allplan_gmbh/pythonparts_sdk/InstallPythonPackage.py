"""
Script for installing a Python package
"""

#pylint: disable=global-statement

import subprocess
import winreg

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_Utility as AllplanUtil

from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

HKCU = winreg.HKEY_CURRENT_USER
ENV = "Environment"
PATH = "PYTHONPATH"
DEFAULT = "%PATH%"


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str):
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


def create_element(_build_ele: BuildingElement,
                   _doc      : AllplanElementAdapter.DocumentAdapter) -> CreateElementResult:
    """
    Creation of element

    Args:
        _build_ele: the building element.
        -doc:       input document

    Returns:
        created element result
    """

    return CreateElementResult()


def on_control_event(build_ele: BuildingElement,
                     event_id  : int) -> bool:
    """ install a Python package

    Args:
        build_ele: the building element.
        event_id:  event ID

    Returns:
        update the palette state
    """

    prg_path = AllplanSettings.AllplanPaths.GetPrgPath() + "\\"


    package = build_ele.package.value or ""

    if not package:
        return False
    build_ele.package.value = ""

    #--------------------- install the package
    path  = AllplanSettings.AllplanPaths.GetUsrPath()
    if build_ele.installLocation.value == "STD":
        path  = AllplanSettings.AllplanPaths.GetStdPath()
    if build_ele.installLocation.value == "ETC":
        path  = AllplanSettings.AllplanPaths.GetEtcPath()

    target_dir  = f"{path}PythonParts-site-packages"
    try:
        subprocess.check_call([prg_path + "Python\\Python.exe", "-m", "pip", "install", "--target", target_dir, package,  "--no-cache-dir"])
        AllplanUtil.ShowMessageBox(f"{package} installed succesfully. The installation log can be found in the Trace window", AllplanUtil.MB_OK)
    except Exception as _:
        AllplanUtil.ShowMessageBox(f"Istallation of {package} failed. The error log can be found in the Trace window", AllplanUtil.MB_OK)
    return True
