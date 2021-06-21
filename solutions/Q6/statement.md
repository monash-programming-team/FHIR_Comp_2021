# Faking Patients

You've recently collected blood samples from a group of patients, and you know that exactly two of the patients gave fake blood in their samples. Luckily, you know that the surface tension of fake blood is much higher than that of real blood, and so you aim to use this to separate the samples out.

To do this, you've hired a spectral analyser. To use the spectral analyser, you select which samples will be on the left dish, and which samples will be on the right dish, then the spectral analyser will tell you which dish has the higher surface tension (If any).

For the purposes of this question, you may assume that:

* The surface tension of a group of samples is simply the average surface tension of all individual samples.
* The surface tension of real blood is always exactly the same.
* The surface tension of fake blood is always exactly the same, and higher than fake blood.

So if the left dish has a higher surface tension than the right dish, you know the there must be more fake samples in the left dish than the right dish.

## Interaction

The first line of input will contain the filepath to the dataset. After this you will have 5 minutes to digest the dataset into something more readable, before printing "Ready!".
After this, the problem begins. The next line of input will contain an integer \(N\), the number of tests.
\(N\) lines then follow. Each of these lines will contain space separated patient IDs - the patients who have given us blood.

After this, interaction begins.
You print one of two types of queries:

* Questions: a "Q", followed by two numbers, \(l_p, r_p\), the number of samples on the left and right dishes, respectively. After this the \(l_r + l_p\) patient ids follow. The Judge will respond with either LEFT, RIGHT or EQUAL.
* Answers: a "A", followed by two patient ids. These are the patients you believe have the fake blood.

As soon as you do an answer, you should go to the next test case.
If you do more than 1000 question queries, the judge will respond with a FINISH, and you should move to the next test case.

## Problem bounds

The number of patients in each test case will not exceed 1000.
The total number of tests will not exceed 100.

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

The test cases are ordered with an increasing number of patients, and you will stop getting score as soon as your program runs out of execution time.

For every test case, with a list of \(p\) patients, if you answered correct after \(q\) questions, your score will increase by

$$
    100 - 100 * \frac{q -\log_3(p * (p-1) / 2)}{p -\log_3(p * (p-1) / 2)}
$$

Since \(\log_3(p * (p-1) / 2)\) is the theoretical limit on solving this problem.

## Example run

```text
Judge: C:/Users/test/Documents/sample_dataset.json
Code: Ready!
Judge: 1
Judge: ID_0001 ID_0002 ID_0003 ID_0004 ID_0005
Code: Q 1 1 ID_0001 ID_0002
Judge: LEFT
Code: Q 1 1 ID_0003 ID_0004
Judge: EQUAL
Code: A ID_0001 ID_0005
```
