from typing import Dict, Type, List, Tuple
from registers import Register

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
        self.size: int = 0
        self.addr: int = 0

class CommandVIF(CommandIR):
    def __init__(self, pc: int):
        super().__init__(pc)
        self.type = CommandType.VIF
        self.mnemonic = ""
        self.interrupt = False
        self.kwargs: Dict[str, int] = {}

class RegisterFormat():
    def __init__(self):
        self.r: int | None = None
        self.type: Type[Register] = Register
        self.fmt: str = "{r}"

class CommandVU(CommandIR):
    class LowerIR:
        def __init__(self):
            self.mnemonic = ""
            self.mnemonic_fmt = "{mnemonic}"
            self.float_value: float | None = None
            self.float_n: int | None = None # int repr of float
            self.branch_pc: int | None = None
            self.dest: int | None = None
            self.fsf: int | None = None
            self.ftf: int | None = None
            self.imm: int | None = None
            self.offset: int | None = None
            self.regs = [RegisterFormat(), RegisterFormat(), RegisterFormat()]

        def get_operands(self) -> List[Tuple[str, int]]:
            result = []
            if self.regs[0].r is not None: result.append(("r", self.regs[0].r))
            if self.regs[1].r is not None: result.append(("r", self.regs[1].r))
            if self.regs[2].r is not None: result.append(("r", self.regs[2].r))
            if self.imm is not None: result.append("imm", self.imm)
            if self.branch_pc is not None: result.append("label", self.branch_pc)
            return result

    class UpperIR:
        def __init__(self):
            self.mnemonic = ""
            self.mnemonic_fmt = "{mnemonic}"
            self.i_flag = False
            self.e_flag = False
            self.m_flag = False
            self.d_flag = False
            self.t_flag = False
            self.dest: int | None = None
            self.bc: int | None = None
            self.regs = [RegisterFormat(), RegisterFormat(), RegisterFormat()]

        def get_operands(self) -> List[Tuple[str, int]]:
            result = []
            if self.regs[0].r is not None: result.append(("r", self.regs[0].r))
            if self.regs[1].r is not None: result.append(("r", self.regs[1].r))
            if self.regs[2].r is not None: result.append(("r", self.regs[2].r))
            return result

    def __init__(self, pc: int):
        super().__init__(pc)
        self.type = CommandType.VU
        self.lower = CommandVU.LowerIR()
        self.upper = CommandVU.UpperIR()
