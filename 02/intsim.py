#!/usr/bin/env python3

import sys

def run(mem):
	mem = mem[:]
	pc = 0
	while mem[pc] != 99:
		if mem[pc] == 1:
			mem[mem[pc + 3]] = mem[mem[pc + 1]] + mem[mem[pc + 2]]
		elif mem[pc] == 2:
			mem[mem[pc + 3]] = mem[mem[pc + 1]] * mem[mem[pc + 2]]
		else:
			raise ValueError("Invalid opcode {} @{}".format(mem[pc], pc))
		pc += 4
	return mem

print(",".join(str(x) for x in run(list(int(x) for x in open(sys.argv[1]).read().split(",")))))
