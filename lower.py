from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from prefixes import PREFIXES
from registers import FloatRegister, IntRegister, SpecialRegister

if TYPE_CHECKING:
    from command import CommandVU
    from vif_packet import VIFPacketIR

# TODO: probably put this in another file because it's gonna get copied in lower
# NOTE: guess it got copied in lower
MNEMONIC_SIZE = 15
REG_SIZE = 10
COMMAND_PREFIX = PREFIXES.VU_LOWER

def _field_1(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    lower_ir.mnemonic = mnemonic
    lower_ir.regs[0].r = (command >> 6) & 0x1F # id
    lower_ir.regs[0].type = IntRegister
    lower_ir.regs[1].r = (command >> 11) & 0x1F # is
    lower_ir.regs[1].type = IntRegister
    lower_ir.regs[2].r = (command >> 16) & 0x1F # it
    lower_ir.regs[2].type = IntRegister
    lower_ir.dest = (command >> 21) & 0xF

def _field_3(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    lower_ir.mnemonic = mnemonic
    lower_ir.dest = (command >> 21) & 0xF

    match mnemonic:
        case "EATANxy" | "EATANxz" | "ELENG" | "ERLENG" | "ERSADD" | "ESADD" | "ESUM":
            lower_ir.regs[0].r = SpecialRegister.P
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = (command >> 11) & 0x1F # is
            lower_ir.regs[1].type = FloatRegister
        case "ILWR" | "ISWR":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # it
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = (command >> 11) & 0x1F # is
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "({r}){dest}"
        case "LQD":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 11) & 0x1F # is
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "(--{r})"
        case "LQI":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 11) & 0x1F # is
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "({r}++)"
        case "MFIR":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 11) & 0x1F # is
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "{r}"
        case "MFP":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = SpecialRegister.P
            lower_ir.regs[1].type = SpecialRegister
            lower_ir.regs[1].fmt = "{r}"
        case "MOVE":
            fs = (command >> 11) & 0x1F
            ft = (command >> 16) & 0x1F
            if fs == ft:
                lower_ir.mnemonic = "NOP"
                return

            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = fs
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{dest}"
        case "MR32":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 11) & 0x1F # fs
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{dest}"
        case "RGET" | "RNEXT":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 16) & 0x1F # ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = SpecialRegister.R
            lower_ir.regs[1].type = SpecialRegister
            lower_ir.regs[1].fmt = "{r}{dest}"
        case "SQD":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 11) & 0x1F # fs
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 16) & 0x1F # it
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "(--{r})"
        case "SQI":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = (command >> 11) & 0x1F # fs
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[0].fmt = "{r}{dest}"
            lower_ir.regs[1].r = (command >> 16) & 0x1F # it
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "({r}++)"
        case "WAITP" | "WAITQ":
            pass
        case "XGKICK":
            lower_ir.regs[0].r = (command >> 11) & 0x1F # is
            lower_ir.regs[0].type = IntRegister
        case "XITOP" | "XTOP":
            lower_ir.regs[0].r = (command >> 16) & 0x1F # it
            lower_ir.regs[0].type = IntRegister
        case _:
            raise RuntimeError(f"Could not represent VU lower field type 3 mnemonic {mnemonic}")

def _field_4(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    fs = (command >> 11) & 0x1F
    ft = (command >> 16) & 0x1F
    fsf = (command >> 21) & 0x3
    ftf = (command >> 23) & 0x3
    is_ = fs
    it_ = ft
    lower_ir.mnemonic = mnemonic
    lower_ir.fsf = fsf
    lower_ir.ftf = ftf

    match mnemonic:
        case "DIV" | "RSQRT":
            lower_ir.regs[0].r = SpecialRegister.Q
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = fs
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{fsf}"
            lower_ir.regs[2].r = ft
            lower_ir.regs[2].type = FloatRegister
            lower_ir.regs[2].fmt = "{r}{ftf}"
        case "EATAN" | "EEXP" | "ERCPR" | "ERSQRT" | "ESIN" | "ESQRT":
            lower_ir.regs[0].r = SpecialRegister.P
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = fs
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{fsf}"
        case "MTIR":
            lower_ir.regs[0].r = SpecialRegister.Q
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = it_
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "{r}"
            lower_ir.regs[2].r = fs
            lower_ir.regs[2].type = FloatRegister
            lower_ir.regs[2].fmt = "{r}{fsf}"
        case "RINIT" | "RXOR":
            lower_ir.regs[0].r = SpecialRegister.R
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = fs
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{fsf}"
        case "SQRT":
            lower_ir.regs[0].r = SpecialRegister.Q
            lower_ir.regs[0].type = SpecialRegister
            lower_ir.regs[1].r = ft
            lower_ir.regs[1].type = FloatRegister
            lower_ir.regs[1].fmt = "{r}{ftf}"
        case _:
            raise RuntimeError(f"Could not represent VU lower field type 4 mnemonic {mnemonic}")

def _field_5(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    is_ = IntRegister.get_register((command >> 11) & 0x1F)
    it_ = IntRegister.get_register((command >> 16) & 0x1F)
    imm5 = (command >> 6) & 0x1F
    
    # imm5 is signed
    if (imm5 & 0x10):
        imm5 = imm5 - 0x20

    lower_ir.mnemonic = mnemonic
    lower_ir.regs[0].r = it_
    lower_ir.regs[0].type = IntRegister
    lower_ir.regs[1].r = is_
    lower_ir.regs[1].type = IntRegister
    lower_ir.regs[1].fmt = "{r}"
    lower_ir.imm = imm5

def _resolve_branch_pc(ir: VIFPacketIR, pc: int, imm: int) -> Tuple[bool, int]:
    # Sections of microprograms can have VIFcode between them (esp. since you can only transfer 0x800 bytes at a time)
    # so we need to properly handle gaps between microprogram parts
    # Bit of a hacky workaround so need to see if there's a better way to handle this
    pc += 8
    actual_start_addr = 0
    forward_ref = False
    for load_addr, size, vaddr in ir.load_addrs:
        if pc in range(vaddr, vaddr+size):
            actual_start_addr = (pc - vaddr) + load_addr
    
    actual_end_addr = actual_start_addr + imm * 8

    # PC wrapping (this assumes VU1!!!)
    if actual_end_addr < 0x0:
        actual_end_addr += 0x4000
    if actual_end_addr >= 0x4000:
        actual_end_addr -= 0x4000

    branch_pc = -1
    for load_addr, size, vaddr in ir.load_addrs:
        if actual_end_addr in range(load_addr, load_addr+size):
            branch_pc = vaddr + (actual_end_addr - load_addr)

    if branch_pc == -1: 
        # Forward reference
        forward_ref = True
        branch_pc = actual_end_addr

    return forward_ref, branch_pc

def _field_7(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    imm11 = command & 0x7FF
    fs = (command >> 11) & 0x1F
    ft = (command >> 16) & 0x1F
    is_ = fs
    it_ = ft
    dest = (command >> 21) & 0xF

    lower_ir.mnemonic = mnemonic

    # imm11 is signed
    if (imm11 & 0x400):
        imm11 = imm11 - 0x800

    # Create label
    match mnemonic:
        case "B" | "IBEQ" | "IBNE" | "IBGEZ" | "IBGTZ" | "IBLEZ" | "IBLTZ":
            forward_ref, branch_pc = _resolve_branch_pc(ir, pc, imm11)
            label = ir.get_or_new_label(branch_pc, forward_ref)
            label.set_type(label.B)
            label.add_ref(pc)
            lower_ir.branch_pc = branch_pc
            lower_ir.forward_ref = forward_ref
        case "BAL":
            forward_ref, branch_pc = _resolve_branch_pc(ir, pc, imm11)
            label = ir.get_or_new_label(branch_pc, forward_ref)
            label.set_type(label.BAL)
            label.add_ref(pc)
            lower_ir.branch_pc = branch_pc
            lower_ir.forward_ref = forward_ref
    match mnemonic:
        case "B":
            pass
        case "BAL":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
        case "IBEQ" | "IBNE":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
        case "IBGEZ" | "IBGTZ" | "IBLEZ" | "IBLTZ":
            lower_ir.regs[0].r = is_
            lower_ir.regs[0].type = IntRegister
        case "ILW" | "ISW":
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.dest = dest
            lower_ir.offset = imm11
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "{offset}({r}){dest}"
        case "JALR":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
        case "JR":
            lower_ir.regs[0].r = is_
            lower_ir.regs[0].type = IntRegister
        case "LQ":
            lower_ir.dest = dest
            lower_ir.offset = imm11
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = ft
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "{offset}({r}){dest}"
        case "SQ":
            lower_ir.dest = dest
            lower_ir.offset = imm11
            lower_ir.mnemonic_fmt = "{mnemonic}.{dest}"
            lower_ir.regs[0].r = fs
            lower_ir.regs[0].type = FloatRegister
            lower_ir.regs[1].r = it_
            lower_ir.regs[1].type = IntRegister
            lower_ir.regs[1].fmt = "{offset}({r}){dest}"
        case _:
            raise RuntimeError(f"Could not represent VU lower field type 7 mnemonic {mnemonic}")

def _field_8(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    imm_lower = command & 0x7FF
    imm_upper = (command >> 21) & 0xF
    is_ = (command >> 11) & 0x1F
    it_ = (command >> 16) & 0x1F
    imm12 = ((imm_upper & 0x1) << 11) | imm_lower
    imm15 = (imm_upper << 11) | imm_lower
    lower_ir.mnemonic = mnemonic

    match mnemonic:
        case "FCGET":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
        case "FMAND" | "FMEQ" | "FMOR":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
        case "FSAND" | "FSEQ" | "FSOR":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.imm = imm12
        case "FSSET":
            lower_ir.imm = imm12
        case "IADDIU" | "ISUBIU":
            lower_ir.regs[0].r = it_
            lower_ir.regs[0].type = IntRegister
            lower_ir.regs[1].r = is_
            lower_ir.regs[1].type = IntRegister
            lower_ir.imm = imm15
        case _:
            raise RuntimeError(f"Could not represent VU lower field type 8 mnemonic {mnemonic}")

def _field_9(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, mnemonic: str, command: int, pc: int) -> str:
    imm = command & 0xFFFFFF
    lower_ir.mnemonic = mnemonic

    match mnemonic:
        case "FCAND" | "FCEQ" | "FCOR":
            lower_ir.regs[0].r = 1
            lower_ir.regs[0].type = IntRegister
            lower_ir.imm = imm
        case "FCSET":
            lower_ir.imm = imm
        case _:
            raise RuntimeError(f"Could not represent VU lower field type 9 mnemonic {mnemonic}")

def _attach_top_bit(cmd: int, n: int):
    # Lower has a different field type depending on if the top bit is set,
    # so we'll just move it to LSB for opcodes so we can easily check
    # if we have the correct field type
    n <<= 1
    n |= (cmd >> 31) & 1
    return n

FIELD_1_TABLE = {
    0b110000_1: "IADD",
    0b110100_1: "IAND",
    0b110101_1: "IOR",
    0b110001_1: "ISUB",
}
FIELD_3_TABLE = {
    0b11101_1111_00_1: "EATANxy",
    0b11101_1111_01_1: "EATANxz",
    0b11100_1111_10_1: "ELENG",
    0b11100_1111_11_1: "ERLENG",
    0b11100_1111_01_1: "ERSADD",
    0b11100_1111_00_1: "ESADD",
    0b11101_1111_10_1: "ESUM",
    0b01111_1111_10_1: "ILWR",
    0b01111_1111_11_1: "ISWR",
    0b01101_1111_10_1: "LQD",
    0b01101_1111_00_1: "LQI",
    0b01111_1111_01_1: "MFIR",
    0b11001_1111_00_1: "MFP",
    0b01100_1111_00_1: "MOVE",
    0b01100_1111_01_1: "MR32",
    0b10000_1111_01_1: "RGET",
    0b10000_1111_00_1: "RNEXT",
    0b01101_1111_11_1: "SQD",
    0b01101_1111_01_1: "SQI",
    0b11110_1111_11_1: "WAITP",
    0b01110_1111_11_1: "WAITQ",
    0b11011_1111_00_1: "XGKICK",
    0b11010_1111_01_1: "XITOP",
    0b11010_1111_00_1: "XTOP",
}
FIELD_4_TABLE = {
    0b01110_1111_00_1: "DIV",
    0b11111_1111_01_1: "EATAN",
    0b11111_1111_10_1: "EEXP",
    0b11110_1111_10_1: "ERCPR",
    0b11110_1111_01_1: "ERSQRT",
    0b11111_1111_00_1: "ESIN",
    0b11110_1111_00_1: "ESQRT",
    0b01111_1111_00_1: "MTIR",
    0b10000_1111_10_1: "RINIT",
    0b01110_1111_10_1: "RSQRT",
    0b10000_1111_11_1: "RXOR",
    0b01110_1111_01_1: "SQRT",
}
FIELD_5_TABLE = {
    0b110010_1: "IADDI",
}
FIELD_7_TABLE = {
    0b0100000: "B",
    0b0100001: "BAL",
    0b0101000: "IBEQ",
    0b0101111: "IBGEZ",
    0b0101101: "IBGTZ",
    0b0101110: "IBLEZ",
    0b0101100: "IBLTZ",
    0b0101001: "IBNE",
    0b0000100: "ILW",
    0b0000101: "ISW",
    0b0100101: "JALR",
    0b0100100: "JR",
    0b0000000: "LQ",
    0b0000001: "SQ",
}
FIELD_8_TABLE = {
    0b0011100: "FCGET",
    0b0011010: "FMAND",
    0b0011000: "FMEQ",
    0b0011011: "FMOR",
    0b0010110: "FSAND",
    0b0010100: "FSEQ",
    0b0010111: "FSOR",
    0b0010101: "FSSET",
    0b0001000: "IADDIU",
    0b0001001: "ISUBIU",
}
FIELD_9_TABLE = {
    0b0010010: "FCAND",
    0b0010000: "FCEQ",
    0b0010011: "FCOR",
    0b0010001: "FCSET",
}
FIELDS = [
    (FIELD_1_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x3F), _field_1),
    (FIELD_3_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x7FF), _field_3),
    (FIELD_4_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x7FF), _field_4),
    (FIELD_5_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x3F), _field_5),
    (FIELD_7_TABLE, lambda cmd: cmd >> 25, _field_7),
    (FIELD_8_TABLE, lambda cmd: cmd >> 25, _field_8),
    (FIELD_9_TABLE, lambda cmd: cmd >> 25, _field_9),
]

def decode(ir: VIFPacketIR, lower_ir: CommandVU.LowerIR, command: int, pc: int) -> None:

    if (command == 0x0):
        # probably alignment
        lower_ir.mnemonic = "<ALIGN>"
        return
    
    for table, extract_fn, format_fn in FIELDS:
        cmd = extract_fn(command)
        if (mnemonic := table.get(cmd, None)) is not None:
            format_fn(ir, lower_ir, mnemonic, command, pc)
            return
    
    print(f"WARNING: Unrecognized VU Lower command: 0x{hex(command)[2:].upper().zfill(8)} ({bin(command)[2:].zfill(32)})")
    return
