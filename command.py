from typing import Dict

class CommandType:
    NONE = 0
    DMAC = 1
    VIF = 2
    VU = 3

class CommandIR:
    def __init__(self) -> None:
        self.type = CommandType.NONE
        self.pc: int | None = None

class CommandDMAC(CommandIR):
    def __init__(self):
        super().__init__()
        self.type = CommandType.DMAC
        self.id: int = 0
        self.id_s: str = ""
        self.size: int = 0
        self.addr: int = 0

class CommandVIF(CommandIR):
    def __init__(self):
        super().__init__()
        self.type = CommandType.VIF
        self.kwargs: Dict[str, int] = {}

class CommandVU(CommandIR):
    class LowerIR:
        def __init__(self):
            self.mnemonic = ""
            self.float_value: float | None = None
            self.branch_pc: int | None = None
            self.dest: int | None = None
            self.dest_s: str | None
            self.bc: int | None = None
            self.bc_s: str | None = None
            self.r1: int | None = None
            self.r1_s: str | None = None
            self.r2: int | None = None
            self.r2_s: str | None = None
            self.r3: int | None = None
            self.r3_s: str | None = None

    class UpperIR:
        def __init__(self):
            self.mnemonic = ""
            self.i_flag = False
            self.e_flag = False
            self.m_flag = False
            self.d_flag = False
            self.t_flag = False
            self.dest: int | None = None
            self.dest_s: str | None
            self.bc: int | None = None
            self.bc_s: str | None = None
            self.r1: int | None = None
            self.r1_s: str | None = None
            self.r2: int | None = None
            self.r2_s: str | None = None
            self.r3: int | None = None
            self.r3_s: str | None = None

    def __init__(self):
        super().__init__()
        self.type = CommandType.VU
        self.lower = CommandVU.LowerIR()
        self.upper = CommandVU.UpperIR()


