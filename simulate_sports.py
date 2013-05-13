# Import necessary modules
import math
import random
from threading import Thread, Lock
from time import sleep
from itertools import combinations as combo


# Initialize PRNG, create locks and shared resources
random.seed(12345)
max_score = 0
max_lock = Lock()
print_lock = Lock()

## Function to simulate a match between two teams
#  num - this is the numth match this week
#  pairing - team numbers for participating teams
def simulateMatch(num, pairing):
  global max_score
  
  # Print a notice that the match has started
  print_lock.acquire()
  try:
    print "+++Match %d between teams %d and %d is beginning" % (num, pairing[0], pairing[1])
  finally:
    print_lock.release()

  # Matches last somewhere between 3 and 15 seconds
  delay = random.randint(3,15)
  sleep(delay)

  # Scores for each team are random, between 1 and 99
  score1 = random.randint(1,99)
  score2 = random.randint(1,99)

  # Print notice that match ended and resulting scores
  print_lock.acquire()
  try:
    print "---Match %d has completed.  Final score: %d to %d" % (num, score1, score2)
  finally:
    print_lock.release()
  
  # Check to see if a new high score was acheived for the week
  new_max = False
  max_lock.acquire()
  try:
    if (score1 > max_score):
      max_score = score1
      new_max = True
    if (score2 > max_score):
      max_score = score2
      new_max = True
  finally:
    max_lock.release()  

  # Print notice if a new max score was achieved by one of the teams
  if (new_max):
    print_lock.acquire()
    try:
      print "My score is now the week's maximum"
    finally:
      print_lock.release()


## Function to generate valid weekly pairings between teams
#  depth - current number of pairings generated for the week
#  matchups - remaining combinations to draw from for new pairings
#  used - list of teams already exhausted for the week
def scheduleWeek(depth, matchups, used):
  # If there are no combos to try, or we've recursed too far, abort this branch
  if ((len(matchups) == 0) or (depth > 5)):
    return (6, [])

  pairing = matchups[0]

  # See if either team in the next combo is exhausted, and if so skip
  if ((pairing[0] in used) or (pairing[1] in used)):
    return scheduleWeek(depth, matchups[1:], used)

  # If we've found 5 valid pairings, that's all we need for the week
  elif (depth == 5):
    return (5, [pairing])

  # Otherwise, keep the current pairing and try adding later pairings
  else:
    map(used.append, pairing[:2])
    deeper = scheduleWeek((depth + 1), matchups[1:], used)

    # If the later pairings reached our goal, append the current and later lists
    if (deeper[0] == 5):
      return (5, [pairing] + deeper[1])

    # Otherwise, the current pairing won't work, so try again with the next
    else:
      map(used.remove, pairing[:2])
      return scheduleWeek(depth, matchups[1:], used)



# Create list of all matchups between teams
matchups = []
combos = combo(xrange(1, 11), 2)
matchups.extend(combos)
matchups = sorted((2 * matchups), key=lambda tup: tup[0])

# Simulate 18 weeks of matches
for week in (range(1,19)):
  print "Simulating week %d:" % (week)
  threads = []
  matchnum = 0

  # Generate 1 weeks worth of matches
  weekly = scheduleWeek(1, matchups, [])
  for pairing in weekly[1]:
    matchnum += 1
    matchups.remove(pairing)

    # Create a new thread to run the simulation function
    threads.append(Thread(target=simulateMatch, args=[matchnum, pairing]))

  # Run the generated threads
  for match in threads:
    match.start()

  # Wait for all running threads to rejoin before simulating the next week
  for match in threads:
    match.join()
  print ""

raw_input("Press any key to continue")
