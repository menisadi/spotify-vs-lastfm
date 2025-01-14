# Is Spotify Wrapped Really Telling the Whole Truth?

## Introduction

Every December, Spotify Wrapped drops into our feeds like clockwork, offering a personalized summary of our listening habits. It’s fun, vibrant, and sometimes feels spot-on. But let’s be honest—have you ever looked at your Wrapped and thought, “Wait, that was my most-played song?”

I had that exact moment this year. I couldn’t shake the feeling that some of my favorite tracks were missing, while others seemed oddly high on the list. Was Spotify Wrapped reflecting my true listening habits, or was it skewed by some hidden logic in Spotify’s algorithms?

To investigate, I needed a way to fact-check Spotify's rankings. Enter Last.fm.

## The Approach

## What is Last.fm?
For those unfamiliar, Last.fm is a music tracking platform that “scrobbles” (logs) every track you listen to across various apps and devices. Whether you’re streaming on Spotify, Apple Music, or even playing MP3s locally, Last.fm keeps a running tally of your plays.

Unlike Spotify Wrapped, which reflects only your activity within Spotify, Last.fm offers a more comprehensive and unbiased record of your listening habits. This made it the perfect tool to cross-check Spotify’s claims.

## The Plan

To test Spotify Wrapped, I compared:

    Spotify's Wrapped Rankings: A list of my top 20 tracks from the year.
    Last.fm’s Rankings: The top 20 tracks scrobbled across all platforms I used throughout the year.

Key Questions I Wanted to Answer:

    Do the same songs appear on both lists?
    Are the rankings consistent between platforms?
    Does Spotify Wrapped accurately reflect my most-played songs, or is it biased?

## The Methodology

I used several quantitative measures to compare the two lists:

    Edit Distance: How many changes are needed to turn one ranking into the other?
    Kendall Tau and Spearman Correlation: Do the relative rankings align?
    Jaccard Similarity: How many tracks appear on both lists?
    Rank-Biased Overlap (RBO): A weighted similarity metric emphasizing the top of the lists.

To visualize the results, I also created a crossed rankings plot, showing how individual songs ranked on Spotify versus Last.fm.

(Insert plot visualization here.)

## The Results

Here’s what I found:

    Overlap: 64% of the tracks appeared on both lists, showing a decent level of agreement.
    Rankings Disagree: The order of songs on the lists often differed. For example, a song that Spotify ranked #2 was only #12 on Last.fm.
    Metrics Summary:
        Spearman Correlation: -0.201 (low alignment between ranks).
        Rank-Biased Overlap (RBO): 65.4% (moderate overlap, especially at the top).
        Composite Score: 40% (indicating significant differences overall).

## Analysis

    Spotify’s Prioritization: Wrapped seems to overemphasize tracks that were played repeatedly in bursts or within Spotify itself. Songs I listened to just a few times on Spotify but heavily elsewhere were often underrepresented.
    Last.fm’s Breadth: By capturing plays across all platforms, Last.fm provided a broader view of my true listening habits. It included tracks I played on platforms like YouTube or local files that Spotify Wrapped ignored.
    Algorithmic Bias?: Wrapped’s focus on Spotify-only data may skew the results to favor certain tracks or artists, especially those Spotify promotes or playlists heavily feature.

## What This Means for You

Spotify Wrapped is undeniably fun, but its accuracy depends on how much you use Spotify and how its algorithms weigh your plays. If, like me, you use multiple platforms or have diverse listening habits, it may not paint a complete picture of your year in music.

## Want to Try This Yourself?

Curious to see how your rankings compare across platforms? I’ve developed a tool to do just that. With a few simple inputs (your Spotify Wrapped playlist and Last.fm data), you can:

    Check which tracks overlap between platforms.
    Quantify how well Spotify Wrapped reflects your listening habits.
    Visualize differences between rankings.

The code is open-source and available here. Give it a try and see if Spotify Wrapped is telling your full musical story!
Conclusion

This little experiment revealed that Spotify Wrapped, while entertaining, might not always be an accurate reflection of your year in music. For a more complete picture, platforms like Last.fm can complement Spotify’s story and uncover listening habits you might have missed.
