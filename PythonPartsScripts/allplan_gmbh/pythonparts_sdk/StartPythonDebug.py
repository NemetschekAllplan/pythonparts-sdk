""" Script for starting the Python debugger
"""

# pylint: disable=import-outside-toplevel

from __future__ import annotations

import importlib
import socket

from typing import TYPE_CHECKING, Any

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseInteractor import BaseInteractor
from BuildingElementComposite import BuildingElementComposite
from BuildingElementControlProperties import BuildingElementControlProperties
from BuildingElementPaletteService import BuildingElementPaletteService
from ControlPropertiesUtil import ControlPropertiesUtil
from NemAll_Python_Geometry import Point2D
from StringTableService import StringTableService
from Utils.DebugUtil import DebugUtil

if TYPE_CHECKING:
    from __BuildingElementStubFiles.StartPythonDebugBuildingElement import StartPythonDebugBuildingElement as BuildingElement  # type: ignore
else:
    from BuildingElement import BuildingElement


def check_allplan_version(_build_ele: BuildingElement,
                          _version  : str) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """

    # Support all versions
    return True


def create_interactor(coord_input: AllplanIFW.CoordinateInput,
                      _pyp_path: str,
                      global_str_table_service: StringTableService,
                      build_ele_list: list[BuildingElement],
                      build_ele_composite: BuildingElementComposite,
                      control_props_list: list[BuildingElementControlProperties],
                      _modify_uuid_list: list[str]) -> StartDebugInteractor:

    """ Function for the interactor creation, called when PythonPart is initialized.

    Args:
        coord_input:               coordinate input
        _pyp_path:                  path of the pyp file
        global_str_table_service:  global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
        _modify_uuid_list:          UUIDs of the existing elements in the modification mode

    Returns:
        Created interactor object
    """

    return StartDebugInteractor(coord_input, global_str_table_service, build_ele_list, build_ele_composite, control_props_list)


class StartDebugInteractor(BaseInteractor):
    """Interactor for starting the debugging mode in Allplan

    Args:
        coord_input:               coordinate input
        global_str_table_service:  global string table service for default strings
        build_ele_list:            list with the building elements containing parameter properties
        build_ele_composite:       building element composite
        control_props_list:        control properties list
    """

    def __init__(self,
                 coord_input             : AllplanIFW.CoordinateInput,
                 global_str_table_service: StringTableService,
                 build_ele_list          : list[BuildingElement],
                 build_ele_composite     : BuildingElementComposite,
                 control_props_list      : list[BuildingElementControlProperties]):

        # set initial values

        self.build_ele                 = build_ele_list[0]
        self.coord_input               = coord_input
        self.global_str_table_service  = global_str_table_service
        self.control_props_util        = ControlPropertiesUtil(control_props_list, build_ele_list) # type: ignore

        # check, whether debugpy is installed

        try:
            debugpy = importlib.import_module('debugpy')
        except ImportError:
            AllplanUtil.ShowMessageBox("'debugpy' is not installed!\n\nUse the tool 'Install Python Package' to install it.",
                                       AllplanUtil.MB_OK)
            self.control_props_util.set_enable_condition("StartListenButton", "False")
            return

        # determine, whether already listening for connection

        if self.is_port_in_use(5678):
            if debugpy.is_client_connected():
                self.build_ele.CurrentState.value = self.build_ele.CONNECTED
                self.show_prompt("IDE is already connected")
            else:
                self.build_ele.CurrentState.value = self.build_ele.LISTENING
                self.show_prompt("Listening for connection from IDE")
        else:
            self.show_prompt("Press 'start listening' button on the palette")

        # do other stuff

        self.create_links_to_online_docs()
        self.palette_service = BuildingElementPaletteService([self.build_ele],
                                                             build_ele_composite,
                                                             self.build_ele.script_name,
                                                             control_props_list,
                                                             self.build_ele.pyp_file_name)
        self.palette_service.show_palette(self.build_ele.pyp_file_name)

    def create_links_to_online_docs(self):
        """Create links to online documentation on pythonparts.allplan.com based on current Allplan version"""

        if int(allplan_version := AllplanSettings.AllplanVersion.MainReleaseName()) > 3000:
            allplan_version = "WIP"

        self.build_ele.DebugDocButton.value = f"https://pythonparts.allplan.com/{allplan_version}/manual/for_developer/debugging/"
        self.build_ele.GettingStartedDocButton.value = f"https://pythonparts.allplan.com/{allplan_version}/manual/getting_started/"

    def show_prompt(self, prompt: str):
        """Shows prompt message in the dialog line

        Args:
            prompt: prompt message
        """

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert(prompt))

    def modify_element_property(self, page: int, name: str, value: Any) -> bool:
        """Handles the event of property modification

        Args:
            page: active palette page
            name: name of the modified parameter
            value: new value

        Returns:
            True when palette update required
        """
        return self.palette_service.modify_element_property(page, name, value)

    def on_control_event(self, event_id: int) -> bool:
        """Handles the event of pressing a button on the property palette

        Args:
            event_id:   id of the pressed button

        Returns:
            True, when palette needs to be updated. False otherwise
        """

        if event_id == self.build_ele.START_LISTEN:
            if DebugUtil.start_debugger(False):
                self.build_ele.CurrentState.value = self.build_ele.CONNECTED
                self.show_prompt("Connected successfully. You can close this tool.")
                self.palette_service.update_palette(-1,False)
            else:
                AllplanUtil.ShowMessageBox("Couldn't connect to client", AllplanUtil.MB_OK)
            return True

        return False

    def process_mouse_msg(self,
                          _mouse_msg: int,
                          _pnt      : Point2D,
                          _msg_info : AllplanIFW.AddMsgInfo) -> bool:
        """Handles the mouse message event

        Args:
            _mouse_msg:  mouse message
            _pnt:        mouse position on the viewport
            _msg_info:   additional message info

        Returns:
            True in any situation
        """

        return True

    def on_preview_draw(self):
        """Handles the on preview draw event"""

    def on_mouse_leave(self):
        """Handles the event of mouse leaving the viewport"""

    def on_cancel_function(self) -> bool:
        """Handles the event of hitting ESC - closes the palette and terminates the PythonPart

        Returns:
            True to terminate the PythonPart in any situation
        """

        self.palette_service.close_palette()
        return True

    def on_cancel_by_menu_function(self):
        """Handles the event of terminating the PythonPart by calling another menu function"""

        self.on_cancel_function()

    def on_value_input_control_enter(self) -> bool:
        """Handles the event of input inside the input control in the dialog line

        Returns:
            True in any situation
        """

        return True

    @staticmethod
    def is_port_in_use(port: int) -> bool:
        """Checks, whether a given port is in use

        Args:
            port: port number

        Returns:
            True, when port is in use. False otherwise
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
            except OSError:
                return True

            return False
