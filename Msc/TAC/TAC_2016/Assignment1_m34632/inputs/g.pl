fun(g, [arg(n, int)],
  body([
      var(id(s,local,real), toreal(int_literal(0): int): real)
    ], 
    while(
      ge(id(n,arg,int): int, int_literal(1): int): bool, [
        assign(id(s,local,real),
          plus(id(s,local,real): real,
            toreal(id(n,arg,int): int): real): real),
        assign(id(n,arg,int),
          minus(id(n,arg,int): int, int_literal(1): int): int)
      ]),
    id(s,local,real): real)).
