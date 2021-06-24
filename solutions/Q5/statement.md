# Extra Weight

You've recently discovered a wonder drug that promises to reduce fat in any patient, provided they have enough body weight for the drug to take effect!

Luckily you have a machine that can tell, given somebody's body weight, whether they will be affected by this drug or not. Unluckily, this machine also suffers from a rat infestation, which tends to mess up test results.

The rats, to your delight, have a strict timetable however, and will always show up on the same days of the week (So they might always be in the machine on Mondays to Fridays, but leave to scrounge for food on the Weekends).

Given that you can test only 1 patient a day, you want to figure out who is the heaviest patient for which this drug will not work, by the end of the month (30 days).

## Interaction

Input will begin with a single integer ~T~, the number of tests. ~T~ lines will follow.

Each test will being with two floats, ~l~ and ~r~. You know that the heaviest patient weighs somewhere between ~l~ and ~r~ kilograms.
After this, you will be able to make queries to the judge. A query can be of two forms:

* `Q <patient_id>`: Test `patient_id` on the machine.
* `A <patient_id>`: You think `patient_id` is the heaviest patient for which the drug won't work.

After printing `Q <patient_id>`, the judge will respond with one of two strings: `SAFE` or `DANGEROUS`. If rats are not currently occupying the machine, `SAFE` will be responded if the person is above a particular weight, and `DANGEROUS` if below this weight. But, if rats are occupying this machine, then the results will be flipped (`DANGEROUS` if above, `SAFE` if below).

After printing `A <patient_id>`, you should move to the next test case.

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

* Solving the problem for all tests containing 3% of the patients or less will get you 20% score.
* Solving the problem for all tests containing 30% of the patients or less will get you 50% score.
* Solving the problem for all tests containing 98% of the patients or less will get you 100% score.

## Other

All references to Body Weight references the latest observation for that patient. Every patient will have at least one observation for Body Weight.
