Part 2
======

This is the program from part 1:

```
1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,5,19,23,1,13,23,27,1,6,27,31,2,31,13,35,1,9,35,39,2,39,13,43,1,43,10,47,1,47,13,51,2,13,51,55,1,55,9,59,1,59,5,63,1,6,63,67,1,13,67,71,2,71,10,75,1,6,75,79,1,79,10,83,1,5,83,87,2,10,87,91,1,6,91,95,1,9,95,99,1,99,9,103,2,103,10,107,1,5,107,111,1,9,111,115,2,13,115,119,1,119,10,123,1,123,10,127,2,127,10,131,1,5,131,135,1,10,135,139,1,139,2,143,1,6,143,0,99,2,14,0,0
```
Task is to find two integers a, b, from 0...99 inclusive, which will result in the value `19690720` being written to location `0`, if a and b are present at locations `1` and `2`. This is a small enough space to be brute forced, but let's take this as an opportunity to get better at Intcode programming, and try to understand the above program. I will list each instruction on its own line, and begin each line with the base address of that instruction (all in decimal). Comments are indicated by the `;` character, and run to the end of the line.

```
0:   1, 0,   0,   3,
4:   1, 1,   2,   3,
8:   1, 3,   4,   3,
12:  1, 5,   0,   3,
16:  2, 6,   1,   19,
20:  1, 5,   19,  23,
24:  1, 13,  23,  27,
28:  1, 6,   27,  31,
32:  2, 31,  13,  35,
36:  1, 9,   35,  39,
40:  2, 39,  13,  43,
44:  1, 43,  10,  47,
48:  1, 47,  13,  51,
52:  2, 13,  51,  55,
56:  1, 55,  9,   59,
60:  1, 59,  5,   63,
64:  1, 6,   63,  67,
68:  1, 13,  67,  71,
72:  2, 71,  10,  75,
76:  1, 6,   75,  79,
80:  1, 79,  10,  83,
84:  1, 5,   83,  87,
88:  2, 10,  87,  91,
92:  1, 6,   91,  95,
96:  1, 9,   95,  99,
100: 1, 99,  9,   103,
104: 2, 103, 10,  107,
108: 1, 5,   107, 111,
112: 1, 9,   111, 115,
116: 2, 13,  115, 119,
120: 1, 119, 10,  123,
124: 1, 123, 10,  127,
128: 2, 127, 10,  131,
132: 1, 5,   131, 135,
136: 1, 10,  135, 139,
140: 1, 139, 2,   143,
144: 1, 6,   143, 0,
148: 99,
149: 2,14,0,0
```

Key observations:

- Store addresses are always less than or equal to instruction address + 3. We know from the examples in part 1 that Intcode machines load the entire instruction before executing it. Consequently, each instruction will be executed as written, unaffected by earlier instructions.
- The use of data `@1` and `@2` as addresses by instruction `@0` is immediately squashed by their use as constants by instruction `@4`
- The inputs `@1` and `@2` are never overwritten
- Generally the output of one instruction is used exactly once, by the next instruction

With this we can more easily annotate the flow of this program. We will use `@x` to refer to the contents of memory at address `x`, `<-` to denote assignment, and `=` in the algebraic sense. The results will probably look something like three-address-code.

```
0:   1, a,   b,   3,     ; NOP because result is immediately squashed
4:   1, 1,   2,   3,     ; add a and b, store at location 3
8:   1, 3,   4,   3,     ; increment @3 by 1
12:  1, 5,   0,   3,     ; @3 <- @5 + @0 = 2 (squash all previous results) (this is never used either!)
16:  2, 6,   1,   19,    ; @19 <- a * 2
20:  1, 5,   19,  23,    ; @23 <- @19 + @5 = 2 * a + 1
24:  1, 13,  23,  27,    ; @27 <- @13 + @23 = (5) + (2 * a + 1) = 2 * a + 6
28:  1, 6,   27,  31,    ; @31 <- @6 + @27 = 2 + @27 = 2 * a + 8 
32:  2, 31,  13,  35,    ; @35 <- @31 * @13 = 5 * (2 * a + 8) = 10 * a + 40
36:  1, 9,   35,  39,    ; @39 <- @35 + @9 = (10 * a + 40) + 3 = 10 * a + 43
40:  2, 39,  13,  43,    ; @43 <- @39 * @13 = 5 * @39 = 50 * a + 215
44:  1, 43,  10,  47,    ; @47 <- @43 + @10 = @43 + 4 = 50 * a + 219
48:  1, 47,  13,  51,    ; @51 <- @47 + @13 = @47 + 5 = 50 * a + 224
52:  2, 13,  51,  55,    ; @55 <- @51 * 5 = 250 * a + 1120
56:  1, 55,  9,   59,    ; @59 <- @55 + @9 = @55 + 3 = 250 * a + 1123
60:  1, 59,  5,   63,    ; @63 <- @59 + @5 = 250 * a + 1124
64:  1, 6,   63,  67,    ; @67 <- @63 + @6 = 250 * a + 1126
68:  1, 13,  67,  71,    ; @71 <- @67 + @13 = 250 * a + 1131
72:  2, 71,  10,  75,    ; @75 <- @71 * @10 = (250 * a + 1131) * 4 = 1000 * a + 4524
76:  1, 6,   75,  79,    ; @79 <- @75 + @6 = 1000 * a + 4526
80:  1, 79,  10,  83,    ; @83 <- @79 + @10 = 1000 * a + 4530
84:  1, 5,   83,  87,    ; @87 <- @83 + @5 = 1000 * a + 4531
88:  2, 10,  87,  91,    ; @91 <- @87 * @10 = 4000 * a + 18124
92:  1, 6,   91,  95,    ; @95 <- @91 + @6 = 4000 * a + 18126
96:  1, 9,   95,  99,    ; @99 <- @95 + @9 = 4000 * a + 18129
100: 1, 99,  9,   103,   ; @103 <- @99 + @9 = 4000 * a + 18132
104: 2, 103, 10,  107,   ; @107 <- @103 * @10 = @103 * 4 = 16000 * a + 72528
108: 1, 5,   107, 111,   ; @111 <- @107 + 1 = 16000 * a + 72529
112: 1, 9,   111, 115,   ; @115 <- @111 + 3 = 16000 * a + 72532
116: 2, 13,  115, 119,   ; @119 <- @115 * 5 = 80_000 * a + 362_660
120: 1, 119, 10,  123,   ; @123 <- @119 + @10 = 80_000 * a + 362_664
124: 1, 123, 10,  127,   ; @127 <- @123 + @10 = 80_000 * a + 362_668
128: 2, 127, 10,  131,   ; @131 <- @127 * @10 = 320_000 * a + 1_450_672
132: 1, 5,   131, 135,   ; @135 <- @131 + @5 = @131 + 1 = 320_000 * a + 1_450_673
136: 1, 10,  135, 139,   ; @139 <- @135 + @10 = @135 + 4 = 320_000 * a + 1_450_677
140: 1, 139, 2,   143,   ; @143 <- @139 + @2 = 320_000 * a + b + 1_450_677
144: 1, 6,   143, 0,     ; @0 <- @143 + 2 = 320_000 * a + b + 1_450_679
148: 99,                 ; Halt
149: 2,14,0,0            ; Garbage at end of program
```

So this program takes two integes a, b and calculates the result 320000 * a + b + 1450679. We can test our expression by substituting our input from part 1: a = 12, b = 2 should yield a result of 5290681. Helpfully, the `a` multiplier has a large power of 10 as one of its factors, so `a` does not affect the 4 LSDs of the result.

Our target output is 19690720. Subtracting the constant offset, this gives 320000 * a + b = 18240041. This yields b = 41, and a = 57.


