import csv
from colorama import Fore, Back, Style

fieldnames = ['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type', 'Category', 'Account Name']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
restarauntTotal = 0
groceriesTotal = 0
counts = {}

for transaction in result:
    amt = float(transaction['Amount'])
    # only count charges that are not credit card bills, brokerage account transfers, or double counted venmo transactions
    if transaction['Transaction Type'] == 'debit' and transaction['Category'] != 'Credit Card Payment' and transaction['Description'] != 'FID BKG SVC LLC ' and 'COINBASE.COM' not in transaction['Description'] and transaction['Account Name'] != 'Venmo':
        if amt>300:
            print("{0:10} -  {1:40} \033[91m-{2:<10,.2f}\033[0m {3:10} {4:10}".format(transaction['Date'], transaction['Description'][:40], amt, transaction['Transaction Type'], transaction['Category']))
        total += amt

        # track restaraunt and grocery spending
        if transaction['Category'] == 'Restaurants' or transaction['Category'] == 'Fast Food':
            restarauntTotal += amt
        elif transaction['Category'] == 'Groceries':
            groceriesTotal += amt

        # track most frequent purchases and total 
        if transaction['Description'] in counts:
            oldCountObj = counts[transaction['Description']]
            oldCountObj['Amount'] += amt
            oldCountObj['Count'] += 1
            counts[transaction['Description']] = oldCountObj
        else:
            counts[transaction['Description']] = {'Amount' : amt, 'Count': 1}

    # subtract deposits from venmo, usually friends paying me back for expenses counted in full in the above loop
    elif transaction['Transaction Type'] == 'credit' and transaction['Account Name'] == 'Venmo':
        total -= amt
        if amt>300:
            print("{0:10} -  {1:40} \033[92m+{2:<10,.2f}\033[0m {3:10} {4:10}".format(transaction['Date'], transaction['Description'][:40], amt, transaction['Transaction Type'], transaction['Category']))

    # add up investment transfers
    elif transaction['Description'] == 'FID BKG SVC LLC ' or 'COINBASE.COM' in transaction['Description']:
        investmentTotal += amt

    # add up paychecks
    elif transaction['Transaction Type'] == 'credit' and 'VISA TECHNOLOGY DES:DIRECT DEP' in transaction['Description']:
        incomeTotal += amt

print("\033[94m***********************************************************************************\033[0m")

print("Total expenses: \033[91m${:,.2f}\033[0m" .format(total))
print("Total investment deposits: \033[92m${:,.2f}\033[0m".format(investmentTotal))
print("Total job income: \033[92m${:,.2f}\033[0m".format(incomeTotal))
print("Total restaraunt spending: \033[91m${:,.2f}\033[0m".format(restarauntTotal))
print("Total groceries spending: \033[91m${:,.2f}\033[0m".format(groceriesTotal))

print("\033[94m***********************************************************************************\033[0m")

countsArr = []

for count in counts:
    c = {}
    c['Name'] = count
    c['Count'] = counts[count]['Count']
    c['Amount'] = counts[count]['Amount']

    countsArr.append(c)

def mySort(e):
    return e['Amount']

countsArr.sort(key=mySort, reverse=True)

for tran in countsArr:
    print( "{0:40} {1:<20} \033[91m${2:<10,.2f}\033[0m".format(tran['Name'][:40], tran['Count'], tran['Amount']))