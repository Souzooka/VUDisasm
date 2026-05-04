from __future__ import annotations
import struct
from typing import List, Tuple, TYPE_CHECKING
from command import CommandVIF, CommandVU
from lower import decode as lower_decode
from prefixes import PREFIXES
from upper import decode as upper_decode

if TYPE_CHECKING:
    from vif_packet import VIFPacketIR

def _cmd_with_args(cmd: str, kwargs={}) -> str:
    result = f"{cmd:<9} "
    keys = kwargs.keys()
    for i, k in enumerate(keys):
        if (i == 0):
            result += "   "
        else:
            result += ", "

        result += f"{k}={hex(kwargs[k])}"
    return result

def _decode_mpg(ir: VIFPacketIR, buf: bytes, start_idx: int, num: int, pc: int) -> int:
    # Presume start of MPG is probably a subroutine
    label = ir.get_or_new_label(pc)
    label.set_type(label.BAL)

    strings = []
    for i in range(num):
        command = CommandVU(pc)
        ir.add_command(command)

        idx = start_idx + i * 8
        lower = struct.unpack("<I", buf[idx+0:idx+4])[0]
        upper = struct.unpack("<I", buf[idx+4:idx+8])[0]
        upper_decode(ir, command.upper, upper)
        i_bit = command.upper.i_flag

        # Representation of lower changes depending on if upper command has I bit set
        if i_bit:
            # Interpret lower as float moved into I register
            lower_float = struct.unpack("<f", buf[idx+0:idx+4])[0]
            strings.append(f"(Move {lower_float} ({hex(lower)}) into I Register)".format(PREFIXES.VU_LOWER))
        else:
            strings.append(lower_decode(ir, command.lower, lower, pc))
        #strings.append(upper_str)

        pc += 0x8
        
    return num * 0x8

def decode(ir: VIFPacketIR, buf: bytes, start_idx: int, pc: int) -> int:
    COMMAND_PREFIX = PREFIXES.VIF
    command = struct.unpack("<I", buf[start_idx:start_idx+4])[0]
    i = command >> 31
    cmd = (command >> 24) & 0x7F
    num = (command >> 16) & 0xFF
    imm = command & 0xFFFF

    command_ir = CommandVIF(pc)
    command_ir.interrupt = bool(i)
    ir.add_command(command_ir)
    size = 4

    match cmd:
        case 0b0000000:
            # NOP
            command_ir.mnemonic = "NOP"
        case 0b0000001:
            # STCYCL
            command_ir.mnemonic = "STCYCL"
            wl = imm >> 8
            cl = imm & 0xFF
            command_ir.kwargs = {"WL": wl, "CL": cl}
        case 0b0000010:
            # OFFSET
            command_ir.mnemonic = "OFFSET"
            val = imm & 0x3F
            command_ir.kwargs = {"VAL": val}
        case 0b0000011:
            # BASE
            # TODO: kwargs
            command_ir.mnemonic = "BASE"
        case 0b0000100:
            # ITOP
            # TODO: kwargs
            command_ir.mnemonic = "ITOP"
        case 0b0000101:
            # STMOD
            # TODO: kwargs
            command_ir.mnemonic = "STMOD"
        case 0b0000110:
            # MSKPATH3
            # TODO: kwargs
            command_ir.mnemonic = "MSKPATH3"
        case 0b0000111:
            # MARK
            # TODO: kwargs
            command_ir.mnemonic = "MARK"
        case 0b0010000:
            # FLUSHE
            # TODO: kwargs
            command_ir.mnemonic = "FLUSHE"
        case 0b0010001:
            # FLUSH
            # TODO: kwargs
            command_ir.mnemonic = "FLUSH"
        case 0b0010011:
            # FLUSHA
            # TODO: kwargs
            command_ir.mnemonic = "FLUSHA"
        case 0b0010100:
            # MSCAL
            # TODO: kwargs
            command_ir.mnemonic = "MSCAL"
        case 0b0010111:
            # MSCNT
            # TODO: kwargs
            command_ir.mnemonic = "MSCNT"
        case 0b0010101:
            # MSCALF
            # TODO: kwargs
            command_ir.mnemonic = "MSCALF"
        case 0b0100000:
            # STMASK
            # TODO: kwargs
            command_ir.mnemonic = "STMASK"
        case 0b0110000:
            # STROW
            # TODO: kwargs
            command_ir.mnemonic = "STROW"
        case 0b0110001:
            # STCOL
            # TODO: kwargs
            command_ir.mnemonic = "STCOL"
        case 0b1001010:
            # MPG
            command_ir.mnemonic = "MPG"
            if (num == 0): num = 256
            load_addr = imm * 0x8
            command_ir.kwargs = {"SIZE": num * 0x8, "LOADADDR": load_addr}

            cmd_size = 4
            size = cmd_size + _decode_mpg(ir, buf, start_idx+4, num, pc+4)
        case 0b1010000:
            # TODO: Consume subpacket
            print("WARNING: [VIF] DIRECT encountered but consuming subpacket unimplemented")
            command_ir.mnemonic = "DIRECT"
        case 0b1010001:
            # TODO: Consume subpacket
            print("WARNING: [VIF] DIRECTHL encountered but consuming subpacket unimplemented")
            command_ir.mnemonic = "DIRECTHL"
        
    if (cmd & 0x60) == 0x60:
        # TODO: Consume subpacket
        print("WARNING: [VIF] UNPACK encountered but consuming subpacket unimplemented")
        command_ir.mnemonic = "UNPACK"

    if len(command_ir.mnemonic) == 0:
        print(f"WARNING: Encountered unknown VIF command: {hex(command)}")
        command_ir.mnemonic = f"[UNKNOWN VIF COMMAND] {hex(command)}"

    return size
