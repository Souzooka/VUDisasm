from __future__ import annotations
import struct

class ELFProgramTable:
    @classmethod
    def from_file(cls, f, header: ELFHeader):
        table = cls()
        table.programs = []
        
        pos = f.tell()
        for i in range(header.e_phnum):
            f.seek(pos + (i * header.e_phentsize))
            table.programs.append(ELFProgram.from_file(f, header))
        
        f.seek(pos)

        return table

class ELFProgram:
    @classmethod
    def from_file(cls, f, header: ELFHeader):
        program = cls()

        pos = f.tell()
        f.seek(pos + 0x4)
        program.p_offset = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x8)
        program.p_vaddr = struct.unpack("<I", f.read(4))[0]

        f.seek(pos)

        return program

class ELFSectionTable:
    @classmethod
    def from_file(cls, f, header: ELFHeader):
        table = cls()
        table.sections = []

        pos = f.tell()
        for i in range(header.e_shnum):
            f.seek(pos + (i * header.e_shentsize))
            table.sections.append(ELFSection.from_file(f, header))

        # Set section names
        str_table_offset = table.sections[header.e_shstrndx].sh_offset
        for section in table.sections:
            f.seek(str_table_offset + section.sh_name)
            name = []
            while ((char := struct.unpack("B", f.read(1))[0]) != 0):
                name.append(char)
            section.set_name("".join(chr(c) for c in name))

        return table

    def get_section(self, name: str) -> ELFSection | None:
        for section in self.sections:
            if section.name == name:
                return section
        return None

class ELFSection:
    class Type:
        SHT_NULL = 0
        SHT_PROGBITS = 1
        SHT_SYMTAB = 2
        SHT_STRTAB = 3
        SHT_RELA = 4
        SHT_HASH = 5
        SHT_DYNAMIC = 6
        SHT_NOTE = 7
        SHT_NOBITS = 8
        SHT_REL = 9
        SHT_SHLIB = 0xA
        SHT_DYNSYM = 0xB
        SHT_INIT_ARRAY = 0xE
        SHT_FINI_ARRAY = 0xF
        SHT_PREINIT_ARRAY = 0x10
        SHT_GROUP = 0x11
        SHT_SYMTAB_SHNDX = 0x12
        SHT_NUM = 0x13

    @classmethod
    def from_file(cls, f, header: ELFHeader):
        section = cls()
        section.name = ".unknown"
        pos = f.tell()

        f.seek(pos + 0x0)
        section.sh_name = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x4)
        section.sh_type = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x10)
        section.sh_offset = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x14)
        section.sh_size = struct.unpack("<I", f.read(4))[0]

        f.seek(pos)

        return section
    
    def set_name(self, name: str):
        self.name = name

class ELFHeader:
    # https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
    @classmethod
    def from_file(cls, f):
        pos = f.tell()
        header = cls()

        f.seek(pos + 0x0)
        header._magic = struct.unpack("<I", f.read(4))[0]
        if (header._magic != 0x464C457F):
            raise RuntimeError("Not an .ELF file")

        f.seek(pos + 0x1C)
        header.e_phoff = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x20)
        header.e_shoff = struct.unpack("<I", f.read(4))[0]

        f.seek(pos + 0x2A)
        header.e_phentsize = struct.unpack("<H", f.read(2))[0]

        f.seek(pos + 0x2C)
        header.e_phnum = struct.unpack("<H", f.read(2))[0]

        f.seek(pos + 0x2E)
        header.e_shentsize = struct.unpack("<H", f.read(2))[0]

        f.seek(pos + 0x30)
        header.e_shnum = struct.unpack("<H", f.read(2))[0]

        f.seek(pos + 0x32)
        header.e_shstrndx = struct.unpack("<H", f.read(2))[0]
        
        f.seek(pos + header.e_phoff)
        header.program_table = ELFProgramTable.from_file(f, header)

        f.seek(pos + header.e_shoff)
        header.section_table = ELFSectionTable.from_file(f, header)

        f.seek(pos)

        return header
