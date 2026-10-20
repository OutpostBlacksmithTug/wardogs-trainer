import ctypes
import struct


class MemoryReaderWriter:
    def __init__(self, handle: int):
        self.handle = handle
        self.k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.base_address = self._module_base()

    def _module_base(self) -> int:
        return 0x140000000  # default Unity IL2CPP base; overridden by build detection

    def read(self, address: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        read = ctypes.c_size_t(0)
        ok = self.k32.ReadProcessMemory(
            self.handle, ctypes.c_void_p(address), buf, size, ctypes.byref(read)
        )
        if not ok:
            raise OSError(f"ReadProcessMemory @0x{address:X} failed")
        return buf.raw[: read.value]

    def write(self, address: int, data: bytes) -> None:
        written = ctypes.c_size_t(0)
        ok = self.k32.WriteProcessMemory(
            self.handle,
            ctypes.c_void_p(address),
            data,
            len(data),
            ctypes.byref(written),
        )
        if not ok:
            raise OSError(f"WriteProcessMemory @0x{address:X} failed")

    def read_int32(self, address: int) -> int:
        return struct.unpack("<i", self.read(address, 4))[0]

    def read_float(self, address: int) -> float:
        return struct.unpack("<f", self.read(address, 4))[0]

    def write_float(self, address: int, value: float) -> None:
        self.write(address, struct.pack("<f", value))

    def write_int32(self, address: int, value: int) -> None:
        self.write(address, struct.pack("<i", value))