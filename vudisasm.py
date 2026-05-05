import os
import sys
from elf import ELFHeader
from vif_packet import VIFPacket
from format import format_commands

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
        lines = format_commands(ir)
        out_file.writelines(lines)

        out_file.writelines(
            [
                "------------------------------------\n",
                "-          End of Packet           -\n",
                "------------------------------------\n",
                "\n",
            ]
        )

elf.close()
