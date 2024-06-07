import argparse
import datetime


def sign(n):
    return -1 if n < 0 else +1


def split_amount(amount: int, tranches: int):
    periodic_amount = round(amount / tranches)
    offshoot = periodic_amount * tranches - amount

    periodic_amount += abs(offshoot) // tranches
    offshoot = abs(offshoot) % tranches

    if offshoot != 0:
        gap = (tranches - offshoot) // offshoot

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

    parser.add_argument(
        "amount", help="amount that has to be divided across periods", type=float
    )

    parser.add_argument(
        "--precision",
        help="specify decimal precision to use",
        action="store",
        default=2,
        type=int,
    )

    parser.add_argument(
        "--from",
        "-f",
        help="specify the account from which to take out funds",
        action="store",
        type=str,
        default="assets:prepaid expenses",
    )

    parser.add_argument(
        "--to",
        "-t",
        help="specify the account to which to move funds to",
        action="store",
        type=str,
        default="expenses",
    )

    parser.add_argument(
        "--start",
        "-s",
        help="specify the starting date",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        required=True,
    )

    parser.add_argument(
        "--end",
        "-e",
        help="specify the ending date",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        required=True,
    )

    parser.add_argument(
        "--commodity",
        "-c",
        help="specify the commodity to use",
        action="store",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--description",
        "-d",
        help="specify the description to use for each transaction",
        action="store",
        type=str,
        default="",
    )

    realToggle = parser.add_mutually_exclusive_group()
    realToggle.add_argument(
        "--real", "-R", action="store_true", help="use real transactions"
    )
    realToggle.add_argument(
        "--periodic",
        "-P",
        action="store_false",
        help="use periodic transactions",
    )

    # TODO: Allow user to choose custom date format for input date
    # TODO: Allow user to choose custom date format for output date

    args = parser.parse_args()

    amount = round(args.amount * 10**args.precision)

    if args.end > args.start:
        tranches = (args.end - args.start).days
    else:
        parser.error("The end date must be greater than the ending date")

    output_tranches = split_amount(amount, tranches)

    if args.real:
        for tnx, tranche in enumerate(output_tranches):
            print(
                f"{datetime.datetime.strftime(args.start + datetime.timedelta(tnx), '%Y-%m-%d')}{' ' + args.description if args.description != '' else ''}"
            )
            print(f"  {getattr(args, 'from')}  -{tranche} {args.commodity}")
            print(f"  {getattr(args, 'to')}  {tranche} {args.commodity}")
            print()
    else:
        for tnx, tranche in enumerate(output_tranches):
            print(
                f"~ {datetime.datetime.strftime(args.start + datetime.timedelta(tnx), '%Y-%m-%d')}{'  ' + args.description if args.description != '' else ''}"
            )
            print(f"  {getattr(args, 'from')}  -{tranche} {args.commodity}")
            print(f"  {getattr(args, 'to')}  {tranche} {args.commodity}")
            print()


if __name__ == "__main__":
    main()
