# VUDisasm

VUDisasm is a simple Python script which parses the .vutext section of PS2 executables and displays the section in a human-readable format.

# Usage + Example Output

Usage: `python vudisasm.py <filename>`

Section of example output (`python vudisasm.py SCES_556.70`):

```
// ...
------------------------------------
-          Start of Packet         -
------------------------------------
0x45F970   [DMAC]   ret 0x2910, 0x00000000
0x45F978   [VIF]    NOP        
0x45F97C   [VIF]    MPG        SIZE=0x800, LOADADDR=0x0

         SUB_45F980:                    
0x45F980   LQ.xyzw         VF01,      0x30(VI00)xyzw         |  NOP                                                        
0x45F988   XTOP            VI01                              |  NOP                                                        
0x45F990   MTIR            Q,         VI02,      VF01x       |  NOP                                                        

         LAB_45F998:                    REFS: 0x45FA00, 0x45FA48
0x45F998   ILW.w           VI03,      0x0(VI01)w             |  NOP                                                        
0x45F9A0   ILW.z           VI04,      0x0(VI01)z             |  NOP                                                        
0x45F9A8   ILW.y           VI05,      0x0(VI01)y             |  NOP                                                        
0x45F9B0   ILW.x           VI06,      0x0(VI01)x             |  NOP                                                        
0x45F9B8   IBNE            VI03,      VI00,      LAB_45FA10  |  NOP                                                        
0x45F9C0   IADDIU          VI01,      VI01,      0x1         |  NOP                                                        

         LAB_45F9C8:                    REFS: 0x45F9E0
0x45F9C8   LQI.xyzw        VF02xyzw,  (VI01++)               |  NOP                                                        
0x45F9D0   ISUBIU          VI04,      VI04,      0x1         |  NOP                                                        
0x45F9D8   NOP                                               |  NOP                                                        
0x45F9E0   IBGTZ           VI04,      LAB_45F9C8             |  NOP                                                        
0x45F9E8   SQI.xyzw        VF02xyzw,  (VI02++)               |  NOP                                                        
0x45F9F0   IBNE            VI05,      VI00,      LAB_45FA58  |  NOP                                                        
0x45F9F8   NOP                                               |  NOP                                                        
0x45FA00   B               LAB_45F998                        |  NOP                                                        
0x45FA08   NOP                                               |  NOP                                                        

         LAB_45FA10:                    REFS: 0x45F9B8, 0x45FA28
0x45FA10   LQI.xyzw        VF02xyzw,  (VI01++)               |  NOP                                                        
0x45FA18   ISUBIU          VI03,      VI03,      0x1         |  NOP                                                        
0x45FA20   NOP                                               |  NOP                                                        
0x45FA28   IBNE            VI03,      VI00,      LAB_45FA10  |  NOP                                                        
0x45FA30   SQI.xyzw        VF02xyzw,  (VI04++)               |  NOP                                                        
0x45FA38   IBNE            VI05,      VI00,      LAB_45FA58  |  NOP                                                        
0x45FA40   NOP                                               |  NOP                                                        
0x45FA48   B               LAB_45F998                        |  NOP                                                        
0x45FA50   NOP                                               |  NOP                                                        
// ...
```
