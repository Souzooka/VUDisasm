import os
import struct
from elf import ELFHeader
from lower import decode as lower_decode
from upper import decode as upper_decode
from vif import decode as vif_decode
from vif_packet import VIFPacket

# TODO: Accept filepath as arg
with open("SCES_556.70", "rb") as elf:
    header = ELFHeader.from_file(elf)

    start = None
    end = None
    vaddr_offset = (header.program_table.programs[0].p_vaddr - header.program_table.programs[0].p_offset)
    if (section := header.section_table.get_section(".vutext")) is not None:
        start = section.sh_offset
        end = start + section.sh_size
    else:
        # TODO: prompt user for start and end address of .vutext
        import sys
        print("WARNING: .vutext section not found")
        sys.exit(1)

    with open("output.txt", "w") as out_file:
        elf.seek(start)

        while (addr := elf.tell()) < end:
            packet = VIFPacket.from_file(elf)
            print(hex(packet.size))
            elf.seek(packet.size, os.SEEK_CUR)
            vaddr = addr + vaddr_offset

            out_file.writelines(
                [
                    "------------------------------------\n",
                    "-          Start of Packet         -\n",
                    "------------------------------------\n",
                ]
            )

            commands = packet.decode()
            for i, command in enumerate(commands):
                out_file.write(f"{hex(vaddr+(i*4)):<15} {command}\n")

            out_file.writelines(
                [
                    "------------------------------------\n",
                    "-          End of Packet           -\n",
                    "------------------------------------\n",
                    "\n",
                ]
            )
