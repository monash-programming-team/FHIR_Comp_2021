# Greedy Vaccines

You are rolling out a vaccine for a new virus, that is fast mutating and specific to body types. As such, every vaccine needs to be personally hand crafted, to avoid side-effects.

That being said, you can still get away with certain groups of people sharing the same hand-crafted vaccine, provided they have similar OBS_NAME. In particular, let's say we are making a vaccine for a group of people, with OBS_NAME in the range of \([v_min, v_max]\). Then the probabilty that any one person experiences side-effects is 

$$
    (v_max - v_min)^2 / 1000000.
$$

Because making these vaccines is expensive, you want to know how many people you can possible vaccinate with a single hand-crafted vaccine, such that the expected number of people with side effects does not exceed 3.

## Patient information

Each patient will have at least one recorded observation for OBS_NAME (LOINC code OBS_CODE).
In the case where a patient has multiple recorded observations for OBS_NAME, use the recording with the latest effective date.

## Input

The first line of input will contain the filepath to the dataset. After this you will have 5 minutes to digest the dataset into something more readable, before printing "Ready!".
After this, the problem begins. The next line of input will contain an integer \(N\), the number of tests.
\(N\) lines then follow. Each of these lines will contain space separated patient IDs - the groups of patients we are considering for vaccination.

## Output

After printing "Ready!", you will have 2 seconds to print \(N\) integers: the maximum number of patients you can vaccinate from each group, with a single hand-crafted vaccine.

## Problem bounds

The total number of patients across all test cases will not exceed \(10^6\).

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

The test cases are ordered with an increasing number of patients, and you will stop getting score as soon as your program runs out of execution time.

For every test case passed, with a list of \(p\) patients, a correct answer will net you \(\sqrt{p}\) score.

## Example run

**REPLACE WITH ACTUAL DATA**

Input:

```text
C:/Users/test/Documents/sample_dataset.json
2
ID_0001 ID_0002
ID_0001 ID_0003 ID_0004 ID_0005
```

Output:

```text
Ready!
1
3
```
