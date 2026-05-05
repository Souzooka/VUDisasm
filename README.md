# VUDisasm

VUDisasm is a simple Python script which parses the .vutext section of PS2 executables and displays the section in a human-readable format.

# Usage + Example Output

Usage: `python vudisasm.py <filename>`

Section of example output (`python vudisasm.py SCES_556.70`):

```
// ...
         SUB_4600E8:                    REFS: 0x4603E0, 0x460608, 0x4604F0, 0x460830, 0x460718
0x4600E8   NOP                                               |  NOP                                                        
0x4600F0   LQ.yzw          VF23,      0x14(VI03)yzw          |  SUB.xyzw        VF26xyzw,  VF25xyzw,  VF24xyzw             
0x4600F8   LQ.yzw          VF17,      0x14(VI04)yzw          |  NOP                                                        
0x460100   DIV             Q,         VF22w,     VF23w       |  NOP                                                        
0x460108   LQ.xyzw         VF27,      0xA(VI03)xyzw          |  NOP                                                        
0x460110   LQ.xyzw         VF22,      0xA(VI04)xyzw          |  NOP                                                        
0x460118   NOP                                               |  SUB.yzw         VF23yzw,   VF23yzw,   VF17yzw              
0x460120   NOP                                               |  MULAw.yzw       ACCyzw,    VF17yzw,   VF00w                
0x460128   NOP                                               |  SUB.xyzw        VF27xyzw,  VF27xyzw,  VF22xyzw             
0x460130   IADDIU          VI06,      VI01,      0x0         |  MADDq.yzw       VF17yzw,   VF23yzw,   Q                    
0x460138   MOVE.xyzw       VF24xyzw,  VF25xyzw               |  MULAw.xyzw      ACCxyzw,   VF24xyzw,  VF00w                
0x460140   LQ.xyzw         VF25,      0x1(VI03)xyzw          |  MADDq.xyzw      VF26xyzw,  VF26xyzw,  Q                    
0x460148   IADDIU          VI04,      VI03,      0x0         |  MULAw.xyzw      ACCxyzw,   VF22xyzw,  VF00w                
0x460150   IADDIU          VI03,      VI03,      0x1         |  MADDq.xyzw      VF27xyzw,  VF27xyzw,  Q                    
0x460158   SQ.yzw          VF17,      0x14(VI05)yzw          |  NOP                                                        
0x460160   SQI.xyzw        VF26xyzw,  (VI05++)               |  CLIPw.xyz       VF25xyz,   VF25w                           
0x460168   JR              VI02                              |  NOP                                                        
0x460170   SQ.xyzw         VF27,      0x9(VI05)xyzw          |  NOP                                                        

         SUB_460178:                    REFS: 0x460400, 0x460628, 0x460510, 0x460850, 0x460738
0x460178   IBNE            VI01,      VI00,      LAB_45F9B0  |  NOP                                                        
0x460180   [VIF]    NOP        
0x460184   [VIF]    MPG        SIZE=0x800, LOADADDR=0x800
0x460188   NOP                                               |  NOP                                                        
0x460190   LQ.xyzw         VF22,      0xA(VI03)xyzw          |  NOP                                                        
0x460198   LQ.yzw          VF17,      0x14(VI03)yzw          |  NOP                                                        
0x4601A0   SQI.xyzw        VF25xyzw,  (VI05++)               |  NOP                                                        
0x4601A8   SQ.xyzw         VF22,      0x9(VI05)xyzw          |  NOP                                                        
0x4601B0   SQ.yzw          VF17,      0x13(VI05)yzw          |  NOP                                                        
0x4601B8   LQ.xyzw         VF25,      0x1(VI03)xyzw          |  MAX.xyzw        VF24xyzw,  VF25xyzw,  VF25xyzw             
0x4601C0   IADDIU          VI04,      VI03,      0x0         |  NOP                                                        
0x4601C8   IADDIU          VI03,      VI03,      0x1         |  NOP                                                        
0x4601D0   JR              VI02                              |  NOP                                                        
0x4601D8   IADDIU          VI06,      VI01,      0x0         |  CLIPw.xyz       VF25xyz,   VF25w                           

         SUB_4601E0:                    REFS: 0x461B80, 0x460AE8, 0x461FC8, 0x461670, 0x460F90
0x4601E0   IBNE            VI12,      VI00,      LAB_460910  |  NOP                                                        
0x4601E8   FCAND           VI01,      0x2FBEF                |  NOP                                                        
0x4601F0   IBEQ            VI01,      VI00,      LAB_460910  |  NOP                                                        
0x4601F8   FCOR            VI01,      0xFDF7DF               |  NOP                                                        
0x460200   IBNE            VI01,      VI00,      LAB_460908  |  NOP                                                        
0x460208   FCOR            VI01,      0xFF7DF7               |  NOP                                                        
0x460210   IBNE            VI01,      VI00,      LAB_460908  |  NOP                                                        
0x460218   FCOR            VI01,      0xFFBEFB               |  NOP                                                        
0x460220   IBNE            VI01,      VI00,      LAB_460908  |  NOP                                                        
0x460228   FCOR            VI01,      0xFFDF7D               |  NOP                                                        
0x460230   IBNE            VI01,      VI00,      LAB_460908  |  NOP                                                        
0x460238   FCOR            VI01,      0xFFEFBE               |  NOP                                                        
0x460240   IBNE            VI01,      VI00,      LAB_460908  |  NOP                                                                                              
// ...
```
