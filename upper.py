from typing import Tuple
from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

# TODO: probably put this in another file because it's gonna get copied in lower
MNEMONIC_SIZE = 15
REG_SIZE = 10

def _field_0(mnemonic: str, command: int) -> Tuple[bool, str]:
    # Ex: {ADD}{x}.{xyzw} {VF10}{xyzw} {VF20}{xyzw} {VF30}{x}
    MNEMONIC_FORMAT = "{0}{1}.{2}"
    FD_FORMAT = "{0}{1}"
    FS_FORMAT = "{0}{1}"
    FT_FORMAT = "{0}{1}"
    FORMAT = f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3:<{REG_SIZE}}}"

    i_bit = bool(command >> 31)
    bc = FloatRegister.get_bc(command & 0x3)
    fd = FloatRegister.get_register((command >> 6) & 0x1F)
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    dest = FloatRegister.get_dest((command >> 21) & 0xF)

    mnemonic_s = MNEMONIC_FORMAT.format(mnemonic, bc, dest)
    fd_s = FD_FORMAT.format(fd, dest)
    fs_s = FS_FORMAT.format(fs, dest)
    ft_s = FT_FORMAT.format(ft, dest)

    return i_bit, FORMAT.format(mnemonic_s, fd_s, fs_s, ft_s)

def decode(command: int) -> Tuple[bool, str]:
    # Returns (i_bit, command_string)
    # the I bit indicates that lower should be copied into the I register
    # (lower is interpreted as a single-precision scalar)
    COMMAND_PREFIX = PREFIXES.VU

    if (command == 0x0):
        # probably alignment
        return False, COMMAND_PREFIX + "<ALIGN>"
    
    # Field type 0
    cmd = (command >> 2) & 0xF
    match cmd:
        case 0b0000:
            # ADDbc
            i_bit, command_str = _field_0("ADD", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0010:
            # MADDbc
            i_bit, command_str = _field_0("MADD", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0100:
            # MAXbc
            i_bit, command_str = _field_0("MAX", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0101:
            # MINIbc
            i_bit, command_str = _field_0("MINI", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0011:
            # MSUBbc
            i_bit, command_str = _field_0("MSUB", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0110:
            # MULbc
            i_bit, command_str = _field_0("MUL", command)
            return i_bit, COMMAND_PREFIX + command_str
        case 0b0001:
            # SUBbc
            i_bit, command_str = _field_0("SUB", command)
            return i_bit, COMMAND_PREFIX + command_str

    return False, COMMAND_PREFIX + hex(command)

