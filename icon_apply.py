"""
Contains logic of applying icon to a folder.
Title: How to change folder icons with Python on windows?
Author: cgohlke
Date: 01/12/2011
URL: https://stackoverflow.com/questions/4662759/how-to-change-folder-icons-with-python-on-windows
"""

import os
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR
import win32api

HICON = c_int
LPTSTR = LPWSTR
TCHAR = c_wchar
MAX_PATH = 260
FCSM_ICON_FILE = 0x00000010
FCS_FORCE_WRITE = 0x00000002
SHGFI_ICON_LOCATION = 0x000001000


class GUID(Structure):
    """
    Structure definition.
    See https://docs.python.org/3/library/ctypes.html#structures-and-unions
    """

    _fields_ = [("Data1", DWORD), ("Data2", WORD), ("Data3", WORD), ("Data4", BYTE * 8)]


class SHFolderCustomSettings(Structure):
    """
    Structure definition.
    """

    _fields_ = [
        ("dw_size", DWORD),
        ("dw_mask", DWORD),
        ("pvid", POINTER(GUID)),
        ("pszWebViewTemplate", LPTSTR),
        ("cchWebViewTemplate", DWORD),
        ("pszWebViewTemplateVersion", LPTSTR),
        ("pszInfoTip", LPTSTR),
        ("cchInfoTip", DWORD),
        ("pclsid", POINTER(GUID)),
        ("dwFlags", DWORD),
        ("psz_icon_file", LPTSTR),
        ("cch_icon_file", DWORD),
        ("i_icon_index", c_int),
        ("pszLogo", LPTSTR),
        ("cchLogo", DWORD),
    ]


class SHFileInfo(Structure):
    """
    Structure definition.
    """

    _fields_ = [
        ("hIcon", HICON),
        ("iIcon", c_int),
        ("dwAttributes", DWORD),
        ("szDisplayName", TCHAR * MAX_PATH),
        ("szTypeName", TCHAR * 80),
    ]


def set_icon(folder_path, icon_path, icon_index):
    """
    Applies 'icon_path' to 'folder_path'
    :param folder_path:
    :param icon_path:
    :param icon_index:
    :return:
    """

    shell32 = ctypes.windll.shell32

    folder_path = str(os.path.abspath(folder_path))
    icon_path = str(os.path.abspath(icon_path))

    fcs = SHFolderCustomSettings()
    fcs.dw_size = sizeof(fcs)
    fcs.dw_mask = FCSM_ICON_FILE
    fcs.psz_icon_file = icon_path
    fcs.cch_icon_file = 0
    fcs.i_icon_index = icon_index

    gs_fcs = shell32.SHGetSetFolderCustomSettings(byref(fcs), folder_path, FCS_FORCE_WRITE)
    if gs_fcs:
        raise WindowsError(win32api.FormatMessage(gs_fcs))

    sfi = SHFileInfo()
    gs_fcs = shell32.SHGetFileInfoW(folder_path, 0, byref(sfi), sizeof(sfi), SHGFI_ICON_LOCATION)
    if gs_fcs == 0:
        raise WindowsError(win32api.FormatMessage(gs_fcs))

    index = shell32.Shell_GetCachedImageIndexW(sfi.szDisplayName, sfi.iIcon, 0)
    if index == -1:
        raise WindowsError()

    shell32.SHUpdateImageW(sfi.szDisplayName, sfi.iIcon, 0, index)
