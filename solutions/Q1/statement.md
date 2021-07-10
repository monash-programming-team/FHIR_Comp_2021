# Efficient Vaccines

You are rolling out a vaccine for a new virus, that is fast mutating and specific to body types. As such, every vaccine needs to be personally hand crafted, to avoid side-effects.

That being said, you can still get away with certain groups of people sharing the same hand-crafted vaccine, provided they have similar Platelet Mean Volume readings. In particular, let's say we are making a vaccine for a group of people, with Platelet Mean Volume in the range of ~[v_\text{min}, v_\text{max}]~. Then the probabilty that any one person experiences side-effects is 

$$
    \frac{(v_\text{max} - v_\text{min})^2}{30n},
$$

where ~n~ is dependant on the test case.

Because making these vaccines is expensive, you want to know how many people you can possibly vaccinate with a single hand-crafted vaccine, such that the expected number of people with side effects does not exceed 3.

## Input

The first line of input will contain the filepath to the dataset.

The next line of input will contain an integer ~T~, the number of tests. ~T~ lines then follow. 

Each of these lines will contain ~n~, the value in the cost above, ~N~, the size of the group of patients, and then space separated patient IDs - the group of patients we are considering for vaccination.

## Output

After reading the dataset, print "Ready!".

After this you will print ~T~ integers: the maximum number of patients you can vaccinate from each group, with a single hand-crafted vaccine.

## Problem bounds (After contest scoring)

The total number of patients across all test cases will not exceed ~10^7~.

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

* Solving the problem for all tests containing 3% of the patients or less will get you 20% score.
* Solving the problem for all tests containing 30% of the patients or less will get you 60% score.
* Solving the problem for all tests containing 98% of the patients or less will get you 100% score.

## Other

Each patient will have at least one recorded observation for Platelet Mean Volume.
In the case where a patient has multiple recorded observations for Platelet Mean Volume, use the recording with the latest effective date.
