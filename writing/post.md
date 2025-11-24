# Is Spotify Wrapped Really Telling the Whole Truth?

## Introduction

Every December, Spotify Wrapped drops into our feeds like clockwork,
offering a personalized summary of our listening habits.
It’s fun, vibrant, and sometimes feels spot-on.
But somehow, every year there is a point in which the illusion breaks.

But let’s be honest—have you ever looked at your Wrapped and thought,
“Wait, that was my most-played song?”

I had that exact moment this year.
I couldn’t shake the feeling that some of my favorite tracks were missing,
while others seemed oddly high on the list.
Was Spotify Wrapped reflecting my true listening habits,
or was it skewed by some hidden logic in Spotify’s algorithms?
Maybe they are just not trying to be precise?

To investigate, I needed a way to fact-check Spotify's rankings. Enter Last.fm.

## The Approach

### What is Last.fm?

For those unfamiliar,
Last.fm is a music tracking platform
that “scrobbles” (logs) every track you listen to across various apps and devices.
Whether you’re streaming on Spotify, Apple Music,
or even playing MP3s locally, Last.fm keeps a running tally of your plays.

Unlike Spotify Wrapped,
which only gives you a hint of your listening habits one a year,
and even then, it only shows partial information,
Last.fm gives you access to your entire listening history.
From reports and chart to a full raw track list history,
you can see them all on their site, or using their accesible API.

## The Plan

To test Spotify Wrapped, I compared:

Spotify's Wrapped Rankings: A list of my top 20 tracks from the year.
Last.fm’s Rankings:
The top 20 tracks scrobbled across all platforms I used throughout the year.

Key Questions I Wanted to Answer:

Do the same songs appear on both lists?
Are the rankings consistent between platforms?
Does Spotify Wrapped accurately reflect my most-played songs, or is it biased?

## The Methodology

### The quest for the right metric

<!--TODO: add this-->

### Some math stuff

<!--TODO: add this-->

### Final result

I used several quantitative measures to compare the two lists:

Edit Distance: How many changes are needed to turn one ranking into the other?
Kendall Tau and Spearman Correlation: Do the relative rankings align?
Jaccard Similarity: How many tracks appear on both lists?
Rank-Biased Overlap (RBO): A weighted similarity metric
emphasizing the top of the lists.

To visualize the results,
I also created a crossed rankings plot,
showing how individual songs ranked on Spotify versus Last.fm.

(Insert plot visualization here.)

## The Results

Here’s what I found:

Overlap: 64% of the tracks appeared on both lists, showing a decent level of agreement.
Rankings Disagree: The order of songs on the lists often differed.
For example, a song that Spotify ranked #2 was only #12 on Last.fm.
Metrics Summary:
Spearman Correlation: -0.201 (low alignment between ranks).
Rank-Biased Overlap (RBO): 65.4% (moderate overlap, especially at the top).
Composite Score: 40% (indicating significant differences overall).

## Analysis

<!--TODO: add this-->

## Want to Try This Yourself?

Curious to see how your rankings compare across platforms?
I’ve developed a tool to do just that.
With a few simple inputs (your Spotify Wrapped playlist and Last.fm data), you can:

Check which tracks overlap between platforms.
Quantify how well Spotify Wrapped reflects your listening habits.
Visualize differences between rankings.

The code is open-source and available here.
Give it a try and see if Spotify Wrapped is telling your full musical story!
Conclusion
