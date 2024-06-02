import argparse

def sign(n):
  return -1 if n < 0 else +1

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("--precision", help="specify decimal precision to use", action="store", default=2, type=int)

  parser.add_argument("amount", help="amount that has to be divided across periods", type=float)
  parser.add_argument("periods", help="number of periods", type=int)

  args = parser.parse_args()

  amount = round(args.amount * 10**args.precision)
  periods = args.periods

  periodic_amount = round(amount / periods)
  offshoot = periodic_amount * periods - amount

  periodic_amount += abs(offshoot) // periods
  offshoot = abs(offshoot) % periods

  gap = ((periods - offshoot) // offshoot) if offshoot != 0 else 0

  running_sum = 0
  for period in range(periods):
    if offshoot != 0 and period % gap == 0:
      print("{}".format((periodic_amount + 1) / 100))

      offshoot -= 1 * sign(offshoot)
      running_sum += periodic_amount - 1 * sign(offshoot)
    else:
      print(f"{periodic_amount / 100:.{args.precision}f}")
      running_sum += periodic_amount

if __name__ == "__main__":
  main()