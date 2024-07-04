from data import Transaction
import csv


class EolCsvWriter:

    def __init__(self, output_file, journal, gl_generic, gl_transfer, gl_fincost):
        self.output_file = output_file
        self.journal = journal
        self.gl_generic = gl_generic
        self.gl_transfer = gl_transfer
        self.gl_fincost = gl_fincost
        self.file = None
        self.writer = None
        self.transactions = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.transactions:
            # Open file here to write everything at once
            with open(self.output_file, mode='w', newline='', encoding='iso-8859-1') as file:
                writer = csv.writer(file)
                starting_balance = self.transactions[0].before_balance
                closing_balance = self.transactions[-1].after_balance
                journal = self.journal
                # EOL is happiest when the header has a fixed ID in the first row
                writer.writerow(
                    ['H', journal, starting_balance, closing_balance])

                for transaction in self.transactions:
                    if transaction.reference == "TRANSFER":
                        glaccount = self.gl_transfer
                    elif transaction.reference == "FEE":
                        glaccount = self.gl_fincost
                    else:
                        glaccount = self.gl_generic

                    eol_transaction = [
                        EolCsv.date(transaction.datetime),
                        glaccount,
                        transaction.description,
                        transaction.amount,
                        transaction.description
                    ]
                    writer.writerow(eol_transaction)

    def write_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)


class EolCsv:
    @staticmethod
    def date(val):
        return val.strftime('%d/%m/%y')
