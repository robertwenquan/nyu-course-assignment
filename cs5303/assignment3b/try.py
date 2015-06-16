#!/usr/bin/python

balance = 4900
saving = 100
interest = 0
month = 1

while balance > 0:
  month += 1
  interest = saving * 0.001
  balance -= (interest + 100)
  saving += (interest + 100)

  if balance >= 0:
    payment = 100
  else:
    payment += balance
    saving += balance
    balance -= balance

  print "%2d saving: %.2f, payment: %.2f, interest: %.2f, balance: %.2f" % (month, saving, payment, interest, balance)
