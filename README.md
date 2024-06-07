# `hledger-accrue`

This is a Python 3 script that takes an amount and a bunch of params which it uses to generate multiple transactions that add up to the original amount. This is useful for accruing expenses.

## Requirements

Make sure you have a working installation of Python.

## Usage

Currently to use this script you have to:

1. Clone the repo

```sh
git clone https://github.com/victormihalache/hledger-accrue.git
```

2. `cd` into the directory

```sh
cd hledger-accrue
```

3. Call the script

```sh
python3 main.py 400 --from 'assets:prepaid expenses' --to 'expenses:rent' --start 2024-01-01 --end 2024-02-01 -c USD
```

On MacOS you can just copy this all:

```sh
git clone https://github.com/victormihalache/hledger-accrue.git
cd hledger-accrue
python3 main.py 400 --from 'assets:prepaid expenses' --to 'expenses:rent' --start 2024-01-01 --end 2024-02-01 -c USD | pbcopy
```

## Roadmap

- [ ] Accrue for different periods, not just daily
- [ ] Custom date formats
- [ ] Generate real transactions, not just periodic
