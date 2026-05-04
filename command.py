from typing import Dict

class CommandType:
    NONE = 0
    DMAC = 1
    VIF = 2
    VU = 3

class CommandIR:
    def __init__(self, pc: int) -> None:
        self.type = CommandType.NONE
        self.pc = pc

class CommandDMAC(CommandIR):
    def __init__(self, pc: int):
        super().__init__(pc)
        self.type = CommandType.DMAC
        self.id: int = 0
        self.id_s: str = "" # TODO: Have a formatter handle this
        self.size: int = 0
        self.addr: int = 0

class CommandVIF(CommandIR):
    def __init__(self, pc: int):
        super().__init__(pc)
        self.type = CommandType.VIF
        self.mnemonic = ""
        self.interrupt = False
        self.kwargs: Dict[str, int] = {}

class CommandVU(CommandIR):
    class LowerIR:
        def __init__(self):
            self.mnemonic = ""
            self.float_value: float | None = None
            self.branch_pc: int | None = None
            self.dest: int | None = None
            self.bc: int | None = None
            self.r1: int | None = None
            self.r1_fmt = "{r}"
            self.r2: int | None = None
            self.r2_fmt = "{r}"
            self.r3: int | None = None
            self.r3_fmt = "{r}"

    class UpperIR:
        def __init__(self):
            self.mnemonic = ""
            self.i_flag = False
            self.e_flag = False
            self.m_flag = False
            self.d_flag = False
            self.t_flag = False
            self.dest: int | None = None
            self.bc: int | None = None
            self.r1: int | None = None
            self.r1_fmt = "{r}"
            self.r2: int | None = None
            self.r2_fmt = "{r}"
            self.r3: int | None = None
            self.r3_fmt = "{r}"

    def __init__(self, pc: int):
        super().__init__(pc)
        self.type = CommandType.VU
        self.lower = CommandVU.LowerIR()
        self.upper = CommandVU.UpperIR()


