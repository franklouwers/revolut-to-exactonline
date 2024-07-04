#!/usr/bin/python3

import argparse
import pprint

from revolut import RevolutCsvReader
from eol import EolCsvWriter


def main():
    parser = argparse.ArgumentParser(
        prog='revolut-to-eolCSV',
        description='Convert Revolut CSV-files to Exact Online CSV format.')

    parser.add_argument('--in',
                        dest='input_file',
                        help='path to Revolut csv-file',
                        required=True)

    parser.add_argument('--out',
                        dest='output_file',
                        help='path to EOL CSV output file',
                        required=True)

    parser.add_argument('--transfer',
                        dest='gl_transfer',
                        help='GLaccount for Transfers (default: 580000)',
                        required=False,
                        default='580000')

    parser.add_argument('--journal',
                        dest='journal',
                        help='Exact Journal ID (default: 502)',
                        required=False,
                        default='502')

    parser.add_argument('--default',
                        dest='gl_default',
                        help='GLaccount for unknown transactions (default: 580900)',
                        required=False,
                        default='580900')

    parser.add_argument('--fincost',
                        dest='gl_fincost',
                        help='GLaccount for banking financial costs (default: 658000)',
                        required=False,
                        default='658000')

    args = parser.parse_args()

    reader = RevolutCsvReader(args.input_file)

    with EolCsvWriter(args.output_file, args.journal, args.gl_default, args.gl_transfer, args.gl_fincost) as writer:
        transactions = reader.get_all_transactions()
        for transaction in transactions:
            pprint.pprint(transaction)
            writer.write_transaction(transaction)

        print('Wrote {} transactions to file: {}'.format(
            len(transactions), args.output_file))


if __name__ == "__main__":
    main()
