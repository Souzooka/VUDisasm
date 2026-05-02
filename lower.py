from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

COMMAND_PREFIX = PREFIXES.VU_LOWER

def decode(command: int, pc: int) -> str:
    #TODO

    if (command == 0x0):
        # probably alignment
        return COMMAND_PREFIX + "<ALIGN>"
    
    return COMMAND_PREFIX + hex(command)
