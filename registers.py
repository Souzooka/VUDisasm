from abc import abstractmethod

class Register:
    COMPONENTS = ['x', 'y', 'z', 'w']
    ACC = "ACC"
    I = "I"
    Q = "Q"
    R = "R"
    P = "P"

    @classmethod
    def get_component(cls, reg: int) -> str:
        return cls.COMPONENTS[reg]
    
    @classmethod
    @abstractmethod
    def get_register(cls, reg: int) -> str:
        pass

    @classmethod
    def get_bc(cls, bc: int | None) -> str | None:
        if bc is None: return None

        return cls.COMPONENTS[bc]
    
    @classmethod
    def get_dest(cls, dest: int | None) -> str | None:
        if dest is None: return None

        result = ""
        for i in range(len(cls.COMPONENTS)):
            if (dest & (1 << i)):
                result += cls.COMPONENTS[i]
        return result

    @classmethod
    def get_register_w_bc(cls, reg: int, bc: int):
        return f"{cls.get_register(reg)}{cls.get_bc(bc)}"

class IntRegister(Register):

    @classmethod
    def get_register(cls, reg: int) -> str:
        return f"VI{str(reg).zfill(2)}"
    
class FloatRegister(Register):

    @classmethod
    def get_register(cls, reg: int) -> str:
        return f"VF{str(reg).zfill(2)}"
    
class SpecialRegister(Register):
    ACC = 32
    I = 33
    Q = 34
    R = 35
    P = 36

    @classmethod
    def get_register(cls, reg: int) -> str:
        match reg:
            case SpecialRegister.ACC:
                return "ACC"
            case SpecialRegister.I:
                return "I"
            case SpecialRegister.Q:
                return "Q"
            case SpecialRegister.R:
                return "R"
            case SpecialRegister.P:
                return "P"
            case _:
                raise RuntimeError()