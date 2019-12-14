print(sum((lambda f, x: f(f, x))(lambda f, x: x // 3 - 2 + f(f, x // 3 - 2) if x > 5 else 0, int(l)) for l in open("part1_input.txt")))
