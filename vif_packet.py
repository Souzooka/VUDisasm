import struct
from typing import List
from vif import decode as vif_decode

# Assumes DMATag (Source Chain Tag) is included
class VIFPacket:
    @classmethod
    def from_file(cls, f):
        packet = cls()
        pos = f.tell()

        f.seek(pos + 0x0)
        packet.size = ((struct.unpack("<I", f.read(4))[0] & 0x3FF) + 1) * 0x10
        f.seek(pos + 0x0)
        packet.buf = f.read(packet.size)
        
        f.seek(pos)

        return packet

    def decode(self) -> List[str]:
        DMA_IDS = ["refe", "cnt", "next", "ref", "refs", "call", "ret", "end"]
        COMMAND_PREFIX = f"{"[DMAC]":<8}"
        operations = []

        # First 8 bytes are DMATag and ADDR
        word = struct.unpack("<I", self.buf[0:4])[0]
        operations.append(f"{COMMAND_PREFIX}{DMA_IDS[(word >> 28) & 0x7]} {hex(self.size)}")
        operations.append(f"{COMMAND_PREFIX}{hex(struct.unpack("<I", self.buf[4:8])[0])}")

        # Now we should start running into VIFCode
        i = 8
        while i < self.size:
            size, strings = vif_decode(self.buf, i)
            i += size
            operations.extend(strings)
        
        return operations
