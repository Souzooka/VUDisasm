from prefixes import PREFIXES
from registers import FloatRegister, IntRegister

def decode(command: int, pc: int) -> str:
    #TODO
    COMMAND_PREFIX = PREFIXES.VU

    if (command == 0x0):
        # probably alignment
        return COMMAND_PREFIX + "<ALIGN>"
    
    return COMMAND_PREFIX + hex(command)
