# VUDisasm

VUDisasm is a simple Python script which parses the .vutext section of PS2 executables and displays the section in a human-readable format.

# Usage + Example Output

Usage: `python vudisasm.py <filename>`

Beginning of example output (`python vudisasm.py SCES_556.70`):

```
------------------------------------
-          Start of Packet         -
------------------------------------
0x45f4f0        [DMAC]  ret 0x480
0x45f4f4        [DMAC]  0x0
0x45f4f8        [VIF]   NOP
0x45f4fc        [VIF]   MPG          SIZE=0x470, LOADADDR=0x0
0x45f500        [VU_l]  LQ.xyzw         VF01,      0x30(VI00)xyzw
0x45f504        [VU_u]  NOP
0x45f508        [VU_l]  XTOP            VI01
0x45f50c        [VU_u]  NOP
0x45f510        [VU_l]  MTIR            VI02,      VF01x
0x45f514        [VU_u]  NOP
0x45f518        [VU_l]  ILW.w           VI03,      0x0(VI01)w
0x45f51c        [VU_u]  NOP
0x45f520        [VU_l]  ILW.z           VI04,      0x0(VI01)z
0x45f524        [VU_u]  NOP
0x45f528        [VU_l]  ILW.y           VI05,      0x0(VI01)y
0x45f52c        [VU_u]  NOP
0x45f530        [VU_l]  ILW.x           VI06,      0x0(VI01)x
0x45f534        [VU_u]  NOP
0x45f538        [VU_l]  IBNE            VI03,      VI00,      0x45f590
0x45f53c        [VU_u]  NOP
0x45f540        [VU_l]  IADDIU          VI01,      VI01,      0x0001
0x45f544        [VU_u]  NOP
0x45f548        [VU_l]  LQI.xyzw        VF02xyzw,  (VI01++)
0x45f54c        [VU_u]  NOP
0x45f550        [VU_l]  ISUBIU          VI04,      VI04,      0x0001
0x45f554        [VU_u]  NOP
0x45f558        [VU_l]  NOP
0x45f55c        [VU_u]  NOP
0x45f560        [VU_l]  IBGTZ           VI04,      0x45f548
0x45f564        [VU_u]  NOP
0x45f568        [VU_l]  SQI.xyzw        VF02xyzw,  (VI02++)
0x45f56c        [VU_u]  NOP
0x45f570        [VU_l]  IBNE            VI05,      VI00,      0x45f5d8
0x45f574        [VU_u]  NOP
0x45f578        [VU_l]  NOP
0x45f57c        [VU_u]  NOP
0x45f580        [VU_l]  B               0x45f518
0x45f584        [VU_u]  NOP
0x45f588        [VU_l]  NOP
0x45f58c        [VU_u]  NOP
// ...
```
