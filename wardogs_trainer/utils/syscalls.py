import ctypes
from ctypes import wintypes

ntdll = ctypes.WinDLL("ntdll", use_last_error=True)

_nt_write = ntdll.NtWriteVirtualMemory
_nt_write.restype = wintypes.LONG
_nt_write.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.LPCVOID,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t),
]


def nt_write(handle: int, address: int, data: bytes) -> bool:
    written = ctypes.c_size_t(0)
    status = _nt_write(
        handle,
        wintypes.LPVOID(address),
        data,
        len(data),
        ctypes.byref(written),
    )
    return status == 0 and written.value == len(data)