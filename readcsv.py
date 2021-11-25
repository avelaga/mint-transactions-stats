import csv

fieldnames = ['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type', 'Category', 'Account Name']

with open('transactions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames)
    result = []
    for row in reader:
        newrow = {}
        for field in fieldnames:
            newrow[field] = row[field]
        result.append(newrow)

total = 0
investmentTotal = 0
incomeTotal = 0

for transaction in result:
    amt = float(transaction['Amount'])
    # only count charges that are not credit card bills, brokerage account transfers, or double counted venmo transactions
    if transaction['Transaction Type'] == 'debit' and transaction['Category'] != 'Credit Card Payment' and transaction['Description'] != 'FID BKG SVC LLC ' and transaction['Account Name'] != 'Venmo':
        if amt>300:
            print("{0:10} -  {1:40} -${2:<10,.2f} {3:10} {4:10}".format(transaction['Date'], transaction['Description'], amt, transaction['Transaction Type'], transaction['Category']))
        total += amt

    # subtract deposits from venmo, usually friends paying me back for expenses counted in full in the above loop
    elif transaction['Transaction Type'] == 'credit' and transaction['Account Name'] == 'Venmo':
        total -= amt
        if amt>300:
            print("{0:10} -  {1:40} +{2:<10,.2f} {3:10} {4:10}".format(transaction['Date'], transaction['Description'], amt, transaction['Transaction Type'], transaction['Category']))

    # add up investment transfers
    elif transaction['Description'] == 'FID BKG SVC LLC ':
        investmentTotal += amt

    # add up paychecks
    elif transaction['Transaction Type'] == 'credit' and 'VISA TECHNOLOGY DES:DIRECT DEP' in transaction['Description']:
        incomeTotal += amt

print("Total expenses: ${:,.2f}" .format(total))
print("Total investment deposits: ${:,.2f}".format(investmentTotal))
print("Total job income: ${:,.2f}".format(incomeTotal))