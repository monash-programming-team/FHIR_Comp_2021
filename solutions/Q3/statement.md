# Patient Links

You've developed a new method for identifying cancer in patients!
However, this method is currently only tested on a single patient, and you want to generalise this method to fit all patients.

Generalising the method is slightly complicated, and depends on a patient's Body Height. The single patient you've developed this method for is the *tallest* of patients you are trying to generalise for.

In order to generalise the method, you need to choose two patients, where for one the method has been generalised, and the other it hasn't (With heights ~h_a~ and ~h_b~). We can then generalise with cost

$$
    C := \ln\left(\frac{||h_a - h_b||}{d \times n}\right),
$$

where ~d~ is dependant on the test case, and ~n~ is the number of patients with heights in the range ~h_a~ to ~h_b~, inclusive.

After which, any patient with height between ~h_a~ and ~h_b~ can be tested with this method. Note that ~C~ can be negative.

Your aim is to complete a series of generalisations with minimum cost, such that any patient can be tested. (The total cost of all generalisations, is the sum of all ~C~ for each generalisation, **plus** the total number of patients generalised (This ensures the result is positive for our test set))

## Input

Input will start with the dataset path, on a single line

Next, a single integer will be given on the next line, this will be the number of test cases, ~t~. ~2t~ lines follow.

For each test case, we have two lines:

The first line contains ~d~ and ~p~, ~d~ being the value mentioned earlier, and ~p~ being the number of patients to consider.

The second line contains the ~p~ space separated patient IDs that we are considering.

## Output

First, once you have read the dataset, print "Ready!"

Next, for each test case, print the number of generalisations you will be making, on a single line.

Then, for each generalization, print one line containing two patient ids: One being already generalised, and another that is not.

## Scoring

We have a solution that does alright in generalising to all patients.

You will begin to accrue points if your answers cost less than 115% of ours.
You will stop getting points if your answers cost less than 97% of ours (You will get full score).

* If you can beat 97% cost for 100 patients or less, you will score 20%
* If you can beat 97% cost for 5000 patients or less, you will score 50%
* If you can beat 97% cost for 100000 patients or less, you will score 100%

## Other

All references to `Body Height` references the latest observation for that patient. Every patient will have at least one observation for `Body Height`.
