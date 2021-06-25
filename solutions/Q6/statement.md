# Faking Patients

You've recently collected blood samples from a group of patients, and you know that exactly two of the patients gave fake blood in their samples. Luckily, you know that the surface tension of fake blood is much higher than that of real blood, and so you aim to use this to separate the samples out.

To do this, you've hired a spectral analyser. To use the spectral analyser, you select which samples will be on the left dish, and which samples will be on the right dish, then the spectral analyser will tell you which dish has the higher surface tension (If any).

For the purposes of this question, you may assume that:

* The surface tension of a group of samples is simply the average surface tension of all individual samples.
* The surface tension of real blood is always exactly the same.
* The surface tension of fake blood is always exactly the same, and higher than fake blood.

So if the left dish has a higher surface tension than the right dish, you know the there must be more fake samples in the left dish than the right dish.

## Interaction

The first line of input will contain the filepath to the dataset. After you've digested the data at this path, you should print "Ready!"

After this, the problem begins. The next line of input will contain an integer ~T~, the number of tests.
~T~ lines then follow. Each of these lines will contain two numbers, ~l~ and ~r~, separated by spaces. You know that the two fake samples have hemoglobin readings somewhere inbetween ~l~ and ~r~.

After this, interaction begins.
You print one of two types of queries:

* Questions: a `Q`, followed by two numbers, ~l_p, r_p~, the number of samples on the left and right dishes, respectively. After this the ~l_r + l_p~ patient ids follow. The Judge will respond with either LEFT, RIGHT or EQUAL - the side of the sample with *higher* surface tension.
* Answers: an `A`, followed by two patient ids. These are the patients you believe have the fake blood.

As soon as you make a guess for the answer, you should go to the next test case.
If you do more than 100 question queries, the judge will respond with a FINISH, and you should move to the next test case.

## Problem bounds

The total number of tests will not exceed 100.

## Scoring

A run time error, or incorrectly formatted print statement, will instantly net you 0 score.

For every test case, if you can solve the problem correctly after TODO queries, you will get the score for this test case.

* Solving the problem for all tests containing 3% of the patients or less will get you 20% score.
* Solving the problem for all tests containing 30% of the patients or less will get you 50% score.
* Solving the problem for all tests containing 98% of the patients or less will get you 100% score.

## Example run

```text
Judge: dataset/build
Code: Ready!
Judge: 1
Judge: 4 10 
(Assumes that ID_0001 ID_0002 ID_0003 ID_0004 ID_0005 are the patients with these hemoglobin values)
Code: Q 1 1 ID_0001 ID_0002
Judge: LEFT
Code: Q 1 1 ID_0003 ID_0004
Judge: EQUAL
Code: A ID_0001 ID_0005
```

## Other

All references to Hemoglobin [Mass/volume] in Blood references the latest observation for that patient. Every patient will have at least one observation for Hemoglobin [Mass/volume] in Blood.
