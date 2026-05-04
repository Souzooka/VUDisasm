import os
import sys
from elf import ELFHeader
from vif_packet import VIFPacket
from command import CommandType, CommandDMAC, CommandVIF, CommandVU

WANT_HORIZONTAL_FORMAT = True

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <filename_to_disassemble>")
    sys.exit(1)

file_path = sys.argv[1]
elf = None
try:
    elf = open(file_path, "rb")
except OSError:
    print(f"ERROR: Could not open \"{file_path}\" as file!")
    sys.exit(1)

header = ELFHeader.from_file(elf)

start = None
end = None
# TODO: Error handling for 0 programs in ELF??
vaddr_offset = (header.program_table.programs[0].p_vaddr - header.program_table.programs[0].p_offset)
if (section := header.section_table.get_section(".vutext")) is not None:
    # .vutext section located in .ELF
    start = section.sh_offset
    end = start + section.sh_size
else:
    # Prompt user for start and end address of .vutext
    # this can occur as some compilers are a bit weird and just
    # shove code and data into one big section
    print("WARNING: .vutext section not found")

    try:
        num = input("Please enter the start (virtual) address for .vutext: ")
        start = int(num, 16) - vaddr_offset
    except:
        print(f"ERROR: Could not parse \"{num}\" as hex string")
        sys.exit(1)

    try:
        num = input("Please enter the end (virtual) address for .vutext: ")
        end = int(num, 16) - vaddr_offset
    except:
        print(f"ERROR: Could not parse \"{num}\" as hex string")
        sys.exit(1)

    if (start > end):
        print("ERROR: start address greater than end address")
        sys.exit(1)
    
    if (start % 0x10 != 0):
        print("ERROR: start not 0x10 byte-aligned")
        sys.exit(1)
    
    if (end % 0x10 != 0):
        print("ERROR: end not 0x10 byte-aligned")
        sys.exit(1)

with open("output.txt", "w") as out_file:
    elf.seek(start)

    while (addr := elf.tell()) < end:
        packet = VIFPacket.from_file(elf)
        elf.seek(packet.size, os.SEEK_CUR)
        vaddr = addr + vaddr_offset

        out_file.writelines(
            [
                "------------------------------------\n",
                "-          Start of Packet         -\n",
                "------------------------------------\n",
            ]
        )

        ir = packet.decode(vaddr)
        for command in ir.commands:
            match command.type:
                # TODO: Formatting/formatter?
                case CommandType.DMAC:
                    assert isinstance(command, CommandDMAC)
                    out_file.write(f"{command.pc:#x} [DMAC] {command.id_s} {command.size:#x}, {command.addr:#010x}\n")
                case CommandType.VIF:
                    assert isinstance(command, CommandVIF)
                    command_str = f"{command.pc:#x} [VIF] {command.mnemonic}"
                    kwargs_strs = []
                    if command.kwargs:
                        for k, v in command.kwargs.items():
                            kwargs_strs.append(f"{k}={v:X}")
                        command_str += " " + ", ".join(kwargs_strs)
                    out_file.write(f"{command_str}\n")
                case CommandType.VU:
                    assert isinstance(command, CommandVU)
                    if (label := ir.get_label(command.pc)) is not None:
                        out_file.write("\n")
                        out_file.write(f"{"":>8}{str(label) + ':':<40} REFS: {", ".join(["0x" + f"{x:X}" for x in label.refs])}\n")

        out_file.writelines(
            [
                "------------------------------------\n",
                "-          End of Packet           -\n",
                "------------------------------------\n",
                "\n",
            ]
        )

elf.close()
