# hledger-accrue

This is a Python 3 script that takes an amount and a bunch of params which it uses to generate multiple transactions that add up to the original amount. This is useful for accruing expenses.

## Requirements

Make sure you have a working installation of Python 3.

## Installation

Clone the repo

```sh
git clone https://github.com/victormihalache/hledger-accrue.git
```

`cd` into the directory

```sh
cd hledger-accrue
```

Alternatively, just copy this:

```sh
git clone https://github.com/victormihalache/hledger-accrue.git
cd hledger-accrue
```

## Usage

```txt
usage: main.py [-h] [--precision PRECISION] [--from FROM] [--to TO] --start
               START --end END --commodity COMMODITY
               [--description DESCRIPTION] [--real | --periodic]
               amount

positional arguments:
  amount                amount that has to be divided across periods

options:
  -h, --help            show this help message and exit
  --precision PRECISION
                        specify decimal precision to use
  --from FROM, -f FROM  specify the account from which to take out funds
  --to TO, -t TO        specify the account to which to move funds to
  --start START, -s START
                        specify the starting date
  --end END, -e END     specify the ending date
  --commodity COMMODITY, -c COMMODITY
                        specify the commodity to use
  --description DESCRIPTION, -d DESCRIPTION
                        specify the description to use for each transaction
  --real, -R            use real transactions
  --periodic, -P        use periodic transactions
```

### Examples

Take rent for January and accrue it for every day of the month:

```sh
python3 main.py 400 --start 2024-01-01 --end 2024-02-01 --commodity EUR --description "Pay rent" -R --to "expenses:rent"
```

## Roadmap

- [ ] Accrue for different periods, not just daily
- [ ] Custom date formats
- [ ] Allow setting for transaction status (unmarked, pending, cleared)
- [ ] Use smart dates similar to hledger's
