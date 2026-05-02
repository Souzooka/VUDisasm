from registers import FloatRegister, IntRegister

def decode(command: int) -> str:
    #TODO
    COMMAND_PREFIX = f"{"[VU]":<8}"
    return COMMAND_PREFIX + hex(command)
