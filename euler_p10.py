#!/usr/bin/python

# Test if num is prime
def isPrime(num):
  root = int(num ** .5)
  while root > 1:
    if not num % root: return 0
    root -= 1
  return 1

# Return an iterator of upto the boundth prime
def genPrime(bound):
  i = 2
  count = 1
  while count <= bound:
    if isPrime(i):
      count += 1
      yield i
    i += 1
  return

# Sum the primes less than 2,000,000
sum = 0
for i in genPrime(2000000):
   if i < 2000000: 
     sum += i
   else: break

print "Sum of prime below 2000000: ", sum
