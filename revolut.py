import os
import string
import csv
import math
from datetime import datetime, timedelta
from data import Transaction

# Constants
NAME_REMOVE_PREFIXES = ['Payment from ', 'To ']
DATE_FORMAT = '%Y-%m-%d'
FEE_NAME = 'Revolut'
FEE_IBAN = ''
FEE_DESCRIPTION_FORMAT = 'Bank transaction fee {}'
FEE_DATETIME_DELTA = timedelta(seconds=1)


class RevolutCsvReader:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise ValueError(f'File does not exist: {filename}')
        self.filename = filename
        self.file = open(self.filename, 'r')
        self.reader = csv.reader(self.file)
        self.headers = self._read_headers()

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    def _read_headers(self):
        def _normalize_header(header):
            header = ''.join(c for c in header if c in string.printable)
            header = header.strip().lower().replace(' ', '_')
            return header

        raw_headers = next(self.reader)
        headers = [_normalize_header(h) for h in raw_headers]
        self.header_indices = {header: idx for idx,
                               header in enumerate(headers)}
        return headers

    def get_all_transactions(self):
        transactions = []
        for row in self.reader:
            transactions.extend(self._parse_transaction(row))
        return transactions

    def _parse_transaction(self, row):
        if not row:  # Skip empty lines
            return []

        # Define required headers and their corresponding attribute names
        required_headers = {
            'date_completed_(utc)': 'completed_date_str',
            'amount': 'amount_str',
            'fee': 'fee_str',
            'balance': 'balance_str',
            'description': 'description',
            'reference': 'reference',
            'beneficiary_iban': 'iban',
            'payer': 'payer',  # Optional field
        }

        # Extract required fields using header indices
        transaction_data = {}
        for header, attr_name in required_headers.items():
            index = self.header_indices.get(header)
            if index is not None:
                transaction_data[attr_name] = row[index]
            else:
                if header != 'payer':  # 'payer' is optional
                    print(f"Missing required header '{header}', skipping transaction.")
                    return []
                else:
                    # Set default value for optional fields
                    transaction_data[attr_name] = ''

        # Parse and sanitize extracted fields
        try:
            completed_datetime = datetime.strptime(
                transaction_data['completed_date_str'], DATE_FORMAT)
            amount = float(transaction_data['amount_str'])
            fee = float(transaction_data['fee_str'])
            balance = float(transaction_data['balance_str'])
            description = transaction_data['description']
            reference = transaction_data['reference']
            iban = transaction_data.get('iban', '')
            payer = transaction_data.get('payer', '')

            if payer:
                description += f" (paid by: {payer})"

            name = ""  # Field not present in CSV; set to empty or handle as needed

            # Create main transaction
            transaction_without_fee = Transaction(
                amount=amount,
                name=self._sanitize_name(name),
                iban=iban,
                description=description,
                datetime=completed_datetime,
                before_balance=balance - amount - fee,
                after_balance=balance - fee,
                reference=reference
            )

            transactions = [transaction_without_fee]

            # Create fee transaction if applicable
            if not math.isclose(fee, 0.00):
                fee_transaction = self._make_fee_transaction(
                    completed_datetime, balance, fee)
                transactions.append(fee_transaction)

            return transactions

        except Exception as e:
            print(f"Error parsing transaction: {e}")
            return []

    def _sanitize_name(self, name):
        for prefix in NAME_REMOVE_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
        return name

    def _make_fee_transaction(self, completed_datetime, balance, fee):
        return Transaction(
            amount=fee,
            name=FEE_NAME,
            iban=FEE_IBAN,
            description=FEE_DESCRIPTION_FORMAT.format(
                int(completed_datetime.timestamp())),
            datetime=completed_datetime + FEE_DATETIME_DELTA,
            before_balance=balance - fee,
            after_balance=balance,
            reference='FEE'
        )
