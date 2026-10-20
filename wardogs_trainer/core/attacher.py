import ctypes
import ctypes.wintypes as wt

PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wt.DWORD),
        ("cntUsage", wt.DWORD),
        ("th32ProcessID", wt.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wt.DWORD),
        ("cntThreads", wt.DWORD),
        ("th32ParentProcessID", wt.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wt.DWORD),
        ("szExeFile", ctypes.c_char * 260),
    ]


class ProcessAttacher:
    def __init__(self, process_name: str):
        self.process_name = process_name.encode()
        self.handle: int | None = None
        self.pid: int | None = None

    def _find_pid(self) -> int | None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        entry = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        if kernel32.Process32First(snap, ctypes.byref(entry)):
            while True:
                if entry.szExeFile == self.process_name:
                    pid = entry.th32ProcessID
                    kernel32.CloseHandle(snap)
                    return pid
                if not kernel32.Process32Next(snap, ctypes.byref(entry)):
                    break
        kernel32.CloseHandle(snap)
        return None

    def attach(self, pid: int | None = None) -> None:
        target = pid or self._find_pid()
        if not target:
            raise RuntimeError(f"{self.process_name.decode()} not running")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target)
        if not handle:
            raise RuntimeError(f"OpenProcess failed, err={ctypes.get_last_error()}")
        self.handle = handle
        self.pid = target

    def detach(self) -> None:
        if self.handle:
            ctypes.WinDLL("kernel32").CloseHandle(self.handle)
        self.handle = None
        self.pid = None