from typing import Tuple

def _cmd_with_args(cmd: str, **kwargs) -> str:
    result = f"{cmd:<9} "
    keys = kwargs.keys()
    for i in range(len(keys)):
        if (i == 0):
            result += "   "
        else:
            result += ", "

        k = keys[i]
        result += f"{k}={hex(kwargs[k])}"
    return result

def decode(command: int) -> Tuple[int, str]:
    in_vif = True
    command_str = hex(command)
    COMMAND_PREFIX = "[VIF] "

    i = command >> 31
    i_prefix = "i" if i else ""
    cmd = (command >> 24) & 0x7F
    num = (command >> 16) & 0xFF
    imm = command & 0xFFFF

    match cmd:
        case 0b0000000:
            command_str = "NOP"
        case 0b0000001:
            command_str = "STCYCL"
            wl = imm >> 8
            cl = imm & 0xFF
            command_str = _cmd_with_args(command_str, {"WL": wl, "CL": cl})
        case 0b0000010:
            command_str = "OFFSET"
            val = imm & 0x3F
            command_str = _cmd_with_args(command_str, {"VAL": val})
        case 0b0000011:
            command_str = "BASE"
        case 0b0000100:
            command_str = "ITOP"
        case 0b0000101:
            command_str = "STMOD"
        case 0b0000110:
            command_str = "MSKPATH3"
        case 0b0000111:
            command_str = "MARK"
        case 0b0010000:
            command_str = "FLUSHE"
        case 0b0010001:
            command_str = "FLUSH"
        case 0b0010011:
            command_str = "FLUSHA"
        case 0b0010100:
            command_str = "MSCAL"
        case 0b0010111:
            command_str = "MSCNT"
        case 0b0010101:
            command_str = "MSCALF"
        case 0b0100000:
            command_str = "STMASK"
        case 0b0110000:
            command_str = "STROW"
        case 0b0110001:
            command_str = "STCOL"

    return (in_vif, COMMAND_PREFIX + i_prefix + command_str)