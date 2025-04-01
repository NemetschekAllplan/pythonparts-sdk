""" Script for DownloadPythonParts
"""

# pylint: disable=consider-using-with
# pylint: disable=broad-exception-caught

from __future__ import annotations

import os

import NemAll_Python_AllplanSettings as AllplanSettings
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_Utility as AllplanUtil

from BaseScriptObject import BaseScriptObject, BaseScriptObjectData
from BuildingElement import BuildingElement
from CreateElementResult import CreateElementResult

from ScriptObjectInteractors.OnCancelFunctionResult import OnCancelFunctionResult

from . import GithubUtil

ALLPLAN_VERSION = AllplanSettings.AllplanVersion.Version()

def check_allplan_version(_build_ele: BuildingElement,
                          _version  : type) -> bool:
    """ Check the current Allplan version

    Args:
        _build_ele: building element with the parameter properties
        _version:   the current Allplan version

    Returns:
        True
    """
    return True


def create_script_object(build_ele         : BuildingElement,
                         script_object_data: BaseScriptObjectData) -> BaseScriptObject:
    """ Create the script object

    Args:
        build_ele:          building element with the parameter properties
        script_object_data: script object data

    Returns:
        The created script object
    """

    return DownloadPythonParts(build_ele, script_object_data)


class DownloadPythonParts(BaseScriptObject):
    """Definition of class DownloadPythonParts
    """

    def __init__(self,
                 _build_ele        : BuildingElement,
                 script_object_data: BaseScriptObjectData):
        """ Initialization of class DownloadPythonParts

        Args:
            _build_ele:         building element with the parameter properties
            script_object_data: script object data
        """

        super().__init__(script_object_data)

        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert("Download Python Part Examples"))

        self.execute_download()

        self.coord_input.CancelInput()


    def start_input(self):
        """Starts the input
        """


    def execute(self) -> CreateElementResult:
        """ Execute the script

        Returns:
            created element result
        """

        return CreateElementResult([])


    def on_cancel_function(self) -> OnCancelFunctionResult:
        """ Handles the cancel function event (e.g. by ESC, ...)

        Returns:
            True : cancel the input
            False: continue the input
            None : in case of not implemented
        """

        return OnCancelFunctionResult.CANCEL_INPUT


    @staticmethod
    def execute_download():
        """ Execute the github download.
        """

        owner, repo = 'NemetschekAllplan', 'PythonPartsExamples'
        branch      = AllplanSettings.AllplanVersion.MainReleaseName()
        sha_file    = f"{AllplanSettings.AllplanPaths.GetUsrPath()}PythonPartsExamples-sha.txt"
        old_sha     = None
        proceed     = AllplanUtil.IDOK

        if os.path.exists(sha_file):
            with open(sha_file, encoding="UTF-8") as f:
                old_sha = f.read()

        if old_sha is None:
            proceed = AllplanUtil.ShowMessageBox("You are about to download PythonPart examples from Github repository." \
                                                 "\nDo you want to proceed?", AllplanUtil.MB_YESNO)

        if proceed == AllplanUtil.IDNO:
            return

        if not GithubUtil.check_github_branch_exists(owner, repo, branch):
            branch = "main"

        try:
            data = GithubUtil.get_last_commit_info(owner, repo, branch)

        except Exception as e:
            print(f"Encountered the following issue {e}")

        new_sha = data.get("sha", None)

        if old_sha and new_sha == old_sha:
           proceed =  AllplanUtil.ShowMessageBox("The PythonPart examples on your PC appear to be up-to-date. " + 
                                       "Would you like to proceed with a force update regardless?", AllplanUtil.MB_YESNO)

        if proceed == AllplanUtil.IDNO:
            return

        if old_sha is not None:
            proceed = AllplanUtil.ShowMessageBox("You are about to override the PythonPart examples.\n" + \
                                                 "The entire content of the following directories will be replaced:\n\n" + \
                                                 f"{AllplanSettings.AllplanPaths.GetUsrPath()}Library\\Examples\\PythonParts\n" +  \
                                                 f"{AllplanSettings.AllplanPaths.GetUsrPath()}PythonPartsExampleScripts\n\n" +\
                                                 "Make sure, you don't keep any personal files in these locations. " +\
                                                 "Do you want to proceed?", AllplanUtil.MB_YESNO)

        if proceed != AllplanUtil.IDNO:
            GithubUtil.delete_folder()

            try:
                GithubUtil.download_github_repo_as_zip(owner, repo, branch)

            except Exception as e:
                print(f"Encountered the following issue {e}")

            if new_sha:
                with open(sha_file, encoding="UTF-8", mode="w") as f:
                    f.write(new_sha)

            AllplanUtil.ShowMessageBox("Download completed successfully. The examples can be accessed in\n\n" \
                                       "Library -> Private -> Examples -> PythonParts.", AllplanUtil.MB_OK)
