import random

def check(n,l):
    out = []
    for i in l:
        if i not in out:
            out.append(i)
        else:
            return False
    out.clear()        
    return True

def primitive(n):
    l= []
    tot = 0
    roots = []
    for i in range(1,n):
        for j in range(1,n):
            t = (pow(i,j))%n
            l.append(t)
        if(check(n,l)):
            tot = tot + 1
            roots.append(i)
        l.clear()        
    return random.choice(roots)

def RandomPrime():
  while True:
    n = random.randint(1, 100)
    if n % 2 == 0:
      continue
    prime = True
    for x in range(3, int(n**0.5 + 1), 2):
      if n % x == 0:
        prime = False
        break; 
    if prime: 
      return n