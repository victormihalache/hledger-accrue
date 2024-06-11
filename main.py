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
    class CustomHelpFormatter(argparse.HelpFormatter):
        def __init__(self, prog, indent_increment=2, max_help_position=80, width=160):
            super().__init__(prog, indent_increment, max_help_position, width)

    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)

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

    dateRange = parser.add_argument_group("date range manipulation")

    dateRange.add_argument(
        "--accrual-start",
        "-s",
        help="specify the date from which to start accruing the amount",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        required=True,
    )

    dateRange.add_argument(
        "--accrual-end",
        "-e",
        help="specify the date at which to stop accruing the amount",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        required=True,
    )

    dateRange.add_argument(
        "--reporting-start",
        help="specify the date from which to start reporting transactions",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
    )

    dateRange.add_argument(
        "--reporting-end",
        help="specify the date at which to stop reporting transactions",
        action="store",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
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
        "-p",
        action="store_false",
        help="use periodic transactions",
    )

    statusToggle = parser.add_mutually_exclusive_group()
    statusToggle.add_argument(
        "--unmarked",
        "-U",
        action="store_true",
        help='mark every transaction as "unmarked"',
    )
    statusToggle.add_argument(
        "--pending",
        "-P",
        action="store_true",
        help='mark every transaction as "pending"',
    )
    statusToggle.add_argument(
        "--cleared",
        "-C",
        action="store_true",
        help='mark every transaction as "cleared"',
    )

    # TODO: Allow user to choose custom date format for input date
    # TODO: Allow user to choose custom date format for output date

    args = parser.parse_args()

    if args.accrual_end > args.accrual_start:
        tranches = (args.accrual_end - args.accrual_start).days
    else:
        parser.error("The end date must be greater than the ending date")

    if args.reporting_start:
        if args.reporting_start < args.accrual_start:
            parser.error(
                "The reporting start date must not come before the accruing start date"
            )
    else:
        args.reporting_start = args.accrual_start

    if args.reporting_end:
        if args.reporting_end > args.accrual_end:
            parser.error(
                "The reporting end date must not come after the accruing end date"
            )
    else:
        args.reporting_end = args.accrual_end

    amount = round(args.amount * 10**args.precision)

    output_tranches = split_amount(amount, tranches)

    if args.unmarked or args.pending or args.cleared:
        if not args.description:
            parser.error(
                "Transaction status can only be set when the description is also set"
            )
        elif not args.real:
            parser.error("Transaction status can only be set for real transactions")

    if args.description:
        description = " " + args.description

        if args.unmarked:
            status = ""
        elif args.pending:
            status = " !"
        elif args.cleared:
            status = " *"
        else:
            status = ""
    else:
        description = ""

    fromAccount = getattr(args, "from")
    toAccount = getattr(args, "to")

    if args.real:
        for tnx, tranche in enumerate(output_tranches):
            date = datetime.datetime.strftime(
                args.accrual_start + datetime.timedelta(tnx), "%Y-%m-%d"
            )

            if not (
                args.reporting_start
                <= datetime.datetime.strptime(date, "%Y-%m-%d")
                <= args.reporting_end
            ):
                continue

            print(f"{date}{status}{description}")
            print(f"  {fromAccount}  -{tranche} {args.commodity}")
            print(f"  {toAccount}  {tranche} {args.commodity}")
            print()
    else:
        for tnx, tranche in enumerate(output_tranches):
            date = datetime.datetime.strftime(
                args.accrual_start + datetime.timedelta(tnx), "%Y-%m-%d"
            )

            if not (
                args.reporting_start
                <= datetime.datetime.strptime(date, "%Y-%m-%d")
                <= args.reporting_end
            ):
                continue

            print(f"~ {date}{description}")
            print(f"  {getattr(args, 'from')}  -{tranche} {args.commodity}")
            print(f"  {getattr(args, 'to')}  {tranche} {args.commodity}")
            print()


if __name__ == "__main__":
    main()
