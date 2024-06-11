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
usage: main.py [-h] [--precision PRECISION] [--from FROM] [--to TO] [--commodity COMMODITY] [--description DESCRIPTION]
               --accrual-start ACCRUAL_START --accrual-end ACCRUAL_END [--reporting-start REPORTING_START]
               [--reporting-end REPORTING_END] [--real | --periodic] [--unmarked | --pending | --cleared]
               amount

positional arguments:
  amount                                           amount that has to be divided across periods

options:
  -h, --help                                       show this help message and exit
  --precision PRECISION                            specify decimal precision to use

transaction settings:
  --from FROM, -f FROM                             specify the account from which to take out funds
  --to TO, -t TO                                   specify the account to which to move funds to
  --commodity COMMODITY, -c COMMODITY              specify the commodity to use
  --description DESCRIPTION, -d DESCRIPTION        specify the description to use for each transaction

date range manipulation:
  --accrual-start ACCRUAL_START, -s ACCRUAL_START  specify the date from which to start accruing the amount
  --accrual-end ACCRUAL_END, -e ACCRUAL_END        specify the date at which to stop accruing the amount
  --reporting-start REPORTING_START                specify the date from which to start reporting transactions
  --reporting-end REPORTING_END                    specify the date at which to stop reporting transactions

transaction type:
  --real, -R                                       use real transactions
  --periodic, -p                                   use periodic transactions

transaction status:
  --unmarked, -U                                   mark every transaction as "unmarked"
  --pending, -P                                    mark every transaction as "pending"
  --cleared, -C                                    mark every transaction as "cleared"
```

### Examples

Take rent for January and accrue it for every day of the month:

```sh
python3 main.py 400 -s 2024-01-01 -e 2024-02-01 -d "Pay rent" --to "expenses:rent"
```

## Roadmap

- [ ] Accrue for different periods, not just daily
- [ ] Custom date formats
- [ ] Use smart dates similar to hledger's
- [ ] Use python's parser groups more nicely
