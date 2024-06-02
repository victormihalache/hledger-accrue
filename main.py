import argparse
import datetime
import calendar

def sign(n):
  return -1 if n < 0 else +1

def split_amount(amount: int, tranches: int):
  periodic_amount = round(amount / tranches)
  offshoot = periodic_amount * tranches - amount

  periodic_amount += abs(offshoot) // tranches

  offshoot = (abs(offshoot) % tranches)

  gap = ((tranches - offshoot) // offshoot) if offshoot != 0 else 0

  resulting_tranches = []
  for period in range(tranches):
    if offshoot != 0 and period % gap == 0:
      resulting_tranches.append((periodic_amount - 1 * sign(offshoot)) / 100)

      offshoot -= sign(offshoot)
    else:
      resulting_tranches.append(periodic_amount / 100)

  return resulting_tranches

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("amount", help="amount that has to be divided across periods", type=float)

  parser.add_argument("--precision", help="specify decimal precision to use", action="store", default=2, type=int)

  parser.add_argument("--from", "-f", help="specify the account from which to take out funds", action="store", type=str, required=True)
  parser.add_argument("--to", "-t", help="specify the account to which to move funds to", action="store", type=str, required=True)

  parser.add_argument("--start", "-s", help="specify the starting date", type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"), required=True)
  parser.add_argument("--end", "-e", help="specify the ending date", type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"), required=True)
  # TODO: Allow user to choose custom date format

  args = parser.parse_args()

  amount = round(args.amount * 10**args.precision)

  if args.end > args.start:
    tranches = (args.end - args.start).days
  else:
    parser.error('The end date must be greater than the ending date')
  
  print(split_amount(amount, tranches))

if __name__ == "__main__":
  main()