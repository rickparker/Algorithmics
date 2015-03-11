def expmod(base, power, modulus):
  if modulus <= 0: return 1
  if power == 0: return 1

  z = expmod(base, power/2, modulus)
  if power & 1 == 0:
    return (z * z) % modulus
  else:
    return base * (z * z) % modulus

print expmod(5, 30000, 31)  ## Expect result 1
print expmod(6, 123456, 31)  ## Expect result 1
print expmod(4, 2006, 3)    ## Expect result 1
print expmod(808017424794512875886459904961710757005754368000000000, 808017424794512875886459904961710757005754368000000000, 2015)  ## Expect result 0
