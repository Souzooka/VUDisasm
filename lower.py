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
FIELDS = [
    (FIELD_1_TABLE, lambda cmd: _attach_top_bit(cmd, cmd & 0x3F), _field_1)
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
