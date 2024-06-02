import argparse

def sign(n):
  return -1 if n < 0 else +1

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("amount", help="amount that has to be divided across periods", type=float)

  parser.add_argument("--precision", help="specify decimal precision to use", action="store", default=2, type=int)

  periodic = parser.add_argument_group("by tranches")
  periodic.add_argument("--tranches", "-t", help="specify the amount of periods to divide the amount by", type=int)

  dated = parser.add_argument_group("by date range")
  dated.add_argument("--start", "-s", help="specify the starting date")
  dated.add_argument("--end", "-e", help="specify the ending date")
  dated.add_argument("--period", "-p", help="specify the periodicity to use to calculate tranches in date range")

  args = parser.parse_args()

  print(args)

  amount = round(args.amount * 10**args.precision)
  tranches = args.tranches

  periodic_amount = round(amount / tranches)
  offshoot = periodic_amount * tranches - amount

  periodic_amount += abs(offshoot) // tranches

  print(offshoot)
  offshoot = (abs(offshoot) % tranches)
  print(offshoot)

  gap = ((tranches - offshoot) // offshoot) if offshoot != 0 else 0

  running_sum = 0
  for period in range(tranches):
    if offshoot != 0 and period % gap == 0:
      print("{}".format((periodic_amount - 1 * sign(offshoot)) / 100))

      running_sum += periodic_amount - 1 * sign(offshoot)
      offshoot -= sign(offshoot)
    else:
      print(f"{periodic_amount / 100:.{args.precision}f}")
      running_sum += periodic_amount

  print (running_sum)
  print (amount)

if __name__ == "__main__":
  main()