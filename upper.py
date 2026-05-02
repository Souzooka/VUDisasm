from typing import Tuple
from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

# TODO: probably put this in another file because it's gonna get copied in lower
MNEMONIC_SIZE = 15
REG_SIZE = 10
COMMAND_PREFIX = PREFIXES.VU

def _field_0(mnemonic: str, command: int) -> str:
    # Ex: {ADD}{x}.{xyzw} {VF10}{xyzw} {VF20}{xyzw} {VF30}{x}
    MNEMONIC_FORMAT = "{0}{1}.{2}"
    FD_FORMAT = "{0}{1},"
    FS_FORMAT = "{0}{1},"
    FT_FORMAT = "{0}{1}"
    FORMAT = f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3}}"

    bc = FloatRegister.get_bc(command & 0x3)
    fd = FloatRegister.get_register((command >> 6) & 0x1F)
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    dest = FloatRegister.get_dest((command >> 21) & 0xF)

    mnemonic_s = MNEMONIC_FORMAT.format(mnemonic, bc, dest)
    fd_s = FD_FORMAT.format(fd, dest)
    fs_s = FS_FORMAT.format(fs, dest)
    ft_s = FT_FORMAT.format(ft, dest)

    return FORMAT.format(mnemonic_s, fd_s, fs_s, ft_s)

def _field_1(mnemonic: str, command: int) -> str:
    # Ex: {ADD}.{xyzw} {VF10}{xyzw} {VF20}{xyzw} {VF30}{xyzw}
    MNEMONIC_FORMAT = "{0}.{1}"
    FD_FORMAT = "{0}{1},"
    FS_FORMAT = "{0}{1},"
    FT_FORMAT = "{0}{1}"
    FORMAT = f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3}}"

    fd = FloatRegister.get_register((command >> 6) & 0x1F)
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    dest = FloatRegister.get_dest((command >> 21) & 0xF)

    mnemonic_s = MNEMONIC_FORMAT.format(mnemonic, dest)
    fd_s = FD_FORMAT.format(fd, dest)
    fs_s = FS_FORMAT.format(fs, dest)
    ft_s = FT_FORMAT.format(ft, dest)

    command_s = FORMAT.format(mnemonic_s, fd_s, fs_s, ft_s)
    if (mnemonic[-1] == 'i'): command_s += ", I"
    if (mnemonic[-1] == 'q'): command_s += ", Q"
    return command_s

def _field_2(mnemonic: str, command: int) -> str:
    # Ex: {ADDA}{x}.{xyzw} {ACC}{xyzw} {VF20}{xyzw} {VF30}{x}
    MNEMONIC_FORMAT = "{0}{1}.{2}"
    FD_FORMAT = "{0}{1},"
    FS_FORMAT = "{0}{1},"
    FT_FORMAT = "{0}{1}"
    FORMAT = f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3}}"

    bc = FloatRegister.get_bc(command & 0x3)
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    dest = FloatRegister.get_dest((command >> 21) & 0xF)

    mnemonic_s = MNEMONIC_FORMAT.format(mnemonic, bc, dest)
    fd_s = FD_FORMAT.format(FloatRegister.ACC, dest)
    fs_s = FS_FORMAT.format(fs, dest)
    ft_s = FT_FORMAT.format(ft, bc)

    return FORMAT.format(mnemonic_s, fd_s, fs_s, ft_s)

def _field_3(mnemonic: str, command: int) -> str:
    return ""

FIELD_0_TABLE = {
    0b0000: "ADD",
    0b0010: "MADD",
    0b0100: "MAX",
    0b0101: "MINI",
    0b0011: "MSUB",
    0b0001: "SUB",
}
FIELD_1_TABLE = {
    0b101000: "ADD",
    0b100010: "ADDi",
    0b100000: "ADDq",
    0b101001: "MADD",
    0b100011: "MADDi",
    0b100001: "MADDq",
    0b101011: "MAX",
    0b011101: "MAXi",
    0b101111: "MINI",
    0b011111: "MINIi",
    0b101101: "MSUB",
    0b100111: "MSUBi",
    0b100101: "MSUBq",
    0b101010: "MUL",
    0b011110: "MULi",
    0b011100: "MULq",
    0b101110: "OPMSUB",
    0b101100: "SUB",
    0b100110: "SUBi",
    0b100100: "SUBq",
}
FIELD_2_TABLE = {
    0b000001111: "ADDA",
    0b000101111: "MADDA",
    0b000111111: "MSUBA",
    0b001101111: "MULA",
    0b000011111: "SUBA",
}
FIELD_3_TABLE = {

}
FIELDS = [
    (FIELD_0_TABLE, lambda cmd: (cmd >> 2) & 0xF, _field_0),
    (FIELD_1_TABLE, lambda cmd: (cmd & 0x3F), _field_1),
    (FIELD_2_TABLE, lambda cmd: (cmd >> 2) & 0x1FF, _field_2),
    (FIELD_3_TABLE, lambda cmd: (cmd & 0x7FF), _field_3)
]

def decode(command: int) -> Tuple[bool, str]:
    # Returns (i_bit, command_string)
    # the I bit indicates that lower should be copied into the I register
    # (lower is interpreted as a single-precision scalar)
    i_bit = bool(command >> 31)

    if (command == 0x0):
        # probably alignment
        return False, COMMAND_PREFIX + "<ALIGN>"
    
    for table, extract_fn, format_fn in FIELDS:
        cmd = extract_fn(command)
        if (mnemonic := table.get(cmd, None)) is not None:
            return i_bit, COMMAND_PREFIX + format_fn(mnemonic, command)

    return i_bit, COMMAND_PREFIX + hex(command)

