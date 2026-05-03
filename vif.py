import struct
from typing import List, Tuple
from lower import decode as lower_decode
from prefixes import PREFIXES
from upper import decode as upper_decode

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

def _decode_mpg(buf: bytes, start_idx: int, num: int, pc: int) -> Tuple[int, List[str]]:
    strings = []
    for i in range(num):
        idx = start_idx + i * 8
        lower = struct.unpack("<I", buf[idx+0:idx+4])[0]
        upper = struct.unpack("<I", buf[idx+4:idx+8])[0]
        i_bit, upper_str = upper_decode(upper)

        # Representation of lower changes depending on if upper command has I bit set
        if i_bit:
            # Interpret lower as float moved into I register
            lower_float = struct.unpack("<f", buf[idx+0:idx+4])[0]
            strings.append(f"{{0:<8}} (Move {lower_float} ({hex(lower)}) into I Register)".format(PREFIXES.VU_LOWER))
        else:
            strings.append(lower_decode(lower, pc))
        strings.append(upper_str)

        pc += 0x8
        
    return num * 0x8, strings

def decode(buf: bytes, start_idx: int, pc: int) -> Tuple[int, List[str]]:
    COMMAND_PREFIX = PREFIXES.VIF
    command = struct.unpack("<I", buf[start_idx:start_idx+4])[0]
    i = command >> 31
    i_prefix = "i" if i else ""
    cmd = (command >> 24) & 0x7F
    num = (command >> 16) & 0xFF
    imm = command & 0xFFFF

    match cmd:
        case 0b0000000:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}NOP"]
        case 0b0000001:
            wl = imm >> 8
            cl = imm & 0xFF
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("STCYCL", {"WL": wl, "CL": cl})}"]
        case 0b0000010:
            val = imm & 0x3F
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("OFFSET", {"VAL": val})}"]
        case 0b0000011:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("BASE")}"]
        case 0b0000100:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("ITOP")}"]
        case 0b0000101:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("STMOD")}"]
        case 0b0000110:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MSKPATH3")}"]
        case 0b0000111:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MARK")}"]
        case 0b0010000:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("FLUSHE")}"]
        case 0b0010001:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("FLUSH")}"]
        case 0b0010011:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("FLUSHA")}"]
        case 0b0010100:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MSCAL")}"]
        case 0b0010111:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MSCNT")}"]
        case 0b0010101:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MSCALF")}"]
        case 0b0100000:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("STMASK")}"]
        case 0b0110000:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("STROW")}"]
        case 0b0110001:
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("STCOL")}"]
        case 0b1001010:
            if (num == 0): num = 256
            load_addr = imm * 0x8

            cmd_size = 4
            cmd_str = [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("MPG", {"SIZE": num * 0x8, "LOADADDR": load_addr})}"]

            size, strings = _decode_mpg(buf, start_idx+4, num, pc+4)
            cmd_str.extend(strings)
            return cmd_size+size, cmd_str
        case 0b1010000:
            # TODO: Consume subpacket
            print("WARNING: [VIF] DIRECT encountered but consuming subpacket unimplemented")
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("DIRECT")}"]
        case 0b1010001:
            # TODO: Consume subpacket
            print("WARNING: [VIF] DIRECTHL encountered but consuming subpacket unimplemented")
            return 4, [f"{COMMAND_PREFIX}{i_prefix}{_cmd_with_args("DIRECTHL")}"]
        
    if (cmd & 0x60) == 0x60:
        # TODO: Consume subpacket
        print("WARNING: [VIF] UNPACK encountered but consuming subpacket unimplemented")
        return 4, [f"{COMMAND_PREFIX}{i_prefix}UNPACK"]

    print(f"WARNING: Encountered unknown VIF command: {hex(command)}")
    return 4, [hex(command)]
