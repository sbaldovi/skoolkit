;
; SkoolKit control file for the 48K Spectrum ROM.
;
; Routine titles taken from 'The Complete Spectrum ROM Disassembly' by Dr Ian
; Logan and Dr Frank O'Hara, published by Melbourne House.
;
; To build the HTML disassembly, find a dump of the 48K Spectrum ROM (48.rom),
; and run these commands:
;   sna2skool.py -o 0 -H -c 48.rom.ctl 48.rom > 48.rom.skool
;   skool2html.py 48.rom.ref
;

@ $0000 start
@ $0000 org=$0000
@ $0000 set-handle-unsupported-macros=1
c $0000 THE 'START'
c $0008 THE 'ERROR' RESTART
c $0010 THE 'PRINT A CHARACTER' RESTART
u $0013
c $0018 THE 'COLLECT CHARACTER' RESTART
c $0020 THE 'COLLECT NEXT CHARACTER' RESTART
u $0025
c $0028 THE 'CALCULATOR' RESTART
u $002B
c $0030 THE 'MAKE BC SPACES' RESTART
c $0038 THE 'MASKABLE INTERRUPT' ROUTINE
c $0053 THE 'ERROR-2' ROUTINE
u $005F
c $0066 THE 'NON-MASKABLE INTERRUPT' ROUTINE
c $0074 THE 'CH-ADD+1' SUBROUTINE
c $007D THE 'SKIP-OVER' SUBROUTINE
t $0095 THE TOKEN TABLE
  $0096,3,2:B1
  $0099,6,5:B1
  $009F,2,1:B1
  $00A1,2,1:B1
  $00A3,5,4:B1
  $00A8,7,6:B1
  $00AF,4,3:B1
  $00B3,2,1:B1
  $00B5,3,2:B1
  $00B8,4,3:B1
  $00BC,4,3:B1
  $00C0,3,2:B1
  $00C3,3,2:B1
  $00C6,3,2:B1
  $00C9,3,2:B1
  $00CC,3,2:B1
  $00CF,3,2:B1
  $00D2,3,2:B1
  $00D5,3,2:B1
  $00D8,2,1:B1
  $00DA,3,2:B1
  $00DD,3,2:B1
  $00E0,3,2:B1
  $00E3,3,2:B1
  $00E6,3,2:B1
  $00E9,4,3:B1
  $00ED,2,1:B1
  $00EF,3,2:B1
  $00F2,4,3:B1
  $00F6,4,3:B1
  $00FA,3,2:B1
  $00FD,3,2:B1
  $0100,2,1:B1
  $0102,3,2:B1
  $0105,2,1:B1
  $0107,2,1:B1
  $0109,2,1:B1
  $010B,4,3:B1
  $010F,4,3:B1
  $0113,2,1:B1
  $0115,4,3:B1
  $0119,6,5:B1
  $011F,3,2:B1
  $0122,6,5:B1
  $0128,4,3:B1
  $012C,5,4:B1
  $0131,6,5:B1
  $0137,7,6:B1
  $013E,5,4:B1
  $0143,6,5:B1
  $0149,4,3:B1
  $014D,6,5:B1
  $0153,3,2:B1
  $0156,5,4:B1
  $015B,5,4:B1
  $0160,6,5:B1
  $0166,7,6:B1
  $016D,4,3:B1
  $0171,3,2:B1
  $0174,6,5:B1
  $017A,5,4:B1
  $017F,4,3:B1
  $0183,4,3:B1
  $0187,4,3:B1
  $018B,7,6:B1
  $0192,3,2:B1
  $0195,6,5:B1
  $019B,8,7:B1
  $01A3,3,2:B1
  $01A6,3,2:B1
  $01A9,3,2:B1
  $01AC,5,4:B1
  $01B1,6,5:B1
  $01B7,5,4:B1
  $01BC,4,3:B1
  $01C0,4,3:B1
  $01C4,3,2:B1
  $01C7,5,4:B1
  $01CC,4,3:B1
  $01D0,4,3:B1
  $01D4,5,4:B1
  $01D9,4,3:B1
  $01DD,3,2:B1
  $01E0,4,3:B1
  $01E4,9,8:B1
  $01ED,2,1:B1
  $01EF,3,2:B1
  $01F2,4,3:B1
  $01F6,5,4:B1
  $01FB,6,5:B1
  $0201,4,3:B1
b $0205 THE KEY TABLES
c $028E THE 'KEYBOARD SCANNING' SUBROUTINE
c $02BF THE 'KEYBOARD' SUBROUTINE
c $0310 THE 'REPEATING KEY' SUBROUTINE
c $031E THE 'K-TEST' SUBROUTINE
c $0333 THE 'KEYBOARD DECODING' SUBROUTINE
c $03B5 THE 'BEEPER' SUBROUTINE
c $03F8 THE 'BEEP' COMMAND ROUTINE
B $03F9,14,1*6,4,1
B $0439,2,1
B $043F,4,1
B $044B,16,1*6,3,1
B $046D,1
b $046E THE 'SEMI-TONE' TABLE
c $04AA THE 'PROGRAM NAME' SUBROUTINE (ZX81)
c $04C2 THE 'SA-BYTES' SUBROUTINE
c $053F THE 'SA/LD-RET' SUBROUTINE
B $0553,1
c $0556 THE 'LD-BYTES' SUBROUTINE
c $05E3 THE 'LD-EDGE-2' AND 'LD-EDGE-1' SUBROUTINES
c $0605 THE 'SAVE, LOAD, VERIFY & MERGE' COMMAND ROUTINES
B $0643,1
B $0671,1
c $07CB THE 'VERIFY' CONTROL ROUTINE
c $0802 THE 'LOAD A DATA BLOCK' SUBROUTINE
B $0807,1
c $0808 THE 'LOAD' CONTROL ROUTINE
c $08B6 THE 'MERGE' CONTROL ROUTINE
c $092C THE 'MERGE A LINE OR A VARIABLE' SUBROUTINE
c $0970 THE 'SAVE' CONTROL ROUTINE
t $09A1 THE CASSETTE MESSAGES
  $09A2,31,30:B1
  $09C1,10,B1:8:B1
  $09CB,15,B1:13:B1
  $09DA,18,B1:16:B1
  $09EC,8,B1:6:B1
c $09F4 THE 'PRINT-OUT' ROUTINES
b $0A11 THE 'CONTROL CHARACTER' TABLE
c $0A23 THE 'CURSOR LEFT' SUBROUTINE
c $0A3D THE 'CURSOR RIGHT' SUBROUTINE
c $0A4F THE 'CARRIAGE RETURN' SUBROUTINE
c $0A5F THE 'PRINT COMMA' SUBROUTINE
c $0A69 THE 'PRINT A QUESTION MARK' SUBROUTINE
c $0A6D THE 'CONTROL CHARACTERS WITH OPERANDS' ROUTINE
c $0AD9 PRINTABLE CHARACTER CODES
c $0ADC THE 'POSITION STORE' SUBROUTINE
c $0B03 THE 'POSITION FETCH' SUBROUTINE
c $0B24 THE 'PRINT ANY CHARACTER(S)' SUBROUTINE
c $0B7F THE 'PRINT ALL CHARACTERS' SUBROUTINE
c $0BDB THE 'SET ATTRIBUTE BYTE' SUBROUTINE
c $0C0A THE 'MESSAGE PRINTING' SUBROUTINE
c $0C3B THE 'PO-SAVE' SUBROUTINE
c $0C41 THE 'TABLE SEARCH' SUBROUTINE
c $0C55 THE 'TEST FOR SCROLL' SUBROUTINE
B $0C87,1
B $0CF8,1
T $0CF9,7,6:B1
B $0D01,1
c $0D4D THE 'TEMPORARY COLOUR ITEMS' SUBROUTINE
c $0D6B THE 'CLS COMMAND' ROUTINE
c $0DAF THE 'CLEARING THE WHOLE DISPLAY AREA' SUBROUTINE
c $0DD9 THE 'CL-SET' SUBROUTINE
c $0DFE THE 'SCROLLING' SUBROUTINE
c $0E44 THE 'CLEAR LINES' SUBROUTINE
c $0E88 THE 'CL-ATTR' SUBROUTINE
c $0E9B THE 'CL-ADDR' SUBROUTINE
c $0EAC THE 'COPY' COMMAND ROUTINE
c $0ECD THE 'COPY-BUFF' SUBROUTINE
c $0EDF THE 'CLEAR PRINTER BUFFER' SUBROUTINE
c $0EF4 THE 'COPY-LINE' SUBROUTINE
B $0F0B,1
c $0F2C THE 'EDITOR' ROUTINES
c $0F81 THE 'ADD-CHAR' SUBROUTINE
b $0FA0 THE 'EDITING KEYS' TABLE
c $0FA9 THE 'EDIT KEY' SUBROUTINE
c $0FF3 THE 'CURSOR DOWN EDITING' SUBROUTINE
c $1007 THE 'CURSOR LEFT EDITING' SUBROUTINE
c $100C THE 'CURSOR RIGHT EDITING' SUBROUTINE
c $1015 THE 'DELETE EDITING' SUBROUTINE
c $101E THE 'ED-IGNORE' SUBROUTINE
c $1024 THE 'ENTER EDITING' SUBROUTINE
c $1031 THE 'ED-EDGE' SUBROUTINE
c $1059 THE 'CURSOR UP EDITING' SUBROUTINE
c $1076 THE 'ED-SYMBOL' SUBROUTINE
c $107F THE 'ED-ERROR' SUBROUTINE
c $1097 THE 'CLEAR-SP' SUBROUTINE
c $10A8 THE 'KEYBOARD INPUT' SUBROUTINE
c $111D THE 'LOWER SCREEN COPYING' SUBROUTINE
c $1190 THE 'SET-HL' AND 'SET-DE' SUBROUTINES
c $11A7 THE 'REMOVE-FP' SUBROUTINE
c $11B7 THE 'NEW COMMAND' ROUTINE
c $12A2 THE 'MAIN EXECUTION' LOOP
t $1391 THE REPORT MESSAGES
  $1392,2,1:B1
  $1394,16,15:B1
  $13A4,18,17:B1
  $13B6,15,14:B1
  $13C5,13,12:B1
  $13D2,13,12:B1
  $13DF,14,13:B1
  $13ED,20,19:B1
  $1401,11,10:B1
  $140C,14,13:B1
  $141A,16,15:B1
  $142A,20,19:B1
  $143E,17,16:B1
  $144F,20,19:B1
  $1463,11,10:B1
  $146E,17,16:B1
  $147F,16,15:B1
  $148F,13,12:B1
  $149C,16,15:B1
  $14AC,18,17:B1
  $14BE,14,13:B1
  $14CC,18,17:B1
  $14DE,14,13:B1
  $14EC,14,13:B1
  $14FA,14,13:B1
  $1508,14,13:B1
  $1516,15,14:B1
  $1525,18,17:B1
  $1537,2,1:B1
  $1539,28,B1:26:B1
c $1555 Report G - No room for line
c $155D THE 'MAIN-ADD' SUBROUTINE
b $15AF THE 'INITIAL CHANNEL INFORMATION'
c $15C4 Report J - Invalid I/O device
B $15C5,1
b $15C6 THE 'INITIAL STREAM DATA'
c $15D4 THE 'WAIT-KEY' SUBROUTINE
B $15E5,1
c $15E6 THE 'INPUT-AD' SUBROUTINE
c $15EF THE 'MAIN PRINTING' SUBROUTINE
c $1601 THE 'CHAN-OPEN' SUBROUTINE
B $160F,1
c $1615 THE 'CHAN-FLAG' SUBROUTINE
b $162D THE 'CHANNEL CODE LOOK-UP' TABLE
c $1634 THE 'CHANNEL 'K' FLAG' SUBROUTINE
c $1642 THE 'CHANNEL 'S' FLAG' SUBROUTINE
c $164D THE 'CHANNEL 'P' FLAG' SUBROUTINE
c $1652 THE 'MAKE-ROOM' SUBROUTINE
c $1664 THE 'POINTERS' SUBROUTINE
c $168F THE 'COLLECT A LINE NUMBER' SUBROUTINE
B $168F,2
c $169E THE 'RESERVE' SUBROUTINE
c $16B0 THE 'SET-MIN' SUBROUTINE
c $16D4 THE 'RECLAIM THE EDIT-LINE' SUBROUTINE
c $16DB THE 'INDEXER' SUBROUTINE
c $16E5 THE 'CLOSE #' COMMAND ROUTINE
c $1701 THE 'CLOSE-2' SUBROUTINE
b $1716 THE 'CLOSE STREAM LOOK-UP' TABLE
c $171C THE 'CLOSE STREAM' SUBROUTINE
c $171E THE 'STREAM DATA' SUBROUTINE
B $1726,1
c $1736 THE 'OPEN#' COMMAND ROUTINE
B $1737,2,1
c $175D THE 'OPEN-2' SUBROUTINE
B $1766,1
b $177A THE 'OPEN STREAM LOOK-UP' TABLE
c $1781 THE 'OPEN-K' SUBROUTINE
c $1785 THE 'OPEN-S' SUBROUTINE
c $1789 THE 'OPEN-P' SUBROUTINE
c $1793 THE 'CAT, ERASE, FORMAT & MOVE' COMMAND ROUTINES
c $1795 THE 'LIST & LLIST' COMMAND ROUTINES
c $17F5 THE 'LLIST' ENTRY POINT
c $17F9 THE 'LIST' ENTRY POINT
c $1855 THE 'PRINT A WHOLE BASIC LINE' SUBROUTINE
c $18B6 THE 'NUMBER' SUBROUTINE
c $18C1 THE 'PRINT A FLASHING CHARACTER' SUBROUTINE
c $18E1 THE 'PRINT THE CURSOR' SUBROUTINE
c $190F THE 'LN-FETCH' SUBROUTINE
c $1925 THE 'PRINTING CHARACTERS IN A BASIC LINE' SUBROUTINE
c $196E THE 'LINE-ADDR' SUBROUTINE
c $1980 THE 'COMPARE LINE NUMBERS' SUBROUTINE
c $1988 THE 'FIND EACH STATEMENT' SUBROUTINE
c $19B8 THE 'NEXT-ONE' SUBROUTINE
c $19DD THE 'DIFFERENCE' SUBROUTINE
c $19E5 THE 'RECLAIMING' SUBROUTINE
c $19FB THE 'E-LINE-NO' SUBROUTINE
c $1A1B THE 'REPORT AND LINE NUMBER PRINTING' SUBROUTINE
b $1A48 THE SYNTAX TABLES
c $1B17 THE 'MAIN PARSER' OF THE BASIC INTERPRETER
c $1B28 THE STATEMENT LOOP
c $1B6F THE 'SEPARATOR' SUBROUTINE
c $1B76 THE 'STMT-RET' SUBROUTINE
B $1B7C,1
c $1B8A THE 'LINE-RUN' ENTRY POINT
c $1B9E THE 'LINE-NEW' SUBROUTINE
B $1BB1,1
c $1BB2 THE 'REM' COMMAND ROUTINE
c $1BB3 THE 'LINE-END' ROUTINE
c $1BBF THE 'LINE-USE' ROUTINE
c $1BD1 THE 'NEXT-LINE' ROUTINE
B $1BED,1
c $1BEE THE 'CHECK-END' SUBROUTINE
c $1BF4 THE 'STMT-NEXT' ROUTINE
b $1C01 THE 'COMMAND CLASS' TABLE
c $1C0D THE 'COMMAND CLASSES - 00, 03 & 05'
c $1C16 THE 'JUMP-C-R' ROUTINE
c $1C1F THE 'COMMAND CLASSES - 01, 02 & 04'
c $1C22 THE 'VARIABLE IN ASSIGNMENT' SUBROUTINE
B $1C2F,1
c $1C56 THE 'FETCH A VALUE' SUBROUTINE
c $1C6C THE 'COMMAND CLASS 04' ROUTINE
c $1C79 THE 'EXPECT NUMERIC/STRING EXPRESSIONS' SUBROUTINE
B $1C8B,1
c $1C96 THE 'SET PERMANENT COLOURS' SUBROUTINE (EQU. CLASS-07)
c $1CBE THE 'COMMAND CLASS 09' ROUTINE
c $1CDB THE 'COMMAND CLASS 0B' ROUTINE
c $1CDE THE 'FETCH A NUMBER' SUBROUTINE
B $1CEB,2,1
c $1CEE THE 'STOP' COMMAND ROUTINE
B $1CEF,1
c $1CF0 THE 'IF' COMMAND ROUTINE
B $1CF7,2,1
c $1D03 THE 'FOR' COMMAND ROUTINE
B $1D14,2,1
B $1D17,6,1
B $1D36,3,1
B $1D85,1
c $1D86 THE 'LOOK-PROG' SUBROUTINE
c $1DAB THE 'NEXT' COMMAND ROUTINE
B $1DBE,6,1
c $1DDA THE 'NEXT-LOOP' SUBROUTINE
B $1DDB,12,1
B $1DD9,1
B $1DE9,1
c $1DEC THE 'READ' COMMAND ROUTINE
B $1E09,1
c $1E27 THE 'DATA' COMMAND ROUTINE
c $1E39 THE 'PASS-BY' SUBROUTINE
c $1E42 THE 'RESTORE' COMMAND ROUTINE
c $1E4F THE 'RANDOMIZE' COMMAND ROUTINE
c $1E5F THE 'CONTINUE' COMMAND ROUTINE
c $1E67 THE 'GO TO' COMMAND ROUTINE
c $1E7A THE 'OUT' COMMAND ROUTINE
c $1E80 THE 'POKE' COMMAND ROUTINE
c $1E85 THE 'TWO-PARAM' SUBROUTINE
c $1E94 THE 'FIND INTEGERS' SUBROUTINE
B $1EA0,1
c $1EA1 THE 'RUN' COMMAND ROUTINE
c $1EAC THE 'CLEAR' COMMAND ROUTINE
B $1EDB,1
c $1EED THE 'GO SUB' COMMAND ROUTINE
c $1F05 THE 'TEST-ROOM' SUBROUTINE
c $1F1A THE 'FREE MEMORY' SUBROUTINE
c $1F23 THE 'RETURN' COMMAND ROUTINE
B $1F39,1
c $1F3A THE 'PAUSE' COMMAND ROUTINE
c $1F54 THE 'BREAK-KEY' SUBROUTINE
c $1F60 THE 'DEF FN' COMMAND ROUTINE
c $1FC3 THE 'UNSTACK-Z' SUBROUTINE
c $1FC9 THE 'LPRINT & PRINT' COMMAND ROUTINES
c $1FF5 THE 'PRINT A CARRIAGE RETURN' SUBROUTINE
c $1FFC THE 'PRINT ITEMS' SUBROUTINE
c $2045 THE 'END OF PRINTING' SUBROUTINE
c $204E THE 'PRINT POSITION' SUBROUTINE
c $2070 THE 'ALTER STREAM' SUBROUTINE
c $2089 THE 'INPUT' COMMAND ROUTINE
c $21B9 THE 'IN-ASSIGN' SUBROUTINE
B $21CF,1
B $21D5,1
c $21D6 THE 'IN-CHAN-K' SUBROUTINE
c $21E1 THE 'COLOUR ITEM' ROUTINES
B $2245,1
c $226C THE 'CO-CHANGE' SUBROUTINE
c $2294 THE 'BORDER' COMMAND ROUTINE
c $22AA THE 'PIXEL ADDRESS' SUBROUTINE
c $22CB THE 'POINT' SUBROUTINE
c $22DC THE 'PLOT' COMMAND ROUTINE
c $2307 THE 'STK-TO-BC' SUBROUTINE
c $2314 THE 'STK-TO-A' SUBROUTINE
c $2320 THE CIRCLE COMMAND ROUTINE
B $232E,3,1
B $2337,2,1
B $233C,2,1
B $2341,3,1
B $2349,4,1
B $2353,3,1
B $235B,19,1
c $2382 THE DRAW COMMAND ROUTINE
B $2395,11,1
B $23A3,18,1
B $23BB,3,1
B $23C6,55,1
B $2406,2,1
B $240F,4,1
B $241A,5,1
B $2426,19,1
B $243B,6,1
B $2448,8,1
B $2457,2,1
B $2460,4,1
B $246B,3,1
B $2475,2,1
c $247D THE 'INITIAL PARAMETERS' SUBROUTINE
B $247E,12,1
B $249C,25,1
c $24B7 THE LINE-DRAWING SUBROUTINE
B $24FA,1
c $24FB THE 'SCANNING' SUBROUTINE
c $2530 THE 'SYNTAX-Z' SUBROUTINE
b $2596 THE SCANNING FUNCTION TABLE
c $25AF THE SCANNING FUNCTION ROUTINES
B $2605,18,1*9,3,1
B $262D,2,1
c $26C9 THE SCANNING VARIABLE ROUTINE
B $2757,2,1
b $2795 THE TABLE OF OPERATORS
b $27B0 THE TABLE OF PRIORITIES
c $27BD THE 'SCANNING FUNCTION' SUBROUTINE
B $2813,1
B $288C,1
c $28AB THE 'FUNCTION SKIPOVER' SUBROUTINE
c $28B2 THE 'LOOK-VARS' SUBROUTINE
c $2951 THE 'STACK FUNCTION ARGUMENT' SUBROUTINE
c $2996 THE 'STK-VAR' SUBROUTINE
B $2A21,1
c $2A52 THE 'SLICING' SUBROUTINE
c $2AB1 THE 'STK-STORE' SUBROUTINE
c $2ACC THE 'INT-EXP' SUBROUTINE
c $2AEE THE 'DE,(DE+1)' SUBROUTINE
c $2AF4 THE 'GET-HL*DE' SUBROUTINE
c $2AFF THE 'LET' COMMAND ROUTINE
B $2B5B,2,1
c $2BA6 THE 'L-ENTER' SUBROUTINE
c $2BAF THE LET SUBROUTINE CONTINUES HERE
c $2BC6 THE 'L-STRING' SUBROUTINE
c $2BEA THE 'L-FIRST' SUBROUTINE
c $2BF1 THE 'STK-FETCH' SUBROUTINE
c $2C02 THE 'DIM' COMMAND ROUTINE
c $2C88 THE 'ALPHANUM' SUBROUTINE
c $2C8D THE 'ALPHA' SUBROUTINE
c $2C9B THE 'DECIMAL TO FLOATING POINT' SUBROUTINE
B $2CD3,2,1
B $2CD6,4,1
B $2CE1,7,1
c $2D1B THE 'NUMERIC' SUBROUTINE
c $2D22 THE 'STK-DIGIT' SUBROUTINE
c $2D28 THE 'STACK-A' SUBROUTINE
c $2D2B THE 'STACK-BC' SUBROUTINE
B $2D38,1
c $2D3B THE 'INTEGER TO FLOATING-POINT' SUBROUTINE
B $2D3D,2,1
B $2D45,5,1
c $2D4F THE 'E-FORMAT TO FLOATING-POINT' SUBROUTINE
B $2D5D,2,1
B $2D66,10,1
B $2D75,3,1
B $2D7C,2,1
c $2D7F THE 'INT-FETCH' SUBROUTINE
c $2D8C THE 'INT-STORE' SUBROUTINE
c $2DA2 THE 'FLOATING-POINT TO BC' SUBROUTINE
B $2DA3,1
B $2DA9,4,1
B $2DAE,2,1
c $2DC1 THE 'LOG(2#CHR(8593)A)' SUBROUTINE
B $2DCC,9,1*2,4,1
c $2DD5 THE 'FLOATING-POINT TO A' SUBROUTINE
c $2DE3 THE 'PRINT A FLOATING-POINT NUMBER' SUBROUTINE
B $2DE4,10,1
B $2DF2,2,1
B $2DF8,6,1
B $2E02,9,1
B $2E25,2,1
B $2E3A,6,1
B $2ECC,3,1
B $2F31,2,1
c $2F8B THE 'CA=10*A+C' SUBROUTINE
c $2F9B THE 'PREPARE TO ADD' SUBROUTINE
c $2FBA THE 'FETCH TWO NUMBERS' SUBROUTINE
c $2FDD THE 'SHIFT ADDEND' SUBROUTINE
c $3004 THE 'ADD-BACK' SUBROUTINE
c $300F THE 'SUBTRACTION' OPERATION
c $3014 THE 'ADDITION' OPERATION
c $30A9 THE 'HL=HL*DE' SUBROUTINE
c $30C0 THE 'PREPARE TO MULTIPLY OR DIVIDE' SUBROUTINE
c $30CA THE 'MULTIPLICATION' OPERATION
B $31AE,1
c $31AF THE 'DIVISION' OPERATION
c $3214 THE 'INTEGER TRUNCATION TOWARDS ZERO' SUBROUTINE
c $3293 THE 'RE-STACK TWO' SUBROUTINE
c $3297 THE 'RE-STACK' SUBROUTINE
b $32C5 THE TABLE OF CONSTANTS
b $32D7 THE TABLE OF ADDRESSES
c $335B THE 'CALCULATE' SUBROUTINE
c $33A2 THE 'SINGLE OPERATION' SUBROUTINE
c $33A9 THE 'TEST 5-SPACES' SUBROUTINE
c $33B4 THE 'STACK NUMBER' SUBROUTINE
c $33C0 THE 'MOVE A FLOATING-POINT NUMBER' SUBROUTINE
c $33C6 THE 'STACK LITERALS' SUBROUTINE
c $33F7 THE 'SKIP CONSTANTS' SUBROUTINE
c $3406 THE 'MEMORY LOCATION' SUBROUTINE
c $340F THE 'GET FROM MEMORY AREA' SUBROUTINE
c $341B THE 'STACK A CONSTANT' SUBROUTINE
c $342D THE 'STORE IN MEMORY AREA' SUBROUTINE
c $343C THE 'EXCHANGE' SUBROUTINE
c $3449 THE 'SERIES GENERATOR' SUBROUTINE
c $346A THE 'ABSOLUTE MAGNITUDE' FUNCTION
c $346E THE 'UNARY MINUS' OPERATION
c $3492 THE 'SIGNUM' FUNCTION
c $34A5 THE 'IN' FUNCTION
c $34AC THE 'PEEK' FUNCTION
c $34B3 THE 'USR' FUNCTION
c $34BC THE 'USR STRING' FUNCTION
B $34E8,1
c $34E9 THE 'TEST-ZERO' SUBROUTINE
c $34F9 THE 'GREATER THAN ZERO' OPERATION
c $3501 THE 'NOT' FUNCTION
c $3506 THE 'LESS THAN ZERO' OPERATION
c $350B THE 'ZERO OR ONE' SUBROUTINE
c $351B THE 'OR' OPERATION
c $3524 THE 'NUMBER AND NUMBER' OPERATION
c $352D THE 'STRING AND NUMBER' OPERATION
c $353B THE 'COMPARISON' OPERATIONS
B $358A,2,1
c $359C THE 'STRING CONCATENATION' OPERATION
c $35BF THE 'STK-PNTRS' SUBROUTINE
c $35C9 THE 'CHR$' FUNCTION
B $35DD,1
c $35DE THE 'VAL' AND 'VAL$' FUNCTION
c $361F THE 'STR$' FUNCTION
c $3645 THE 'READ-IN' SUBROUTINE
c $3669 THE 'CODE' FUNCTION
c $3674 THE 'LEN' FUNCTION
c $367A THE 'DECREASE THE COUNTER' SUBROUTINE
c $3686 THE 'JUMP' SUBROUTINE
c $368F THE 'JUMP ON TRUE' SUBROUTINE
c $369B THE 'END-CALC' SUBROUTINE
c $36A0 THE 'MODULUS' SUBROUTINE
B $36A1,13,1
c $36AF THE 'INT' FUNCTION
B $36B0,6,1
B $36B7,12,1
c $36C4 THE 'EXPONENTIAL' FUNCTION
B $36C5,52,1*3,4,1*13,2,1,3,1,3,1,4,1,4,1,4,1,4,1
B $3704,1
B $370F,3,1
c $3713 THE 'NATURAL LOGARITHM' FUNCTION
B $3714,6,1
B $371B,4,1
B $3726,21,1*8,4,1
B $373D,69,1*3,4,1*19,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1
c $3783 THE 'REDUCE ARGUMENT' SUBROUTINE
B $3784,28,1*3,4,1
B $37A1,8,1
c $37AA THE 'COSINE' FUNCTION
B $37AB,10,1
c $37B5 THE 'SINE' FUNCTION
B $37B6,35,1*12,2,1,3,1,4,1,4,1,4,1
c $37DA THE 'TAN' FUNCTION
B $37DB,6,1
c $37E2 THE 'ARCTAN' FUNCTION
B $37EB,13,1
B $37F9,57,1*15,2,1,2,1,2,1,3,1,3,1,2,1,4,1,4,1,4,1,4,1
c $3833 THE 'ARCSIN' FUNCTION
B $3834,14,1
c $3843 THE 'ARCCOS' FUNCTION
B $3844,5,1
c $384A THE 'SQUARE ROOT' FUNCTION
B $384B,6,1
c $3851 THE 'EXPONENTIATION' OPERATION
B $3852,8,1
B $385D,16,1
u $386E
b $3D00 Character set
  $3D00,8,b1 #UDG$3D00
  $3D08,8,b1 #UDG$3D08
  $3D10,8,b1 #UDG$3D10
  $3D18,8,b1 #UDG$3D18
  $3D20,8,b1 #UDG$3D20
  $3D28,8,b1 #UDG$3D28
  $3D30,8,b1 #UDG$3D30
  $3D38,8,b1 #UDG$3D38
  $3D40,8,b1 #UDG$3D40
  $3D48,8,b1 #UDG$3D48
  $3D50,8,b1 #UDG$3D50
  $3D58,8,b1 #UDG$3D58
  $3D60,8,b1 #UDG$3D60
  $3D68,8,b1 #UDG$3D68
  $3D70,8,b1 #UDG$3D70
  $3D78,8,b1 #UDG$3D78
  $3D80,8,b1 #UDG$3D80
  $3D88,8,b1 #UDG$3D88
  $3D90,8,b1 #UDG$3D90
  $3D98,8,b1 #UDG$3D98
  $3DA0,8,b1 #UDG$3DA0
  $3DA8,8,b1 #UDG$3DA8
  $3DB0,8,b1 #UDG$3DB0
  $3DB8,8,b1 #UDG$3DB8
  $3DC0,8,b1 #UDG$3DC0
  $3DC8,8,b1 #UDG$3DC8
  $3DD0,8,b1 #UDG$3DD0
  $3DD8,8,b1 #UDG$3DD8
  $3DE0,8,b1 #UDG$3DE0
  $3DE8,8,b1 #UDG$3DE8
  $3DF0,8,b1 #UDG$3DF0
  $3DF8,8,b1 #UDG$3DF8
  $3E00,8,b1 #UDG$3E00
  $3E08,8,b1 #UDG$3E08
  $3E10,8,b1 #UDG$3E10
  $3E18,8,b1 #UDG$3E18
  $3E20,8,b1 #UDG$3E20
  $3E28,8,b1 #UDG$3E28
  $3E30,8,b1 #UDG$3E30
  $3E38,8,b1 #UDG$3E38
  $3E40,8,b1 #UDG$3E40
  $3E48,8,b1 #UDG$3E48
  $3E50,8,b1 #UDG$3E50
  $3E58,8,b1 #UDG$3E58
  $3E60,8,b1 #UDG$3E60
  $3E68,8,b1 #UDG$3E68
  $3E70,8,b1 #UDG$3E70
  $3E78,8,b1 #UDG$3E78
  $3E80,8,b1 #UDG$3E80
  $3E88,8,b1 #UDG$3E88
  $3E90,8,b1 #UDG$3E90
  $3E98,8,b1 #UDG$3E98
  $3EA0,8,b1 #UDG$3EA0
  $3EA8,8,b1 #UDG$3EA8
  $3EB0,8,b1 #UDG$3EB0
  $3EB8,8,b1 #UDG$3EB8
  $3EC0,8,b1 #UDG$3EC0
  $3EC8,8,b1 #UDG$3EC8
  $3ED0,8,b1 #UDG$3ED0
  $3ED8,8,b1 #UDG$3ED8
  $3EE0,8,b1 #UDG$3EE0
  $3EE8,8,b1 #UDG$3EE8
  $3EF0,8,b1 #UDG$3EF0
  $3EF8,8,b1 #UDG$3EF8
  $3F00,8,b1 #UDG$3F00
  $3F08,8,b1 #UDG$3F08
  $3F10,8,b1 #UDG$3F10
  $3F18,8,b1 #UDG$3F18
  $3F20,8,b1 #UDG$3F20
  $3F28,8,b1 #UDG$3F28
  $3F30,8,b1 #UDG$3F30
  $3F38,8,b1 #UDG$3F38
  $3F40,8,b1 #UDG$3F40
  $3F48,8,b1 #UDG$3F48
  $3F50,8,b1 #UDG$3F50
  $3F58,8,b1 #UDG$3F58
  $3F60,8,b1 #UDG$3F60
  $3F68,8,b1 #UDG$3F68
  $3F70,8,b1 #UDG$3F70
  $3F78,8,b1 #UDG$3F78
  $3F80,8,b1 #UDG$3F80
  $3F88,8,b1 #UDG$3F88
  $3F90,8,b1 #UDG$3F90
  $3F98,8,b1 #UDG$3F98
  $3FA0,8,b1 #UDG$3FA0
  $3FA8,8,b1 #UDG$3FA8
  $3FB0,8,b1 #UDG$3FB0
  $3FB8,8,b1 #UDG$3FB8
  $3FC0,8,b1 #UDG$3FC0
  $3FC8,8,b1 #UDG$3FC8
  $3FD0,8,b1 #UDG$3FD0
  $3FD8,8,b1 #UDG$3FD8
  $3FE0,8,b1 #UDG$3FE0
  $3FE8,8,b1 #UDG$3FE8
  $3FF0,8,b1 #UDG$3FF0
  $3FF8,8,b1 #UDG$3FF8
i $4000
