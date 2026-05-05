from __future__ import annotations
from typing import List, TYPE_CHECKING
from command import CommandType
from prefixes import PREFIXES

if TYPE_CHECKING:
    from command import CommandDMAC, CommandVIF, CommandVU
    from vif_packet import VIFPacketIR

_PC_SIZE = 8
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
_VU_OPERAND_SIZE = 12
"""Size of VU operation operands"""
_VU_COMMAND_SIZE = 60
"""Size of upper or lower string"""

def _format_dmac(command: CommandDMAC) -> List[str]:
    DMA_IDS = ["refe", "cnt", "next", "ref", "refs", "call", "ret", "end"]
    pc_s = f"{command.pc:#x} "
    prefix_s = f"{PREFIXES.DMAC} "
    return [f"{pc_s:<{_PC_SIZE}} {prefix_s:<{_PREFIX_SIZE}} {DMA_IDS[command.id]} 0x{command.size:X}, 0x{command.addr:08x}\n"]

def _format_vif(command: CommandVIF) -> List[str]:
    pc_s = f"{command.pc:#x} "
    prefix_s = f"{PREFIXES.VIF} "
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
