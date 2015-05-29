from skoolkittest import SkoolKitTestCase
from skoolkit.z80 import assemble, get_size

OPERATIONS = (
    ('ADC A,0', (206, 0)),
    ('ADC A,$01', (206, 1)),
    ('ADC A,%00000010', (206, 2)),
    ('ADC A," "', (206, 32)),
    ('ADC A,B', (136,)),
    ('ADC A,C', (137,)),
    ('ADC A,D', (138,)),
    ('ADC A,E', (139,)),
    ('ADC A,H', (140,)),
    ('ADC A,L', (141,)),
    ('ADC A,(HL)', (142,)),
    ('ADC A,A', (143,)),
    ('ADC A,IXh', (221, 140)),
    ('ADC A,IXl', (221, 141)),
    ('ADC A,(IX+5)', (221, 142, 5)),
    ('ADC A,(IX-$06)', (221, 142, 250)),
    ('ADC A,(IX+%00000111)', (221, 142, 7)),
    ('ADC A,(IX-"a")', (221, 142, 159)),
    ('ADC A,IYh', (253, 140)),
    ('ADC A,IYl', (253, 141)),
    ('ADC A,(IY-10)', (253, 142, 246)),
    ('ADC A,(IY+$10)', (253, 142, 16)),
    ('ADC A,(IY-%1)', (253, 142, 255)),
    ('ADC A,(IY+"@")', (253, 142, 64)),
    ('ADC HL,BC', (237, 74)),
    ('ADC HL,DE', (237, 90)),
    ('ADC HL,HL', (237, 106)),
    ('ADC HL,SP', (237, 122)),
    ('ADD A,11', (198, 11)),
    ('ADD A,$11', (198, 17)),
    ('ADD A,%10', (198, 2)),
    ('ADD A,"!"', (198, 33)),
    ('ADD A,B', (128,)),
    ('ADD A,C', (129,)),
    ('ADD A,D', (130,)),
    ('ADD A,E', (131,)),
    ('ADD A,H', (132,)),
    ('ADD A,L', (133,)),
    ('ADD A,(HL)', (134,)),
    ('ADD A,A', (135,)),
    ('ADD A,IXh', (221, 132)),
    ('ADD A,IXl', (221, 133)),
    ('ADD A,(IX-20)', (221, 134, 236)),
    ('ADD A,(IX+$20)', (221, 134, 32)),
    ('ADD A,(IX-%111)', (221, 134, 249)),
    ('ADD A,(IX+"$")', (221, 134, 36)),
    ('ADD A,IYh', (253, 132)),
    ('ADD A,IYl', (253, 133)),
    ('ADD A,(IY+5)', (253, 134, 5)),
    ('ADD A,(IY-$05)', (253, 134, 251)),
    ('ADD A,(IY+%101)', (253, 134, 5)),
    ('ADD A,(IY-".")', (253, 134, 210)),
    ('ADD HL,BC', (9,)),
    ('ADD HL,DE', (25,)),
    ('ADD HL,HL', (41,)),
    ('ADD HL,SP', (57,)),
    ('ADD IX,BC', (221, 9)),
    ('ADD IX,DE', (221, 25)),
    ('ADD IX,IX', (221, 41)),
    ('ADD IX,SP', (221, 57)),
    ('ADD IY,BC', (253, 9)),
    ('ADD IY,DE', (253, 25)),
    ('ADD IY,IY', (253, 41)),
    ('ADD IY,SP', (253, 57)),
    ('AND 15', (230, 15)),
    ('AND $15', (230, 21)),
    ('AND %00001111', (230, 15)),
    ('AND "&"', (230, 38)),
    ('AND B', (160,)),
    ('AND C', (161,)),
    ('AND D', (162,)),
    ('AND E', (163,)),
    ('AND H', (164,)),
    ('AND L', (165,)),
    ('AND (HL)', (166,)),
    ('AND A', (167,)),
    ('AND IXh', (221, 164)),
    ('AND IXl', (221, 165)),
    ('AND (IX+23)', (221, 166, 23)),
    ('AND (IX-$23)', (221, 166, 221)),
    ('AND (IX+%1001)', (221, 166, 9)),
    ('AND (IX-"%")', (221, 166, 219)),
    ('AND IYh', (253, 164)),
    ('AND IYl', (253, 165)),
    ('AND (IY-101)', (253, 166, 155)),
    ('AND (IY+$7F)', (253, 166, 127)),
    ('AND (IY-%1101)', (253, 166, 243)),
    ('AND (IY+"(")', (253, 166, 40)),
    ('BIT 0,B', (203, 64)),
    ('BIT 0,C', (203, 65)),
    ('BIT 0,D', (203, 66)),
    ('BIT 0,E', (203, 67)),
    ('BIT 0,H', (203, 68)),
    ('BIT 0,L', (203, 69)),
    ('BIT 0,(HL)', (203, 70)),
    ('BIT 0,A', (203, 71)),
    ('BIT 0,(IX+1)', (221, 203, 1, 70)),
    ('BIT 0,(IY+1)', (253, 203, 1, 70)),
    ('BIT 1,B', (203, 72)),
    ('BIT 1,C', (203, 73)),
    ('BIT 1,D', (203, 74)),
    ('BIT 1,E', (203, 75)),
    ('BIT 1,H', (203, 76)),
    ('BIT 1,L', (203, 77)),
    ('BIT 1,(HL)', (203, 78)),
    ('BIT 1,A', (203, 79)),
    ('BIT 1,(IX+1)', (221, 203, 1, 78)),
    ('BIT 1,(IY+1)', (253, 203, 1, 78)),
    ('BIT 2,B', (203, 80)),
    ('BIT 2,C', (203, 81)),
    ('BIT 2,D', (203, 82)),
    ('BIT 2,E', (203, 83)),
    ('BIT 2,H', (203, 84)),
    ('BIT 2,L', (203, 85)),
    ('BIT 2,(HL)', (203, 86)),
    ('BIT 2,A', (203, 87)),
    ('BIT 2,(IX+1)', (221, 203, 1, 86)),
    ('BIT 2,(IY+1)', (253, 203, 1, 86)),
    ('BIT 3,B', (203, 88)),
    ('BIT 3,C', (203, 89)),
    ('BIT 3,D', (203, 90)),
    ('BIT 3,E', (203, 91)),
    ('BIT 3,H', (203, 92)),
    ('BIT 3,L', (203, 93)),
    ('BIT 3,(HL)', (203, 94)),
    ('BIT 3,A', (203, 95)),
    ('BIT 3,(IX+1)', (221, 203, 1, 94)),
    ('BIT 3,(IY+1)', (253, 203, 1, 94)),
    ('BIT 4,B', (203, 96)),
    ('BIT 4,C', (203, 97)),
    ('BIT 4,D', (203, 98)),
    ('BIT 4,E', (203, 99)),
    ('BIT 4,H', (203, 100)),
    ('BIT 4,L', (203, 101)),
    ('BIT 4,(HL)', (203, 102)),
    ('BIT 4,A', (203, 103)),
    ('BIT 4,(IX+1)', (221, 203, 1, 102)),
    ('BIT 4,(IY+1)', (253, 203, 1, 102)),
    ('BIT 5,B', (203, 104)),
    ('BIT 5,C', (203, 105)),
    ('BIT 5,D', (203, 106)),
    ('BIT 5,E', (203, 107)),
    ('BIT 5,H', (203, 108)),
    ('BIT 5,L', (203, 109)),
    ('BIT 5,(HL)', (203, 110)),
    ('BIT 5,A', (203, 111)),
    ('BIT 5,(IX+1)', (221, 203, 1, 110)),
    ('BIT 5,(IY+1)', (253, 203, 1, 110)),
    ('BIT 6,B', (203, 112)),
    ('BIT 6,C', (203, 113)),
    ('BIT 6,D', (203, 114)),
    ('BIT 6,E', (203, 115)),
    ('BIT 6,H', (203, 116)),
    ('BIT 6,L', (203, 117)),
    ('BIT 6,A', (203, 119)),
    ('BIT 6,(HL)', (203, 118)),
    ('BIT 6,(IX+1)', (221, 203, 1, 118)),
    ('BIT 6,(IY+1)', (253, 203, 1, 118)),
    ('BIT 7,B', (203, 120)),
    ('BIT 7,C', (203, 121)),
    ('BIT 7,D', (203, 122)),
    ('BIT 7,E', (203, 123)),
    ('BIT 7,H', (203, 124)),
    ('BIT 7,L', (203, 125)),
    ('BIT 7,(HL)', (203, 126)),
    ('BIT 7,A', (203, 127)),
    ('BIT 7,(IX+1)', (221, 203, 1, 126)),
    ('BIT 7,(IY+1)', (253, 203, 1, 126)),
    ('CALL 1', (205, 1, 0)),
    ('CALL NZ,$0123', (196, 35, 1)),
    ('CALL Z,10', (204, 10, 0)),
    ('CALL NC,$1000', (212, 0, 16)),
    ('CALL C,1234', (220, 210, 4)),
    ('CALL PO,$FADE', (228, 222, 250)),
    ('CALL PE,65535', (236, 255, 255)),
    ('CALL P,$8001', (244, 1, 128)),
    ('CALL M,49152', (252, 0, 192)),
    ('CCF', (63,)),
    ('CP 123', (254, 123)),
    ('CP $50', (254, 80)),
    ('CP %10000000', (254, 128)),
    ('CP ":"', (254, 58)),
    ('CP B', (184,)),
    ('CP C', (185,)),
    ('CP D', (186,)),
    ('CP E', (187,)),
    ('CP H', (188,)),
    ('CP L', (189,)),
    ('CP (HL)', (190,)),
    ('CP A', (191,)),
    ('CP IXh', (221, 188)),
    ('CP IXl', (221, 189)),
    ('CP (IX+0)', (221, 190, 0)),
    ('CP IYh', (253, 188)),
    ('CP IYl', (253, 189)),
    ('CP (IY+0)', (253, 190, 0)),
    ('CPD', (237, 169)),
    ('CPDR', (237, 185)),
    ('CPI', (237, 161)),
    ('CPIR', (237, 177)),
    ('CPL', (47,)),
    ('DAA', (39,)),
    ('DEC B', (5,)),
    ('DEC C', (13,)),
    ('DEC D', (21,)),
    ('DEC E', (29,)),
    ('DEC H', (37,)),
    ('DEC L', (45,)),
    ('DEC (HL)', (53,)),
    ('DEC A', (61,)),
    ('DEC IXh', (221, 37)),
    ('DEC IXl', (221, 45)),
    ('DEC (IX+0)', (221, 53, 0)),
    ('DEC IYh', (253, 37)),
    ('DEC IYl', (253, 45)),
    ('DEC (IY+0)', (253, 53, 0)),
    ('DEC BC', (11,)),
    ('DEC DE', (27,)),
    ('DEC HL', (43,)),
    ('DEC SP', (59,)),
    ('DEC IX', (221, 43)),
    ('DEC IY', (253, 43)),
    ('DI', (243,)),
    ('DJNZ 16388', (16, 2)),
    ('DJNZ $4000', (16, 254)),
    ('EI', (251,)),
    ("EX AF,AF'", (8,)),
    ('EX DE,HL', (235,)),
    ('EX (SP),HL', (227,)),
    ('EX (SP),IX', (221, 227)),
    ('EX (SP),IY', (253, 227)),
    ('EXX', (217,)),
    ('HALT', (118,)),
    ('IM 0', (237, 70)),
    ('IM 1', (237, 86)),
    ('IM 2', (237, 94)),
    ('IN A,(0)', (219, 0)),
    ('IN B,(C)', (237, 64)),
    ('IN C,(C)', (237, 72)),
    ('IN D,(C)', (237, 80)),
    ('IN E,(C)', (237, 88)),
    ('IN H,(C)', (237, 96)),
    ('IN L,(C)', (237, 104)),
    ('IN A,(C)', (237, 120)),
    ('INC B', (4,)),
    ('INC C', (12,)),
    ('INC D', (20,)),
    ('INC E', (28,)),
    ('INC H', (36,)),
    ('INC L', (44,)),
    ('INC (HL)', (52,)),
    ('INC A', (60,)),
    ('INC IXh', (221, 36)),
    ('INC IXl', (221, 44)),
    ('INC IYh', (253, 36)),
    ('INC IYl', (253, 44)),
    ('INC (IX+0)', (221, 52, 0)),
    ('INC (IY+0)', (253, 52, 0)),
    ('INC BC', (3,)),
    ('INC DE', (19,)),
    ('INC HL', (35,)),
    ('INC SP', (51,)),
    ('INC IX', (221, 35)),
    ('INC IY', (253, 35)),
    ('IND', (237, 170)),
    ('INDR', (237, 186)),
    ('INI', (237, 162)),
    ('INIR', (237, 178)),
    ('JP 11', (195, 11, 0)),
    ('JP NZ,$1100', (194, 0, 17)),
    ('JP Z,23755', (202, 203, 92)),
    ('JP NC,$0110', (210, 16, 1)),
    ('JP C,24576', (218, 0, 96)),
    ('JP PO,$819A', (226, 154, 129)),
    ('JP PE,62686', (234, 222, 244)),
    ('JP P,$EDB1', (242, 177, 237)),
    ('JP M,8', (250, 8, 0)),
    ('JP (HL)', (233,)),
    ('JP (IX)', (221, 233)),
    ('JP (IY)', (253, 233)),
    ('JR 16386', (24, 0)),
    ('JR NZ,16384', (32, 254)),
    ('JR Z,$4004', (40, 2)),
    ('JR NC,16382', (48, 252)),
    ('JR C,$4006', (56, 4)),
    ('LD (16384),A', (50, 0, 64)),
    ('LD ($4000),BC', (237, 67, 0, 64)),
    ('LD (32768),DE', (237, 83, 0, 128)),
    ('LD ($8000),HL', (34, 0, 128)),
    ('LD (23295),SP', (237, 115, 255, 90)),
    ('LD ($BEEB),IX', (221, 34, 235, 190)),
    ('LD (12345),IY', (253, 34, 57, 48)),
    ('LD A,(12345)', (58, 57, 48)),
    ('LD BC,($BEEB)', (237, 75, 235, 190)),
    ('LD DE,(23295)', (237, 91, 255, 90)),
    ('LD HL,($8000)', (42, 0, 128)),
    ('LD SP,(32768)', (237, 123, 0, 128)),
    ('LD IX,($4000)', (221, 42, 0, 64)),
    ('LD IY,(16384)', (253, 42, 0, 64)),
    ('LD BC,1', (1, 1, 0)),
    ('LD DE,12', (17, 12, 0)),
    ('LD HL,123', (33, 123, 0)),
    ('LD SP,1234', (49, 210, 4)),
    ('LD SP,HL', (249,)),
    ('LD SP,IX', (221, 249)),
    ('LD SP,IY', (253, 249)),
    ('LD IX,12345', (221, 33, 57, 48)),
    ('LD IY,23456', (253, 33, 160, 91)),
    ('LD (BC),A', (2,)),
    ('LD A,(BC)', (10,)),
    ('LD (DE),A', (18,)),
    ('LD A,(DE)', (26,)),
    ('LD I,A', (237, 71)),
    ('LD A,I', (237, 87)),
    ('LD R,A', (237, 79)),
    ('LD A,R', (237, 95)),
    ('LD B,16', (6, 16)),
    ('LD B,$16', (6, 22)),
    ('LD B,%1111', (6, 15)),
    ('LD B,"B"', (6, 66)),
    ('LD B,B', (64,)),
    ('LD B,C', (65,)),
    ('LD B,D', (66,)),
    ('LD B,E', (67,)),
    ('LD B,H', (68,)),
    ('LD B,L', (69,)),
    ('LD B,(HL)', (70,)),
    ('LD B,A', (71,)),
    ('LD B,IXh', (221, 68)),
    ('LD B,IXl', (221, 69)),
    ('LD B,(IX+1)', (221, 70, 1)),
    ('LD B,(IX-$01)', (221, 70, 255)),
    ('LD B,(IX+%1)', (221, 70, 1)),
    ('LD B,(IX-"!")', (221, 70, 223)),
    ('LD B,IYh', (253, 68)),
    ('LD B,IYl', (253, 69)),
    ('LD B,(IY-2)', (253, 70, 254)),
    ('LD B,(IY+$02)', (253, 70, 2)),
    ('LD B,(IY-%10)', (253, 70, 254)),
    ('LD B,(IY+"*")', (253, 70, 42)),
    ('LD C,0', (14, 0)),
    ('LD C,B', (72,)),
    ('LD C,C', (73,)),
    ('LD C,D', (74,)),
    ('LD C,E', (75,)),
    ('LD C,H', (76,)),
    ('LD C,L', (77,)),
    ('LD C,(HL)', (78,)),
    ('LD C,A', (79,)),
    ('LD C,IXh', (221, 76)),
    ('LD C,IXl', (221, 77)),
    ('LD C,(IX+0)', (221, 78, 0)),
    ('LD C,IYh', (253, 76)),
    ('LD C,IYl', (253, 77)),
    ('LD C,(IY+0)', (253, 78, 0)),
    ('LD D,0', (22, 0)),
    ('LD D,B', (80,)),
    ('LD D,C', (81,)),
    ('LD D,D', (82,)),
    ('LD D,E', (83,)),
    ('LD D,H', (84,)),
    ('LD D,L', (85,)),
    ('LD D,(HL)', (86,)),
    ('LD D,A', (87,)),
    ('LD D,IXh', (221, 84)),
    ('LD D,IXl', (221, 85)),
    ('LD D,(IX+0)', (221, 86, 0)),
    ('LD D,IYh', (253, 84)),
    ('LD D,IYl', (253, 85)),
    ('LD D,(IY+0)', (253, 86, 0)),
    ('LD E,0', (30, 0)),
    ('LD E,B', (88,)),
    ('LD E,C', (89,)),
    ('LD E,D', (90,)),
    ('LD E,E', (91,)),
    ('LD E,H', (92,)),
    ('LD E,L', (93,)),
    ('LD E,(HL)', (94,)),
    ('LD E,A', (95,)),
    ('LD E,IXh', (221, 92)),
    ('LD E,IXl', (221, 93)),
    ('LD E,(IX+0)', (221, 94, 0)),
    ('LD E,IYh', (253, 92)),
    ('LD E,IYl', (253, 93)),
    ('LD E,(IY+0)', (253, 94, 0)),
    ('LD H,0', (38, 0)),
    ('LD H,B', (96,)),
    ('LD H,C', (97,)),
    ('LD H,D', (98,)),
    ('LD H,E', (99,)),
    ('LD H,H', (100,)),
    ('LD H,L', (101,)),
    ('LD H,(HL)', (102,)),
    ('LD H,A', (103,)),
    ('LD H,(IX+0)', (221, 102, 0)),
    ('LD H,(IY+0)', (253, 102, 0)),
    ('LD L,0', (46, 0)),
    ('LD L,B', (104,)),
    ('LD L,C', (105,)),
    ('LD L,D', (106,)),
    ('LD L,E', (107,)),
    ('LD L,H', (108,)),
    ('LD L,L', (109,)),
    ('LD L,(HL)', (110,)),
    ('LD L,A', (111,)),
    ('LD L,(IX+0)', (221, 110, 0)),
    ('LD L,(IY+0)', (253, 110, 0)),
    ('LD (HL),0', (54, 0)),
    ('LD (HL),B', (112,)),
    ('LD (HL),C', (113,)),
    ('LD (HL),D', (114,)),
    ('LD (HL),E', (115,)),
    ('LD (HL),H', (116,)),
    ('LD (HL),L', (117,)),
    ('LD (HL),A', (119,)),
    ('LD A,0', (62, 0)),
    ('LD A,B', (120,)),
    ('LD A,C', (121,)),
    ('LD A,D', (122,)),
    ('LD A,E', (123,)),
    ('LD A,H', (124,)),
    ('LD A,L', (125,)),
    ('LD A,(HL)', (126,)),
    ('LD A,A', (127,)),
    ('LD A,IXh', (221, 124)),
    ('LD A,IXl', (221, 125)),
    ('LD A,(IX+0)', (221, 126, 0)),
    ('LD A,IYh', (253, 124)),
    ('LD A,IYl', (253, 125)),
    ('LD A,(IY+0)', (253, 126, 0)),
    ('LD (IX+10),$20', (221, 54, 10, 32)),
    ('LD (IX+"A"),%00010001', (221, 54, 65, 17)),
    ('LD (IX+1),B', (221, 112, 1)),
    ('LD (IX+$02),C', (221, 113, 2)),
    ('LD (IX+%11),D', (221, 114, 3)),
    ('LD (IX+"?"),E', (221, 115, 63)),
    ('LD (IX+5),H', (221, 116, 5)),
    ('LD (IX+6),L', (221, 117, 6)),
    ('LD (IX+7),A', (221, 119, 7)),
    ('LD IXh,8', (221, 38, 8)),
    ('LD IXh,$09', (221, 38, 9)),
    ('LD IXh,%1010', (221, 38, 10)),
    ('LD IXh,">"', (221, 38, 62)),
    ('LD IXh,B', (221, 96)),
    ('LD IXh,C', (221, 97)),
    ('LD IXh,D', (221, 98)),
    ('LD IXh,E', (221, 99)),
    ('LD IXh,IXh', (221, 100)),
    ('LD IXh,IXl', (221, 101)),
    ('LD IXh,A', (221, 103)),
    ('LD IXl,0', (221, 46, 0)),
    ('LD IXl,B', (221, 104)),
    ('LD IXl,C', (221, 105)),
    ('LD IXl,D', (221, 106)),
    ('LD IXl,E', (221, 107)),
    ('LD IXl,IXh', (221, 108)),
    ('LD IXl,IXl', (221, 109)),
    ('LD IXl,A', (221, 111)),
    ('LD (IY+10),100', (253, 54, 10, 100)),
    ('LD (IY+11),B', (253, 112, 11)),
    ('LD (IY+12),C', (253, 113, 12)),
    ('LD (IY+13),D', (253, 114, 13)),
    ('LD (IY+14),E', (253, 115, 14)),
    ('LD (IY+15),H', (253, 116, 15)),
    ('LD (IY+16),L', (253, 117, 16)),
    ('LD (IY+17),A', (253, 119, 17)),
    ('LD IYh,200', (253, 38, 200)),
    ('LD IYh,B', (253, 96)),
    ('LD IYh,C', (253, 97)),
    ('LD IYh,D', (253, 98)),
    ('LD IYh,E', (253, 99)),
    ('LD IYh,IYh', (253, 100)),
    ('LD IYh,IYl', (253, 101)),
    ('LD IYh,A', (253, 103)),
    ('LD IYl,0', (253, 46, 0)),
    ('LD IYl,B', (253, 104)),
    ('LD IYl,C', (253, 105)),
    ('LD IYl,D', (253, 106)),
    ('LD IYl,E', (253, 107)),
    ('LD IYl,IYh', (253, 108)),
    ('LD IYl,IYl', (253, 109)),
    ('LD IYl,A', (253, 111)),
    ('LDD', (237, 168)),
    ('LDDR', (237, 184)),
    ('LDI', (237, 160)),
    ('LDIR', (237, 176)),
    ('NEG', (237, 68)),
    ('NOP', (0,)),
    ('OR 110', (246, 110)),
    ('OR $11', (246, 17)),
    ('OR %10101010', (246, 170)),
    ('OR "\\\\"', (246, 92)),
    ('OR B', (176,)),
    ('OR C', (177,)),
    ('OR D', (178,)),
    ('OR E', (179,)),
    ('OR H', (180,)),
    ('OR L', (181,)),
    ('OR (HL)', (182,)),
    ('OR A', (183,)),
    ('OR IXh', (221, 180)),
    ('OR IXl', (221, 181)),
    ('OR (IX+0)', (221, 182, 0)),
    ('OR IYh', (253, 180)),
    ('OR IYl', (253, 181)),
    ('OR (IY+0)', (253, 182, 0)),
    ('OTDR', (237, 187)),
    ('OTIR', (237, 179)),
    ('OUT (11),A', (211, 11)),
    ('OUT ($11),A', (211, 17)),
    ('OUT (C),B', (237, 65)),
    ('OUT (C),C', (237, 73)),
    ('OUT (C),D', (237, 81)),
    ('OUT (C),E', (237, 89)),
    ('OUT (C),H', (237, 97)),
    ('OUT (C),L', (237, 105)),
    ('OUT (C),A', (237, 121)),
    ('OUTD', (237, 171)),
    ('OUTI', (237, 163)),
    ('POP BC', (193,)),
    ('POP DE', (209,)),
    ('POP HL', (225,)),
    ('POP AF', (241,)),
    ('POP IX', (221, 225)),
    ('POP IY', (253, 225)),
    ('PUSH BC', (197,)),
    ('PUSH DE', (213,)),
    ('PUSH HL', (229,)),
    ('PUSH AF', (245,)),
    ('PUSH IX', (221, 229)),
    ('PUSH IY', (253, 229)),
    ('RES 0,B', (203, 128)),
    ('RES 0,C', (203, 129)),
    ('RES 0,D', (203, 130)),
    ('RES 0,E', (203, 131)),
    ('RES 0,H', (203, 132)),
    ('RES 0,L', (203, 133)),
    ('RES 0,(HL)', (203, 134)),
    ('RES 0,A', (203, 135)),
    ('RES 0,(IX+1)', (221, 203, 1, 134)),
    ('RES 0,(IY+1)', (253, 203, 1, 134)),
    ('RES 1,B', (203, 136)),
    ('RES 1,C', (203, 137)),
    ('RES 1,D', (203, 138)),
    ('RES 1,E', (203, 139)),
    ('RES 1,H', (203, 140)),
    ('RES 1,L', (203, 141)),
    ('RES 1,(HL)', (203, 142)),
    ('RES 1,A', (203, 143)),
    ('RES 1,(IX+1)', (221, 203, 1, 142)),
    ('RES 1,(IY+1)', (253, 203, 1, 142)),
    ('RES 2,B', (203, 144)),
    ('RES 2,C', (203, 145)),
    ('RES 2,D', (203, 146)),
    ('RES 2,E', (203, 147)),
    ('RES 2,H', (203, 148)),
    ('RES 2,L', (203, 149)),
    ('RES 2,(HL)', (203, 150)),
    ('RES 2,A', (203, 151)),
    ('RES 2,(IX+1)', (221, 203, 1, 150)),
    ('RES 2,(IY+1)', (253, 203, 1, 150)),
    ('RES 3,B', (203, 152)),
    ('RES 3,C', (203, 153)),
    ('RES 3,D', (203, 154)),
    ('RES 3,E', (203, 155)),
    ('RES 3,H', (203, 156)),
    ('RES 3,L', (203, 157)),
    ('RES 3,(HL)', (203, 158)),
    ('RES 3,A', (203, 159)),
    ('RES 3,(IX+1)', (221, 203, 1, 158)),
    ('RES 3,(IY+1)', (253, 203, 1, 158)),
    ('RES 4,B', (203, 160)),
    ('RES 4,C', (203, 161)),
    ('RES 4,D', (203, 162)),
    ('RES 4,E', (203, 163)),
    ('RES 4,H', (203, 164)),
    ('RES 4,L', (203, 165)),
    ('RES 4,(HL)', (203, 166)),
    ('RES 4,A', (203, 167)),
    ('RES 4,(IX+1)', (221, 203, 1, 166)),
    ('RES 4,(IY+1)', (253, 203, 1, 166)),
    ('RES 5,B', (203, 168)),
    ('RES 5,C', (203, 169)),
    ('RES 5,D', (203, 170)),
    ('RES 5,E', (203, 171)),
    ('RES 5,H', (203, 172)),
    ('RES 5,L', (203, 173)),
    ('RES 5,(HL)', (203, 174)),
    ('RES 5,A', (203, 175)),
    ('RES 5,(IX+1)', (221, 203, 1, 174)),
    ('RES 5,(IY+1)', (253, 203, 1, 174)),
    ('RES 6,B', (203, 176)),
    ('RES 6,C', (203, 177)),
    ('RES 6,D', (203, 178)),
    ('RES 6,E', (203, 179)),
    ('RES 6,H', (203, 180)),
    ('RES 6,L', (203, 181)),
    ('RES 6,(HL)', (203, 182)),
    ('RES 6,A', (203, 183)),
    ('RES 6,(IX+1)', (221, 203, 1, 182)),
    ('RES 6,(IY+1)', (253, 203, 1, 182)),
    ('RES 7,B', (203, 184)),
    ('RES 7,C', (203, 185)),
    ('RES 7,D', (203, 186)),
    ('RES 7,E', (203, 187)),
    ('RES 7,H', (203, 188)),
    ('RES 7,L', (203, 189)),
    ('RES 7,(HL)', (203, 190)),
    ('RES 7,A', (203, 191)),
    ('RES 7,(IX+1)', (221, 203, 1, 190)),
    ('RES 7,(IY+1)', (253, 203, 1, 190)),
    ('RET', (201,)),
    ('RET NZ', (192,)),
    ('RET Z', (200,)),
    ('RET NC', (208,)),
    ('RET C', (216,)),
    ('RET PO', (224,)),
    ('RET PE', (232,)),
    ('RET P', (240,)),
    ('RET M', (248,)),
    ('RETI', (237, 77)),
    ('RETN', (237, 69)),
    ('RL B', (203, 16)),
    ('RL C', (203, 17)),
    ('RL D', (203, 18)),
    ('RL E', (203, 19)),
    ('RL H', (203, 20)),
    ('RL L', (203, 21)),
    ('RL (HL)', (203, 22)),
    ('RL A', (203, 23)),
    ('RL (IX+1)', (221, 203, 1, 22)),
    ('RL (IY+1)', (253, 203, 1, 22)),
    ('RLA', (23,)),
    ('RLC B', (203, 0)),
    ('RLC C', (203, 1)),
    ('RLC D', (203, 2)),
    ('RLC E', (203, 3)),
    ('RLC H', (203, 4)),
    ('RLC L', (203, 5)),
    ('RLC (HL)', (203, 6)),
    ('RLC A', (203, 7)),
    ('RLC (IX-1)', (221, 203, 255, 6)),
    ('RLC (IY-1)', (253, 203, 255, 6)),
    ('RLCA', (7,)),
    ('RLD', (237, 111)),
    ('RR B', (203, 24)),
    ('RR C', (203, 25)),
    ('RR D', (203, 26)),
    ('RR E', (203, 27)),
    ('RR H', (203, 28)),
    ('RR L', (203, 29)),
    ('RR (HL)', (203, 30)),
    ('RR A', (203, 31)),
    ('RR (IX+1)', (221, 203, 1, 30)),
    ('RR (IY+1)', (253, 203, 1, 30)),
    ('RRA', (31,)),
    ('RRC B', (203, 8)),
    ('RRC C', (203, 9)),
    ('RRC D', (203, 10)),
    ('RRC E', (203, 11)),
    ('RRC H', (203, 12)),
    ('RRC L', (203, 13)),
    ('RRC (HL)', (203, 14)),
    ('RRC A', (203, 15)),
    ('RRC (IX-1)', (221, 203, 255, 14)),
    ('RRC (IY-1)', (253, 203, 255, 14)),
    ('RRCA', (15,)),
    ('RRD', (237, 103)),
    ('RST 0', (199,)),
    ('RST $08', (207,)),
    ('RST $10', (215,)),
    ('RST 24', (223,)),
    ('RST 32', (231,)),
    ('RST 40', (239,)),
    ('RST 48', (247,)),
    ('RST 56', (255,)),
    ('SBC A,20', (222, 20)),
    ('SBC A,$20', (222, 32)),
    ('SBC A,%10001000', (222, 136)),
    ('SBC A,"z"', (222, 122)),
    ('SBC A,B', (152,)),
    ('SBC A,C', (153,)),
    ('SBC A,D', (154,)),
    ('SBC A,E', (155,)),
    ('SBC A,H', (156,)),
    ('SBC A,L', (157,)),
    ('SBC A,(HL)', (158,)),
    ('SBC A,A', (159,)),
    ('SBC A,IXh', (221, 156)),
    ('SBC A,IXl', (221, 157)),
    ('SBC A,(IX+0)', (221, 158, 0)),
    ('SBC A,IYh', (253, 156)),
    ('SBC A,IYl', (253, 157)),
    ('SBC A,(IY+0)', (253, 158, 0)),
    ('SBC HL,BC', (237, 66)),
    ('SBC HL,DE', (237, 82)),
    ('SBC HL,HL', (237, 98)),
    ('SBC HL,SP', (237, 114)),
    ('SCF', (55,)),
    ('SET 0,B', (203, 192)),
    ('SET 0,C', (203, 193)),
    ('SET 0,D', (203, 194)),
    ('SET 0,E', (203, 195)),
    ('SET 0,H', (203, 196)),
    ('SET 0,L', (203, 197)),
    ('SET 0,(HL)', (203, 198)),
    ('SET 0,A', (203, 199)),
    ('SET 0,(IX+1)', (221, 203, 1, 198)),
    ('SET 0,(IY+1)', (253, 203, 1, 198)),
    ('SET 1,B', (203, 200)),
    ('SET 1,C', (203, 201)),
    ('SET 1,D', (203, 202)),
    ('SET 1,E', (203, 203)),
    ('SET 1,H', (203, 204)),
    ('SET 1,L', (203, 205)),
    ('SET 1,(HL)', (203, 206)),
    ('SET 1,A', (203, 207)),
    ('SET 1,(IX+1)', (221, 203, 1, 206)),
    ('SET 1,(IY+1)', (253, 203, 1, 206)),
    ('SET 2,B', (203, 208)),
    ('SET 2,C', (203, 209)),
    ('SET 2,D', (203, 210)),
    ('SET 2,E', (203, 211)),
    ('SET 2,H', (203, 212)),
    ('SET 2,L', (203, 213)),
    ('SET 2,(HL)', (203, 214)),
    ('SET 2,A', (203, 215)),
    ('SET 2,(IX+1)', (221, 203, 1, 214)),
    ('SET 2,(IY+1)', (253, 203, 1, 214)),
    ('SET 3,B', (203, 216)),
    ('SET 3,C', (203, 217)),
    ('SET 3,D', (203, 218)),
    ('SET 3,E', (203, 219)),
    ('SET 3,H', (203, 220)),
    ('SET 3,L', (203, 221)),
    ('SET 3,(HL)', (203, 222)),
    ('SET 3,A', (203, 223)),
    ('SET 3,(IX+1)', (221, 203, 1, 222)),
    ('SET 3,(IY+1)', (253, 203, 1, 222)),
    ('SET 4,B', (203, 224)),
    ('SET 4,C', (203, 225)),
    ('SET 4,D', (203, 226)),
    ('SET 4,E', (203, 227)),
    ('SET 4,H', (203, 228)),
    ('SET 4,L', (203, 229)),
    ('SET 4,(HL)', (203, 230)),
    ('SET 4,A', (203, 231)),
    ('SET 4,(IX+1)', (221, 203, 1, 230)),
    ('SET 4,(IY+1)', (253, 203, 1, 230)),
    ('SET 5,B', (203, 232)),
    ('SET 5,C', (203, 233)),
    ('SET 5,D', (203, 234)),
    ('SET 5,E', (203, 235)),
    ('SET 5,H', (203, 236)),
    ('SET 5,L', (203, 237)),
    ('SET 5,(HL)', (203, 238)),
    ('SET 5,A', (203, 239)),
    ('SET 5,(IX+1)', (221, 203, 1, 238)),
    ('SET 5,(IY+1)', (253, 203, 1, 238)),
    ('SET 6,B', (203, 240)),
    ('SET 6,C', (203, 241)),
    ('SET 6,D', (203, 242)),
    ('SET 6,E', (203, 243)),
    ('SET 6,H', (203, 244)),
    ('SET 6,L', (203, 245)),
    ('SET 6,(HL)', (203, 246)),
    ('SET 6,A', (203, 247)),
    ('SET 6,(IX+1)', (221, 203, 1, 246)),
    ('SET 6,(IY+1)', (253, 203, 1, 246)),
    ('SET 7,B', (203, 248)),
    ('SET 7,C', (203, 249)),
    ('SET 7,D', (203, 250)),
    ('SET 7,E', (203, 251)),
    ('SET 7,H', (203, 252)),
    ('SET 7,L', (203, 253)),
    ('SET 7,(HL)', (203, 254)),
    ('SET 7,A', (203, 255)),
    ('SET 7,(IX+1)', (221, 203, 1, 254)),
    ('SET 7,(IY+1)', (253, 203, 1, 254)),
    ('SLA B', (203, 32)),
    ('SLA C', (203, 33)),
    ('SLA D', (203, 34)),
    ('SLA E', (203, 35)),
    ('SLA H', (203, 36)),
    ('SLA L', (203, 37)),
    ('SLA (HL)', (203, 38)),
    ('SLA A', (203, 39)),
    ('SLA (IX+1)', (221, 203, 1, 38)),
    ('SLA (IY+1)', (253, 203, 1, 38)),
    ('SLL B', (203, 48)),
    ('SLL C', (203, 49)),
    ('SLL D', (203, 50)),
    ('SLL E', (203, 51)),
    ('SLL H', (203, 52)),
    ('SLL L', (203, 53)),
    ('SLL (HL)', (203, 54)),
    ('SLL A', (203, 55)),
    ('SLL (IX+1)', (221, 203, 1, 54)),
    ('SLL (IY+1)', (253, 203, 1, 54)),
    ('SRA B', (203, 40)),
    ('SRA C', (203, 41)),
    ('SRA D', (203, 42)),
    ('SRA E', (203, 43)),
    ('SRA H', (203, 44)),
    ('SRA L', (203, 45)),
    ('SRA (HL)', (203, 46)),
    ('SRA A', (203, 47)),
    ('SRA (IX+1)', (221, 203, 1, 46)),
    ('SRA (IY+1)', (253, 203, 1, 46)),
    ('SRL B', (203, 56)),
    ('SRL C', (203, 57)),
    ('SRL D', (203, 58)),
    ('SRL E', (203, 59)),
    ('SRL H', (203, 60)),
    ('SRL L', (203, 61)),
    ('SRL (HL)', (203, 62)),
    ('SRL A', (203, 63)),
    ('SRL (IX+1)', (221, 203, 1, 62)),
    ('SRL (IY+1)', (253, 203, 1, 62)),
    ('SUB 99', (214, 99)),
    ('SUB $80', (214, 128)),
    ('SUB %01000100', (214, 68)),
    ('SUB ","', (214, 44)),
    ('SUB B', (144,)),
    ('SUB C', (145,)),
    ('SUB D', (146,)),
    ('SUB E', (147,)),
    ('SUB H', (148,)),
    ('SUB L', (149,)),
    ('SUB (HL)', (150,)),
    ('SUB ( HL )', (150,)),
    ('SUB A', (151,)),
    ('SUB IXh', (221, 148)),
    ('SUB IXl', (221, 149)),
    ('SUB (IX+0)', (221, 150, 0)),
    ('SUB IYh', (253, 148)),
    ('SUB IYl', (253, 149)),
    ('SUB (IY+0)', (253, 150, 0)),
    ('XOR 43', (238, 43)),
    ('XOR $43', (238, 67)),
    ('XOR %01000010', (238, 66)),
    ('XOR "\\""', (238, 34)),
    ('XOR B', (168,)),
    ('XOR C', (169,)),
    ('XOR D', (170,)),
    ('XOR E', (171,)),
    ('XOR H', (172,)),
    ('XOR L', (173,)),
    ('XOR (HL)', (174,)),
    ('XOR A', (175,)),
    ('XOR IXh', (221, 172)),
    ('XOR IXl', (221, 173)),
    ('XOR (IX+0)', (221, 174, 0)),
    ('XOR\t(IX + 3)', (221, 174, 3)),
    ('XOR IYh', (253, 172)),
    ('XOR IYl', (253, 173)),
    ('XOR (IY+0)', (253, 174, 0))
)

INVALID_OPERATIONS = (
    'CCF A',
    'CPD B',
    'CPDR C',
    'CPI D',
    'CPIR E',
    'CPL H',
    'DAA L',
    'DI 1',
    'EI 2',
    'EXX BC',
    'HALT DE',
    'IND HL',
    'INDR SP',
    'INI IX',
    'INIR IY',
    'LDD (HL)',
    'LDDR (BC)',
    'LDI (DE)',
    'LDIR 0',
    'NEG A',
    'NOP B',
    'OTDR C',
    'OTIR D',
    'OUTD E',
    'OUTI H',
    'RETI L',
    'RETN (HL)',
    'RLA 1',
    'RLCA 2',
    'RLD 3',
    'RRA 4',
    'RRCA 5',
    'RRD 6',
    'SCF 7',
    'LD A',
    'LD HL',
    'OUT (254)',
    'IN (C)',
    'ADC',
    'ADD',
    'AND',
    'CP',
    'OR',
    'SUB',
    'SBC',
    'XOR',
    'LD A,1,2',
    'LD HL,0,1',
    'OUT (254),A,B',
    'IN (C),B,D',
    'ADC A,1,2',
    'ADD A,1,2',
    'AND 1,2',
    'CP 1,2',
    'OR 1,2',
    'SBC A,1,1'
    'SUB 1,2',
    'XOR 1,2',
    'ADC B,5',
    'ADD C,5',
    'SBC D,5',
    'IN A,x254x',
    'OUT x254x,A',
    'EX !SP!,HL',
    'LD HL,*0*',
    'LD B,(IX+0.',
    'LD C,(IZ+0)',
    'LD D,(IX*0)',
    'RETP',
    'RST 1',
    'RST 64',
    'SBC IX,DE',
    'BIT 0,IXl',
    'RES 1,IXh',
    'SET 2,IYl',
    'BIT 8,A',
    'RL IXl',
    'LD IXl,H',
    'LD IXh,(IX+0)',
    'JR 130',
    'DJNZ 65409',
    'CALL N,0',
    'JP Q,0',
    'IN A,(E)',
    'OUT (D),A',
    'LD R,B',
    'LD R,0',
    'LD I,C',
    'LD I,5',
    'LD A,256',
    'LD B,256',
    'LD C,256',
    'LD D,256',
    'LD E,256',
    'LD H,256',
    'LD L,256',
    'LD IXh,256',
    'LD IXl,256',
    'LD IYh,256',
    'LD IYl,256',
    'LD (HL),256',
    'LD (IX+0),256',
    'LD (IY+0),256',
    'AND 300',
    'CP 273',
    'OR 502',
    'SUB 260',
    'XOR 907',
    'ADC A,301',
    'SBC A,500',
    'IN A,(299)',
    'OUT (287),A',
    'LD A,n',
    'LD HL,n',
    'LD A,(n)',
    'LD HL,(n)',
    'LD (n),A',
    'LD (n),HL',
    'LD HL,65536',
    'LD HL,(65537)',
    'LD (65537),HL',
    'LD DE,65538',
    'LD DE,(65539)',
    'LD (65539),DE',
    'LD BC,65540',
    'LD BC,(65541)',
    'LD (65541),BC',
    'LD SP,65542',
    'LD SP,(65543)',
    'LD (65543),SP',
    'LD IX,65544',
    'LD IX,(65545)',
    'LD (65545),IX',
    'LD IY,65546',
    'LD IY,(65547)',
    'LD (65547),IY',
    'LD A,(65548)',
    'LD (65548),A',
    'LD SP,DE',
    'ADD HL,56',
    'ADC DE,HL',
    'EX HL,DE',
    'EX DE,BC',
    'EX AF,HL',
    'EX BC,HL',
    'EX (SP),DE',
    'EX HL,IX',
    'LD A,(IX+256)',
    'LD B,(IY-256)',
    'PUSH SP',
    'POP SP',
    'LD IXhl,0'
)

RELATIVE_JUMPS = (
    (65534, 'JR 2', (24, 2)),
    (0, 'DJNZ 65534', (16, 252)),
    (65407, 'JR Z,0', (40, 127)),
    (125, 'DJNZ 65535', (16, 128))
)

DEFB_DEFM = (
    ('1,2', (1, 2)),
    ('"ABC"', (65, 66, 67)),
    ('"A",1', (65, 1)),
    (r'0,"\"A,\""', (0, 34, 65, 44, 34)),
    (r'"C:\\",12', (67, 58, 92, 12)),
    ('256,1,1000,2', (0, 1, 0, 2)),
    ('1,x,2', (1, 0, 2))
)

DEFW = (
    ('1,256,65535', (1, 0, 0, 1, 255, 255)),
    ('$01,$100,$ffff', (1, 0, 0, 1, 255, 255)),
    ('%101,%111111111', (5, 0, 255, 1)),
    ('"a",1', (97, 0, 1, 0)),
    (r'"\\",1', (92, 0, 1, 0)),
    ('",",1', (44, 0, 1, 0)),
    ('1,65536,2', (1, 0, 0, 0, 2, 0)),
    ('?,45', (0, 0, 45, 0))
)

DEFS = (
    ('3', (0, 0, 0)),
    ('3,1', (1, 1, 1)),
    ('$02,$02', (2, 2)),
    ('3,%01010101', (85, 85, 85)),
    ('2,"b"', (98, 98)),
    ('3,","', (44, 44, 44)),
    ('2,257', (0, 0)),
    ('65536,1', ()),
    ('$,4', ())
)

class Z80Test(SkoolKitTestCase):
    def setUp(self):
        SkoolKitTestCase.setUp(self)
        self.longMessage = True

    def _test_operation(self, operation, exp_data, address):
        data = assemble(operation, address)
        self.assertEqual(exp_data, data, "assemble('{}', {}) failed".format(operation, address))
        exp_length = len(data)
        length = get_size(operation, address)
        self.assertEqual(exp_length, length, "get_size('{}', {}) failed".format(operation, address))

    def _test_assembly(self, operation, exp_data=(), address=0):
        self._test_operation(operation, exp_data, address)
        if '"' not in operation:
            self._test_operation(operation.lower(), exp_data, address)

    def test_all_instructions(self):
        for operation, exp_data in OPERATIONS:
            self._test_assembly(operation, exp_data, 16384)

    def test_invalid_instructions(self):
        for operation in INVALID_OPERATIONS:
            self._test_assembly(operation)

    def test_relative_jumps_across_64k_boundary(self):
        for address, operation, exp_data in RELATIVE_JUMPS:
            self._test_assembly(operation, exp_data, address)

    def test_defb(self):
        for items, exp_data in DEFB_DEFM:
            self._test_assembly('DEFB {}'.format(items), exp_data)

    def test_defm(self):
        for items, exp_data in DEFB_DEFM:
            self._test_assembly('DEFM {}'.format(items), exp_data)

    def test_defw(self):
        for items, exp_data in DEFW:
            self._test_assembly('DEFW {}'.format(items), exp_data)

    def test_defs(self):
        for items, exp_data in DEFS:
            self._test_assembly('DEFS {}'.format(items), exp_data)