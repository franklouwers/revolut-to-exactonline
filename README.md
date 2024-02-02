# Convert Revolut export file to Exact Online compatible CSV format

This small Python script converts Revolut Transaction Statements (in CSV) to Exact Online's wierd CSV format.

## Disclaimer
This script comes without any warranty whatsoever. Do not use it in production.
Do not use it if you are not familiar with how banks work, how bookkeeping
software works, and if you do not have the technical know-how to make changes
to this script yourself if something breaks. If you do use this script it might
kill your cat or start World War 3. Don't come to me, I warned you.

Very big thanks to https://github.com/gerwin3 for https://github.com/gerwin3/revolut-to-mt940!

## Features

* It is specifically built for getting Revolut Business transactions into Exact Online.
* Parses the Revolut CSV file and extracts: timestamp, counterparty name, transaction description, transaction amount, fee amount, balance after transaction, counterparty IBAN.
* This information is converted into a valid Exact Online compatible CSV file.
* Revolut charges fees for transactions. These are included in the transaction (as Revolut sees it). This could cause problems when importing into bookkeeping software as the amounts do not match up. This script will not include fees in transactions but insert "fake" transactions for each deducted fee. You will see those transactions separately in your bookkeeping software but in Revolut they are included in the transaction.

## Usage

1. Clone the repository.
2. Make sure you have Python 3.
3. Run the following command:

```
python3 main.py \
	--in /path/to/revolut.csv \
	--out /path/to/eol.csv
```

Other optional parameters:

```
  --transfer GL_TRANSFER    GLaccount for Transfers (default: 580000)
  --journal JOURNAL         Exact Journal ID (default: 502)
  --default GL_DEFAULT      GLaccount for unknown transactions (default: 580900)
  --fincost GL_FINCOST      GLaccount for banking financial costs (default: 658000)
```

I've included rough notes (in Dutch) on how to configure this in Exact Online in the [notes](notes.md) file.

## License

MIT

The majority of this code is (c) Gerwin van der Lugt (Revolut to MT940). The Exact Online adaption is (c) Frank Louwers
