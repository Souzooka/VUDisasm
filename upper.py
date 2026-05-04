from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from prefixes import PREFIXES
from registers import FloatRegister, SpecialRegister

if TYPE_CHECKING:
    from command import CommandVU
    from vif_packet import VIFPacketIR

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

    upper_ir.mnemonic = mnemonic
    upper_ir.mnemonic_fmt = "{mnemonic}.{dest}"
    upper_ir.regs[0].r = (command >> 6) & 0x1F
    upper_ir.regs[0].type = FloatRegister
    upper_ir.regs[0].fmt = "{r}{dest}"
    upper_ir.regs[1].r = (command >> 11) & 0x1F
    upper_ir.regs[1].type = FloatRegister
    upper_ir.regs[1].fmt = "{r}{dest}"
    upper_ir.regs[2].r = (command >> 16) & 0x1F
    upper_ir.regs[2].type = FloatRegister
    upper_ir.regs[2].fmt = "{r}{dest}"
    upper_ir.dest = (command >> 21) & 0xF

    match mnemonic[-1]:
        case 'i':
            upper_ir.regs[2].r = SpecialRegister.I
            upper_ir.regs[2].type = SpecialRegister
            upper_ir.regs[2].fmt = "{r}"
        case 'q':
            upper_ir.regs[2].r = SpecialRegister.Q
            upper_ir.regs[2].type = SpecialRegister
            upper_ir.regs[2].fmt = "{r}"

def _field_2(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> str:
    # Ex: {ADDA}{x}.{xyzw} {ACC}{xyzw} {VF20}{xyzw} {VF30}{x}

    upper_ir.mnemonic = mnemonic
    upper_ir.mnemonic_fmt = "{mnemonic}{bc}.{dest}"
    upper_ir.bc = command & 0x3
    upper_ir.regs[0].r = SpecialRegister.ACC
    upper_ir.regs[0].type = SpecialRegister
    upper_ir.regs[0].fmt = "{r}{dest}"
    upper_ir.regs[1].r = (command >> 11) & 0x1F
    upper_ir.regs[1].type = FloatRegister
    upper_ir.regs[1].fmt = "{r}{dest}"
    upper_ir.regs[2].r = (command >> 16) & 0x1F
    upper_ir.regs[2].type = FloatRegister
    upper_ir.regs[2].fmt = "{r}{bc}"
    upper_ir.dest = (command >> 21) & 0xF

def _field_3(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, mnemonic: str, command: int) -> str:
    upper_ir.mnemonic = mnemonic
    upper_ir.mnemonic_fmt = "{mnemonic}.{dest}"
    upper_ir.regs[0].r = (command >> 11) & 0x1F # fs
    upper_ir.regs[0].type = FloatRegister
    upper_ir.regs[0].fmt = "{r}{dest}"
    upper_ir.regs[1].r = (command >> 16) & 0x1F # ft
    upper_ir.regs[1].type = FloatRegister
    upper_ir.regs[1].fmt = "{r}{dest}"
    upper_ir.dest = (command >> 21) & 0xF

    match mnemonic:
        case "ABS" | "FTOI0" | "FTOI4" | "FTOI12" | "FTOI15" | "ITOF0" | "ITOF4" | "ITOF12" | "ITOF15":
            # fs and ft are swapped here
            upper_ir.regs[0], upper_ir.regs[1] = upper_ir.regs[1], upper_ir.regs[0]
        case "ADDA" | "MADDA" | "MSUBA" | "MULA" | "SUBA":
            # Has ACC as first operand
            upper_ir.regs[0], upper_ir.regs[1], upper_ir.regs[2] = upper_ir.regs[2], upper_ir.regs[0], upper_ir.regs[1]
            upper_ir.regs[0].r = SpecialRegister.ACC
            upper_ir.regs[0].type = SpecialRegister
            upper_ir.regs[0].fmt = "{r}{dest}"
        case "ADDAi" | "MADDAi" | "MSUBAi" | "MULAi" | "SUBAi":
            # Has ACC as first operand, I as third
            upper_ir.regs[0], upper_ir.regs[1], upper_ir.regs[2] = upper_ir.regs[2], upper_ir.regs[0], upper_ir.regs[1]
            upper_ir.regs[0].r = SpecialRegister.ACC
            upper_ir.regs[0].type = SpecialRegister
            upper_ir.regs[0].fmt = "{r}{dest}"
            upper_ir.regs[2].r = SpecialRegister.I
            upper_ir.regs[2].type = SpecialRegister
            upper_ir.regs[2].fmt = "{r}"
        case "ADDAq" | "MADDAq" | "MSUBAq" | "MULAq" | "SUBAq":
            # Has ACC as first operand, Q as third
            upper_ir.regs[0], upper_ir.regs[1], upper_ir.regs[2] = upper_ir.regs[2], upper_ir.regs[0], upper_ir.regs[1]
            upper_ir.regs[0].r = SpecialRegister.ACC
            upper_ir.regs[0].type = SpecialRegister
            upper_ir.regs[0].fmt = "{r}{dest}"
            upper_ir.regs[2].r = SpecialRegister.Q
            upper_ir.regs[2].type = SpecialRegister
            upper_ir.regs[2].fmt = "{r}"
        case "CLIP":
            # Custom dest
            upper_ir.mnemonic_fmt = "{mnemonic}w.xyz"
            upper_ir.regs[0].fmt = "{r}xyz"
            upper_ir.regs[1].fmt = "{r}w"
        case "NOP":
            # No operands
            upper_ir.mnemonic_fmt = "{mnemonic}"
            upper_ir.regs[0].r = None
            upper_ir.regs[1].r = None
            upper_ir.regs[2].r = None
        case "OPMULA":
            # Has ACC, custom dest
            upper_ir.regs[0], upper_ir.regs[1], upper_ir.regs[2] = upper_ir.regs[2], upper_ir.regs[0], upper_ir.regs[1]
            upper_ir.mnemonic_fmt = "{mnemonic}.xyz"
            upper_ir.regs[0].r = SpecialRegister.ACC
            upper_ir.regs[0].type = SpecialRegister
            upper_ir.regs[0].fmt = "{r}xyz"
            upper_ir.regs[1].fmt = "{r}xyz"
            upper_ir.regs[2].fmt = "{r}xyz"

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

def decode(ir: VIFPacketIR, upper_ir: CommandVU.UpperIR, command: int) -> None:
    # Collect flags for IR
    upper_ir.i_flag = bool((command >> 31) & 1)
    upper_ir.e_flag = bool((command >> 30) & 1)
    upper_ir.m_flag = bool((command >> 29) & 1)
    upper_ir.d_flag = bool((command >> 28) & 1)
    upper_ir.t_flag = bool((command >> 27) & 1)

    if (command == 0x0):
        # probably alignment
        upper_ir.mnemonic = "<ALIGN>"
        return
    
    for table, extract_fn, format_fn in FIELDS:
        cmd = extract_fn(command)
        if (mnemonic := table.get(cmd, None)) is not None:
            format_fn(ir, upper_ir, mnemonic, command)
            return

    print(f"WARNING: Unrecognized VU Upper command: 0x{hex(command)[2:].upper().zfill(8)} ({bin(command)[2:].zfill(32)})")
