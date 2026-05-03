from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

# TODO: probably put this in another file because it's gonna get copied in lower
MNEMONIC_SIZE = 15
REG_SIZE = 10
COMMAND_PREFIX = PREFIXES.VU_LOWER

def _field_1(mnemonic: str, command: int, pc: int) -> str:
    MNEMONIC_FORMAT = "{0}"
    ID_FORMAT = "{0},"
    IS_FORMAT = "{0},"
    IT_FORMAT = "{0}"
    FORMAT = f"{{0:<{MNEMONIC_SIZE}}} {{1:<{REG_SIZE}}} {{2:<{REG_SIZE}}} {{3}}"

    id_ = IntRegister.get_register((command >> 6) & 0x1F)
    is_ = IntRegister.get_register((command >> 11) & 0x1F)
    it = IntRegister.get_register((command >> 16) & 0x1F)

    mnemonic_s = MNEMONIC_FORMAT.format(mnemonic)
    id_s = ID_FORMAT.format(id_)
    is_s = IS_FORMAT.format(is_)
    it_s = IT_FORMAT.format(it)

    return FORMAT.format(mnemonic_s, id_s, is_s, it_s)

def _field_3(mnemonic: str, command: int, pc: int) -> str:
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    dest = FloatRegister.get_dest((command >> 21) & 0xF)
    is_ = IntRegister.get_register((command >> 11) & 0x1F)
    it_ = IntRegister.get_register((command >> 16) & 0x1F)

    match mnemonic:
        case "EATANxy" | "EATANxz" | "ELENG" | "ERLENG" | "ERSADD" | "ESADD" | "ESUM":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{IntRegister.P},":<{REG_SIZE}} {fs}"
        case "ILWR" | "ISWR":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{it_},":<{REG_SIZE}} ({is_}){dest}"
        case "LQD":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} (--{is_})"
        case "LQI":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} ({is_}++)"
        case "MFIR":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} {is_}"
        case "MFP":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} {IntRegister.P}"
        case "MOVE":
            if (ft == fs): return "NOP"
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} {fs}{dest}"
        case "MR32":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} {fs}{dest}"
        case "RGET" | "RNEXT":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{ft}{dest},":<{REG_SIZE}} {IntRegister.R}"
        case "SQD":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{fs}{dest},":<{REG_SIZE}} (--{it_})"
        case "SQI":
            return f"{f"{mnemonic}.{dest}":<{MNEMONIC_SIZE}} {f"{fs}{dest},":<{REG_SIZE}} ({it_}++)"
        case "WAITP" | "WAITQ":
            return f"{mnemonic}"
        case "XGKICK":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {is_}"
        case "XITOP" | "XTOP":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {it_}"

    raise RuntimeError(f"Could not represent VU lower field type 3 mnemonic {mnemonic}")

def _field_4(mnemonic: str, command: int, pc: int) -> str:
    fs = FloatRegister.get_register((command >> 11) & 0x1F)
    ft = FloatRegister.get_register((command >> 16) & 0x1F)
    fsf = FloatRegister.get_bc((command >> 21) & 0x3)
    ftf = FloatRegister.get_bc((command >> 23) & 0x3)
    is_ = IntRegister.get_register((command >> 11) & 0x1F)
    it_ = IntRegister.get_register((command >> 16) & 0x1F)

    match mnemonic:
        case "DIV" | "RSQRT":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{FloatRegister.Q},":<{REG_SIZE}} {f"{fs}{fsf},":<{REG_SIZE}} {ft}{ftf}"
        case "EATAN" | "EEXP" | "ERCPR" | "ERSQRT" | "ESIN" | "ESQRT":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{IntRegister.P},":<{REG_SIZE}} {fs}{fsf}"
        case "MTIR":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{it_},":<{REG_SIZE}} {fs}{fsf}"
        case "RINIT" | "RXOR":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{IntRegister.R},":<{REG_SIZE}} {fs}{fsf}"
        case "SQRT":
            return f"{mnemonic:<{MNEMONIC_SIZE}} {f"{FloatRegister.Q},":<{REG_SIZE}} {ft}{ftf}"

    raise RuntimeError(f"Could not represent VU lower field type 4 mnemonic {mnemonic}")

def _field_5(mnemonic: str, command: int, pc: int) -> str:
    is_ = IntRegister.get_register((command >> 11) & 0x1F)
    it_ = IntRegister.get_register((command >> 16) & 0x1F)
    imm5 = (command >> 6) & 0x1F
    
    # imm5 is signed
    if (imm5 & 0x10):
        imm5 = 0x20 - imm5

    return f"{f"{mnemonic}":<{MNEMONIC_SIZE}} {f"{it_},":<{REG_SIZE}} {f"{is_},":<{REG_SIZE}} {imm5}"

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
FIELDS = [
    (FIELD_1_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x3F), _field_1),
    (FIELD_3_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x7FF), _field_3),
    (FIELD_4_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x7FF), _field_4),
    (FIELD_5_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x3F), _field_5),
]

def decode(command: int, pc: int) -> str:

    if (command == 0x0):
        # probably alignment
        return COMMAND_PREFIX + "<ALIGN>"
    
    for table, extract_fn, format_fn in FIELDS:
        cmd = extract_fn(command)
        if (mnemonic := table.get(cmd, None)) is not None:
            return COMMAND_PREFIX + format_fn(mnemonic, command, pc)
    
    return COMMAND_PREFIX + hex(command)
