"""
Contains logic of applying icon to a folder.
"""
import os
import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR
import win32api

#************************************************************
#* Title: How to change folder icons with Python on windows?
#* Author: cgohlke
#* Date: 01/12/2011
#* URL: https://stackoverflow.com/questions/4662759/how-to
#       -change-folder-icons-with-python-on-windows
#************************************************************
HICON = c_int
LPTSTR = LPWSTR
TCHAR = c_wchar
MAX_PATH = 260
FCSM_ICONFILE = 0x00000010
FCS_FORCEWRITE = 0x00000002
SHGFI_ICONLOCATION = 0x000001000    

# https://docs.python.org/3/library/ctypes.html#structures-and-unions
class GUID(Structure):
    """
    Structure definition.
    """
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8)]

class SHFOLDERCUSTOMSETTINGS(Structure):
    """
    Structure definition.
    """
    _fields_ = [
        ('dw_size', DWORD),
        ('dw_mask', DWORD),
        ('pvid', POINTER(GUID)),
        ('pszWebViewTemplate', LPTSTR),
        ('cchWebViewTemplate', DWORD),
        ('pszWebViewTemplateVersion', LPTSTR),
        ('pszInfoTip', LPTSTR),
        ('cchInfoTip', DWORD),
        ('pclsid', POINTER(GUID)),
        ('dwFlags', DWORD),
        ('psz_icon_file', LPTSTR),
        ('cch_icon_file', DWORD),
        ('i_icon_index', c_int),
        ('pszLogo', LPTSTR),
        ('cchLogo', DWORD)]

class SHFILEINFO(Structure):
    """
    Structure definition.
    """
    _fields_ = [
        ('hIcon', HICON),
        ('iIcon', c_int),
        ('dwAttributes', DWORD),
        ('szDisplayName', TCHAR * MAX_PATH),
        ('szTypeName', TCHAR * 80)]    

def seticon(folderpath, iconpath, iconindex):
    """
    Applies 'iconpath' to 'folderpath'
    """
    shell32 = ctypes.windll.shell32

    folderpath = str(os.path.abspath(folderpath))
    iconpath = str(os.path.abspath(iconpath))

    fcs = SHFOLDERCUSTOMSETTINGS()
    fcs.dw_size = sizeof(fcs)
    fcs.dw_mask = FCSM_ICONFILE
    fcs.psz_icon_file = iconpath
    fcs.cch_icon_file = 0
    fcs.i_icon_index = iconindex

    gs_fcs = shell32.SHGetSetFolderCustomSettings(byref(fcs), \
                                                  folderpath, FCS_FORCEWRITE)
    if gs_fcs:
        raise WindowsError(win32api.FormatMessage(gs_fcs))

    sfi = SHFILEINFO()
    gs_fcs = shell32.SHGetFileInfoW(folderpath, 0, byref(sfi), \
                                    sizeof(sfi), SHGFI_ICONLOCATION)
    if gs_fcs == 0:
        raise WindowsError(win32api.FormatMessage(gs_fcs))

    index = shell32.Shell_GetCachedImageIndexW(sfi.szDisplayName, sfi.iIcon, 0)
    if index == -1:
        raise WindowsError()

    shell32.SHUpdateImageW(sfi.szDisplayName, sfi.iIcon, 0, index)
    