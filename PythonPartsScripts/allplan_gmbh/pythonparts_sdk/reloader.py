# Python Module Reloader
#
# Copyright (c) 2009-2015 Jon Parise <jon@indelible.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Python Module Reloader"""

# pylint: disable=global-statement
# pylint: disable=redefined-builtin

from typing import Set, Dict, Mapping, Sequence, List, Any

from types import ModuleType

import builtins
import importlib
import sys
import types

__author__ = 'Jon Parise <jon@indelible.org>'

_baseimport   = builtins.__import__
_BLACKLIST    = None
_PARENT       = None

_NAME_MODNAME : Dict[str, str]       = {}
_DEPENDENCIES : Dict[str, List[Any]] = {}
_VISITED      : Set[str]             = set()

# PEP 328 changed the default level to 0 in Python 3.3.
_DEFAULT_LEVEL = -1 if sys.version_info < (3, 3) else 0

def enable(blacklist=None):
    """Enable global module dependency tracking.

    A blacklist can be specified to exclude specific modules (and their import
    hierarchies) from the reloading process.  The blacklist can be any iterable
    listing the fully-qualified names of modules that should be ignored.  Note
    that blacklisted modules will still appear in the dependency graph; they
    will just not be reloaded.
    """

    global _BLACKLIST

    builtins.__import__ = _import

    if blacklist is not None:
        _BLACKLIST = frozenset(blacklist)


def disable():
    """Disable global module dependency tracking."""

    global _BLACKLIST, _PARENT

    builtins.__import__ = _baseimport
    _BLACKLIST          = None

    _DEPENDENCIES.clear()

    _PARENT = None


def clear_visited():
    """ clear the visited module list
    """

    _VISITED.clear()


def _reload(mod: ModuleType) -> ModuleType:
    """ Internal module reloading routine.

    Args:
        mod: module to reload

    Returns:
        reloaded module
    """

    mod_name = mod.__name__

    # If this module's name appears in our blacklist, skip its entire dependency hierarchy.

    if _BLACKLIST and mod_name in _BLACKLIST:
        return mod

    # Start by adding this module to our set of _VISITED modules.  We use this
    # set to avoid running into infinite recursion while walking the module
    # dependency graph.

    _VISITED.add(str(mod))

    # Start by reloading all of our dependencies in reverse order.  Note that
    # we recursively call ourself to perform the nested reloads.

    name = _NAME_MODNAME.get(mod_name)

    if name is not None and (deps := _DEPENDENCIES.get(name, None)) is not None or \
                            (deps := _DEPENDENCIES.get(mod_name, None)) is not None:
        for dep in reversed(deps):
            if str(dep) not in _VISITED:
                _reload(dep)

    # Clear this module's list of dependencies.  Some import statements may
    # have been removed.  We'll rebuild the dependency list as part of the
    # reload operation below.

    if name in _DEPENDENCIES:
        del _DEPENDENCIES[name]

    if mod_name in _NAME_MODNAME:
        del _NAME_MODNAME[mod_name]

    # Because we're triggering a reload and not an import, the module itself
    # won't run through our _import hook below.  In order for this module's
    # dependencies (which will pass through the _import hook) to be associated
    # with this module, we need to set our parent pointer beforehand.

    global _PARENT

    _PARENT = mod_name

    callback = getattr(mod, '__reload__', None)

    if callback is not None:
        script = callback(mod)
    else:
        script = importlib.reload(mod)

    # Reset our parent pointer now that the reloading operation is complete.
    _PARENT = None

    return script


def reload(mod: ModuleType) -> ModuleType:
    """ Reload an existing module.

    Any known dependencies of the module will also be reloaded.

    If a module has a __reload__(d) function, it will be called with a copy of
    the original module's dictionary after the module is reloaded.

    Args:
        mod: module to reload

    Returns:
        reloaded module
    """

    if mod in _VISITED:
        return mod

    return _reload(mod)


def _import(name    : str,
            globals : Mapping[str, object]  = None,
            locals  : Mapping[str, object] = None,
            fromlist: Sequence[str] = None,
            level   : int= _DEFAULT_LEVEL):
    """ __import__() replacement function that tracks module dependencies.

    Args:
        name:     name of the module
        globals:  globals of the module
        locals:   locals of the module
        fromlist: from list
        level:    level
    """
    # Track our current parent module.  This is used to find our current place
    # in the dependency graph.

    global _PARENT

    parent  = _PARENT
    _PARENT = name

    # Perform the actual import work using the base import function.

    base = _baseimport(name, globals, locals, fromlist, level)

    if base is not None and parent is not None:
        mod = base

        # We manually walk through the imported hierarchy because the import
        # function only returns the top-level package reference for a nested
        # import statement (e.g. 'package' for `import package.module`) when
        # no from_list has been specified.  It's possible that the package
        # might not have all of its descendants as attributes, in which case
        # we fall back to using the immediate ancestor of the module instead.

        if fromlist is None:
            for component in name.split('.')[1:]:
                try:
                    mod = getattr(mod, component)
                except AttributeError:
                    mod = sys.modules[mod.__name__ + '.' + component]

        # If this is a nested import for a reload able (source-based) module,
        # we append ourself to our parent's dependency list.

        if hasattr(mod, '__file__'):
            str_m = str(mod)


            #------------- normal import

            if str_m.endswith(".py'>"):
                if "\\\\Prg\\\\Python\\\\"     not in str_m and \
                   "PythonParts-site-packages" not in str_m:
                    mod_list = _DEPENDENCIES.setdefault(parent, [])
                    mod_list.append(mod)

                    _NAME_MODNAME[mod.__name__] = name


            #------------- relative import with "from .import xxx"

            elif str_m.startswith("<module") and str_m.endswith(" (namespace)>"):
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name, None)

                    if isinstance(attr, types.ModuleType):
                        for item in fromlist:
                            if attr.__name__.endswith("." + item):
                                mod_list = _DEPENDENCIES.setdefault(parent, [])
                                mod_list.append(attr)

                                _NAME_MODNAME[attr.__name__] = item

    # Lastly, we always restore our global _parent pointer.
    _PARENT = parent

    return base
