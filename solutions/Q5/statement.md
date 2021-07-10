# Extra Weight

You've recently discovered a wonder drug that promises to reduce fat in any patient, provided they have enough body weight for the drug to take effect!

Luckily you have a machine that can tell, given somebody's body weight, whether they will be affected by this drug or not. Unluckily, this machine also suffers from a rat infestation, which tends to mess up test results.

The rats, to your delight, have a strict timetable however, and will always show up on the same days of the week (So they might always be in the machine on Mondays to Fridays, but leave to scrounge for food on the Weekends).

Given that you can test only 1 patient a day, you want to figure out who is the heaviest patient for which this drug will not work, by the end of the month (30 days).

## Interaction

Input will begin with the dataset path. After consuming the dataset, print "Ready!".

After this, you should read a single integer ~T~, the number of tests. ~T~ lines will follow.

Each test will being with two floats, ~l~ and ~r~. You know that the heaviest patient weighs somewhere between ~l~ and ~r~ kilograms.
After this, you will be able to make queries to the judge. A query can be of two forms:

* `Q <patient_id>`: Test `patient_id` on the machine.
* `A <patient_id>`: You think `patient_id` is the heaviest patient for which the drug won't work.

After printing `Q <patient_id>`, the judge will respond with one of two strings: `SAFE` or `DANGEROUS`. If rats are not currently occupying the machine, `SAFE` will be responded if the person is above a particular weight, and `DANGEROUS` if below this weight. But, if rats are occupying this machine, then the results will be flipped (`DANGEROUS` if above, `SAFE` if below). However, if this the 31st query, the judge will respond `FINISHED`, and you must move to the next test case.

After printing `A <patient_id>`, you should move to the next test case (So don't expect a response).

## Problem bounds (After contest scoring)

The total number of patients across all test cases will not exceed ~10^7~.
The total number of patients in a single test case will not exceed ~10^5~.

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

* Solving the problem for all tests containing 3% of the patients or less will get you 20% score.
* Solving the problem for all tests containing 30% of the patients or less will get you 50% score.
* Solving the problem for all tests containing 98% of the patients or less will get you 100% score.

## Other

All references to Body Weight references the latest observation for that patient. Every patient will have at least one observation for Body Weight.

In every test case, at least one patient will *not* have body weight in the range ~l~ to ~r~.

## Example run

```text
Judge: build
Code: Ready!
Judge: 1
Judge: 60 80 
(Assumes that ID_0001 ID_0002 ID_0003 ID_0004 ID_0005 are the patients with these body weight values, and that Rats are in the first and third queries, with ID_0001, ID_0002 and ID_0003 being DANGEROUS)
Code: Q ID_0001
Judge: SAFE
Code: Q ID_0001
Judge: DANGEROUS
Code: Q ID_0005
Judge: DANGEROUS
(This is a blind guess, you need to actually solve the problem though)
Code: A ID_0003
```
