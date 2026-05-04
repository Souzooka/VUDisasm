from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

if TYPE_CHECKING:
    from command import CommandVU
    from vif_packet import VIFPacketIR

# TODO: probably put this in another file because it's gonna get copied in lower
MNEMONIC_SIZE = 15
REG_SIZE = 10
COMMAND_PREFIX = PREFIXES.VU_UPPER

def _field_0(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> None:
    # Ex: {ADD}{x}.{xyzw} {VF10}{xyzw} {VF20}{xyzw} {VF30}{x}

    upper_ir.mnemonic = mnemonic
    upper_ir.mnemonic_fmt = "{mnemonic}{bc}.{dest}"
    upper_ir.bc = command & 0x3
    upper_ir.regs[0].r = (command >> 6) & 0x1F
    upper_ir.regs[0].type = FloatRegister
    upper_ir.regs[0].fmt = "{r}{dest}"
    upper_ir.regs[1].r = (command >> 11) & 0x1F
    upper_ir.regs[1].type = FloatRegister
    upper_ir.regs[1].fmt = "{r}{dest}"
    upper_ir.regs[2].r = (command >> 16) & 0x1F
    upper_ir.regs[2].type = FloatRegister
    upper_ir.regs[2].fmt = "{r}{bc}"
    upper_ir.dest = (command >> 21) & 0xF

def _field_1(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> str:
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

    if (mnemonic[-1] == 'i'): ft_s = FloatRegister.I
    if (mnemonic[-1] == 'q'): ft_s = FloatRegister.Q

    command_s = FORMAT.format(mnemonic_s, fd_s, fs_s, ft_s)
    return command_s

def _field_2(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> str:
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

def _field_3(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> str:
    has_i = mnemonic.endswith("i")
    has_q = mnemonic.endswith("q")
    has_acc_dest = mnemonic.endswith("A") or has_i or has_q
    
    r1 = FloatRegister.get_register((command >> 11) & 0x1F) # fs
    r2 = FloatRegister.get_register((command >> 16) & 0x1F) # ft
    r3 = None
    dest = FloatRegister.get_dest((command >> 21) & 0xF)

    # Field type 3 has a bunch of odd edgecases to account for
    if mnemonic == "NOP":
        return "NOP"
    if mnemonic == "CLIP":
        return f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:}}".format("CLIPw.xyz", r1 + "xyz,", r2 + "w")
    if mnemonic == "OPMULA":
        return f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3}}".format("OPMULA.xyz", FloatRegister.ACC + "xyz,", r1 + "xyz,", r2 + "xyz")

    if has_acc_dest:
        r1, r2, r3 = FloatRegister.ACC, r1, r2
        if has_i: r3 = FloatRegister.I
        if has_q: r3 = FloatRegister.Q

    # Swap fs, ft to ft, fs for these operations
    SWAP_LIST = ["ABS", "FTOI0", "FTOI4", "FTOI12", "FTOI15", "ITOF0", "ITOF4", "ITOF12", "ITOF15",]
    if mnemonic in SWAP_LIST:
        r1, r2 = r2, r1

    command_s = ""
    command_s += f"{{0:<{MNEMONIC_SIZE}}} ".format(mnemonic + "." + dest)
    command_s += f"{{0:<{REG_SIZE}}} ".format(r1 + dest + ",")
    command_s += f"{{0:<{REG_SIZE}}} ".format(r2 + dest + ("," if r3 is not None else ""))
    if r3 is not None:
        command_s += f"{{0:<{REG_SIZE}}}".format(r3 + (dest if not has_i and not has_q else ""))
    return command_s

FIELD_0_TABLE = {
    0b0000: "ADD",
    0b0010: "MADD",
    0b0100: "MAX",
    0b0101: "MINI",
    0b0011: "MSUB",
    0b0110: "MUL",
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
    0b00000_1111: "ADDA",
    0b00010_1111: "MADDA",
    0b00011_1111: "MSUBA",
    0b00110_1111: "MULA",
    0b00001_1111: "SUBA",
}
FIELD_3_TABLE = {
    0b00111_1111_01: "ABS",
    0b01010_1111_00: "ADDA",
    0b01000_1111_00: "ADDAi",
    0b01000_1111_00: "ADDAq",
    0b00111_1111_11: "CLIP",
    0b00101_1111_00: "FTOI0",
    0b00101_1111_01: "FTOI4",
    0b00101_1111_10: "FTOI12",
    0b00101_1111_11: "FTOI15",
    0b00100_1111_00: "ITOF0",
    0b00100_1111_01: "ITOF4",
    0b00100_1111_10: "ITOF12",
    0b00100_1111_11: "ITOF15",
    0b01010_1111_01: "MADDA",
    0b01000_1111_11: "MADDAi",
    0b01000_1111_01: "MADDAq",
    0b01011_1111_01: "MSUBA",
    0b01001_1111_11: "MSUBAi",
    0b01001_1111_01: "MSUBAq",
    0b01010_1111_10: "MULA",
    0b00111_1111_10: "MULAi",
    0b00111_1111_00: "MULAq",
    0b01011_1111_11: "NOP",
    0b01011_1111_10: "OPMULA",
    0b01011_1111_00: "SUBA",
    0b01001_1111_10: "SUBAi",
    0b01001_1111_00: "SUBAq",
}
FIELDS = [
    (FIELD_0_TABLE, lambda cmd: (cmd >> 2) & 0xF, _field_0),
    (FIELD_1_TABLE, lambda cmd: (cmd & 0x3F), _field_1),
    (FIELD_2_TABLE, lambda cmd: (cmd >> 2) & 0x1FF, _field_2),
    (FIELD_3_TABLE, lambda cmd: (cmd & 0x7FF), _field_3)
]

def decode(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, command: int) -> Tuple[bool, str]:
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
            return i_bit, COMMAND_PREFIX + (format_fn(ir, upper_ir, mnemonic, command) or "")

    print(f"WARNING: Unrecognized VU Upper command: 0x{hex(command)[2:].upper().zfill(8)} ({bin(command)[2:].zfill(32)})")
    return i_bit, COMMAND_PREFIX + hex(command)

