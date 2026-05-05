from __future__ import annotations
from typing import List, TYPE_CHECKING
from command import CommandType
from prefixes import PREFIXES
from registers import Register

if TYPE_CHECKING:
    from command import CommandDMAC, CommandVIF, CommandVU
    from vif_packet import VIFPacketIR

_PC_SIZE = 10
"""Size of PC on left side of line"""
_PREFIX_SIZE = 8
"""Size of category prefix"""

# VIF
_VIF_MNEMONIC_SIZE = 10
"""Size of VIF mnemonic"""
_VIF_KWARGS_LEFT_PAD = 1
"""Space between mnemonic and kwargs"""

# VU labels
_VU_LABEL_LEFT_ALIGN = 20
"""Left align for "LAB_0123456", etc. labels"""
_VU_LABEL_REFS_LEFT_PAD = 20
"""Left align relative to label for label references"""

# VU
_VU_MNEMONIC_SIZE = 15
"""Size of VU mnemonic"""
_VU_LOWER_OPERAND_SIZE = 10
"""Size of VU lower operation operands"""
_VU_UPPER_OPERAND_SIZE = 10
"""Size of VU upper operation operands"""
_VU_COMMAND_SIZE = 60
"""Size of upper or lower string"""

def _hex(n: int) -> str:
    sign = n < 0
    return f"{"-" if sign else ""}0x{abs(n):X}"

def _format_dmac(command: CommandDMAC) -> List[str]:
    DMA_IDS = ["refe", "cnt", "next", "ref", "refs", "call", "ret", "end"]
    pc_s = f"{_hex(command.pc)}"
    prefix_s = f"{PREFIXES.DMAC}"
    return [f"{pc_s:<{_PC_SIZE}} {prefix_s:<{_PREFIX_SIZE}} {DMA_IDS[command.id]} 0x{command.size:X}, 0x{command.addr:08x}\n"]

def _format_vif(command: CommandVIF) -> List[str]:
    pc_s = f"{_hex(command.pc)}"
    prefix_s = f"{PREFIXES.VIF}"
    mnemonic_s = f"{command.mnemonic} "
    kwargs_strings = [f"{k}=0x{v:X}" for k, v in command.kwargs.items()]
    kwarg_s = ", ".join(kwargs_strings)
    return [f"{pc_s:<{_PC_SIZE}} {prefix_s:<{_PREFIX_SIZE}} {mnemonic_s:<{_VIF_MNEMONIC_SIZE}}{" ":<{_VIF_KWARGS_LEFT_PAD}}{kwarg_s}\n"]

def _format_vu(ir: VIFPacketIR, command: CommandVU) -> List[str]:
    lines = []

    # Check for a label first
    if (label := ir.get_label(command.pc)) is not None:
        # Found label
        lines.append("\n")
        label_s = f"{str(label) + ":":>{_VU_LABEL_LEFT_ALIGN}}"
        ref_strings = []
        for ref in label.refs:
            ref_strings.append(f"0x{ref:X}")
        ref_s = ", ".join(ref_strings)
        if ref_s != "":
            ref_s = f"{f"REFS: {ref_s}"}"
        lines.append(f"{label_s}{" ":<{_VU_LABEL_REFS_LEFT_PAD}}{ref_s}\n")

    # Lower commands
    pc_s = f"{_hex(command.pc)}"
    pc_s = f"{pc_s:<{_PC_SIZE}}"
    if command.lower.float_value is not None:
        # LOI instruction
        mnemonic_s = "LOI"
        operand_s = str(command.lower.float_value)
    else:
        # Mnemonic
        format_args = {
            "mnemonic": command.lower.mnemonic,
            "dest": Register.get_dest(command.lower.dest),
        }
        mnemonic_s = f"{command.lower.mnemonic_fmt.format(**format_args):<{_VU_MNEMONIC_SIZE}}"
        # Operands
        operand_strings = []
        for _type, reg_index, val in command.lower.get_operands():
            match _type:
                case "r":
                    format_args = {
                        "r": command.lower.regs[reg_index].type.get_register(val),
                        "dest": command.lower.regs[reg_index].type.get_dest(command.lower.dest),
                        "offset": f"{_hex(command.lower.offset or 0)}",
                        "fsf": command.lower.regs[reg_index].type.get_bc(command.lower.fsf),
                        "ftf": command.lower.regs[reg_index].type.get_bc(command.lower.ftf),
                    }
                    operand_strings.append(command.lower.regs[reg_index].fmt.format(**format_args))
                case "imm":
                    operand_strings.append(f"{_hex(val)}")
                case "label":
                    operand_strings.append(str(ir.get_label(val, forward_ref=command.lower.forward_ref)))

        # Stick a comma on the end of each but last operand
        for i in range(len(operand_strings) - 1): operand_strings[i] += ","
        # Pad each operand
        for i in range(len(operand_strings)): operand_strings[i] = f"{operand_strings[i]:<{_VU_LOWER_OPERAND_SIZE}}"
        # Join the operands
        operand_s = " ".join(operand_strings)

    # Put together the lower line
    line = f"{f"{pc_s} {mnemonic_s} {operand_s}":<{_VU_COMMAND_SIZE}} | "

    # Upper commands
    pc_s = f"0x{command.pc:X}"
    pc_s = f"{pc_s:<{_PC_SIZE}}"
    # Mnemonic
    format_args = {
        "mnemonic": command.upper.mnemonic,
        "dest": Register.get_dest(command.upper.dest),
        "bc": Register.get_bc(command.upper.bc)
    }
    mnemonic_s = f"{command.upper.mnemonic_fmt.format(**format_args):<{_VU_MNEMONIC_SIZE}}"
    # Operands
    operand_strings = []
    for _type, reg_index, val in command.upper.get_operands():
        match _type:
            case "r":
                format_args = {
                    "r": command.upper.regs[reg_index].type.get_register(val),
                    "dest": command.upper.regs[reg_index].type.get_dest(command.upper.dest),
                    "bc": command.upper.regs[reg_index].type.get_bc(command.upper.bc),
                }
                operand_strings.append(command.upper.regs[reg_index].fmt.format(**format_args))

    # Stick a comma on the end of each but last operand
    for i in range(len(operand_strings) - 1): operand_strings[i] += ","
    # Pad each operand
    for i in range(len(operand_strings)): operand_strings[i] = f"{operand_strings[i]:<{_VU_UPPER_OPERAND_SIZE}}"
    # Join the operands
    operand_s = " ".join(operand_strings)

    # Put together the lower line
    line += f"{f" {mnemonic_s} {operand_s}":<{_VU_COMMAND_SIZE}}"

    lines.append(line + "\n")
    return lines

def format_commands(ir: VIFPacketIR) -> List[str]:
    lines = []
    for command in ir.commands:
        match command.type:
            case CommandType.DMAC:
                lines.extend(_format_dmac(command))
            case CommandType.VIF:
                lines.extend(_format_vif(command))
            case CommandType.VU:
                lines.extend(_format_vu(ir, command))
    
    return lines
