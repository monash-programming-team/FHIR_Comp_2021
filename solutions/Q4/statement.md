# Batch Testing

You need to test a set of patients for a particular disease, and luckily you've been able to rent the machine to do this.
However, you can't just put all patients under the testing device and expect to get good results, you need to clean the machine first.

Every day, you can select a set of patients to test. These patients have observations for both Diastolic and Systolic Blood Pressure.
For any group of patients with systolic and diastolic blood pressure ~s_1, d_1~ and ~s_2, d_2~, ~s_3, d_3~, ~\ldots~, we can calculate the Hamming distance:

$$
    H := \max_{n}(s_n) - \min_{n}(s_n) + \max_{n}(d_n) - \min_{n}(d_n).
$$

In other words the span of Systolic Blood Pressure plus the span of Diastolic Blood Pressure.
The cleaning cost in order to ensure all of these tests are accurate is

$$
    C := 10 + H^{1.5}.
$$

Your aim is to test everyone, with minimum cleaning cost.

## Input

Input will start with the dataset path, on a single line

Next, a single integer will be given on the next line, this will be the number of test cases, ~t~. ~t~ lines follow.

Each line contains a list of space-separate patient ids - The patients for this particular test.
**The number of patients in each test case will not exceed 30.**

## Output

First, once you have read the dataset, print "Ready!"

Next, for each test case, print the number of cleanings you will be using, on a single line.

Then, for each cleaning, print one line containing (separated by spaces):

* The character 'C'
* The distance required (~H~) for this cleaning
* The character 'P'
* The space separated patient ids you will be testing after this clean.

## Scoring

We have a solution the does alright in allocating everyone.

You will begin to accrue points if your answers cost less than 125% of ours.
You will stop getting points if your answers cost less than 95% of ours (You will get full score).

* If you can beat 95% cost for 8 patients or less, you will score 20%
* If you can beat 95% cost for 15 patients or less, you will score 50%
* If you can beat 95% cost for 30 patients or less, you will score 100%

## Other

All references to Systolic / Diastolic Blood Pressure references the latest observation for that patient. Every patient will have at least one observation for Systolic / Diastolic Blood Pressure.

## Example run

TODO
