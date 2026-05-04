from __future__ import annotations
import struct
from typing import List, Set
from command import CommandIR, CommandDMAC, CommandVIF
from prefixes import PREFIXES
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

    def decode(self, pc: int) -> VIFPacketIR:
        DMA_IDS = ["refe", "cnt", "next", "ref", "refs", "call", "ret", "end"]

        ir = VIFPacketIR()

        # First 8 bytes are DMATag and ADDR
        dma_tag = CommandDMAC(pc)
        dma_tag.pc = pc
        dma_tag.size = self.size
        word = struct.unpack("<I", self.buf[0:4])[0]
        dma_tag.id = (word >> 28) & 0x7
        dma_tag.id_s = DMA_IDS[dma_tag.id]
        addr = struct.unpack("<I", self.buf[4:8])[0]
        dma_tag.addr = addr
        ir.commands.append(dma_tag)

        # Now we should start running into VIFCode
        i = 8
        while i < self.size:
            size = vif_decode(ir, self.buf, i, pc+i)
            i += size
        
        return ir

class VIFPacketIR:
    
    def __init__(self):
        self.labels: Set[int] = set()
        self.commands: List[CommandIR] = []

    def add_command(self, command: CommandIR):
        self.commands.append(command)
