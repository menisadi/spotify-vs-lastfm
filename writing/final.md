# Spotify Wrapped Was Off - But By How Much? A Statistical Deep Dive

## Background

Every December, Spotify Wrapped drops into our feeds like clockwork,
offering a personalized summary of our listening habits.
It’s fun, vibrant, and sometimes feels spot-on.
But let’s be honest, almost every year there are some details which just feels off.
I'm not talking about the fact that "Baby Shark" made his way to my top songs,
this one I can explain.
I talking about this one song which you do listen to, but you are quite sure that not this much.
Or a song you had on repeat and still didn't menage to crack your top-10 somehow.
Last year [several](add-link) [claims](add-link) about the inaccuracy of the Spotify Wrapped rose on the media.
For me it was ["Sunset"](add-link) by the talented Caroline Polachek which I just couldn't get enough,
yet Spotify placed it on the modest no. 17.
Meanwhile one spot below come ["Two Weeks"](add-link) by Grizzly Bear.
Now, don't get me wrong, this is a great song which I did listen to but not *this much*.
Faced with the mystery of my missing favorites,
I turned to a tool that has quietly, faithfully tracked my listening habits for years: Last.FM.

### Last.FM

For those unfamiliar, [Last.FM](add-link) is a music tracking service that "scrobbles", or records,
every song you listen to across various platforms.
It creates a detailed log of your music history, minute by minute, play by play.
While it isn’t as flashy as Spotify Wrapped, it's built around the idea of precision and transparency.
If you listened to "Sunset" three times in a row at 2 a.m.,
Last.FM knows and it is open to remind you when you wish to.
I have it tracking my music for more than a decade, before I was even listening to any streaming service.

To perform the comparison, I needed Spotify’s version of my listening stats.
Unfortunately, Spotify doesn't provide users with a full, downloadable record of their annual listening history.
However, they do generate a playlist called "Your Top Songs 2024",
which compiles what they claim are your most played songs of the year.
I extracted the tracklist from this playlist and used it as the best available proxy for Spotify’s internal ranking.

With the two lists,Last.FM’s data and Spotify’s playlist, side-by-side,
the discrepancies became immediately obvious.

![visual-comarison](comparing.png)

As you can see my instincts where right regrading "Sunset".
In general the two lists doesn't look unrelated but there are significant discrepancies.
But how bad is it?
How far are the two lists from each other?
What does "far" even mean in this context?

## How different are the lists?

### Intuitive metric: Jaccard Similarity

First, do the lists even talk about the same songs?
[Jaccard Similarity](add-link) looks only at membership, not order: overlap / union.
When running this similarity test on my Spotify vs Last.fm data gives 0.639,
meaning roughly 64% of the unique tracks appear on both lists.
Good news: the playlists are not strangers, bad news: a third of the songs are unique to one source.
Still, as intuitive and simple this metric is, it is clear it missed a crucial point - order and ranking.
Placing 'sunset' outside my top-10 of the year really feels off and Jaccard doesn't reflect such miss.

### The stats head instinct: Spearman list correlation

This is the statisticians immediate go-to tool for such analysis.
[Spearman list correlation](add-link) asks: if I rank both lists, do the positions line up?
If we number the songs somehow, will the resulting lists of numbers up and down together,
even if not at the same speed?
Here it landed at -0.201.
Negative means the rank orders tilt against each other - when Spotify says “high”, Last.FM often says “mid” or “low”.
It’s not a perfect inversion, but it shows order disagreements even among the shared songs.

### The ML flavored: Edit Distance

Anyone which ever dealt with some sort of natural language processing tasks (NLP) knows this one.
Our lists are not words but we can pretend they are.
If we treat each list as a sequence, [edit distance](add-lin) counts how many insert/delete/move operations it takes to morph one into the other.
The raw distance here is 88 (normalized 0.880 out of 1), which is high.
Translation: if you start with Spotify's lists you’d be editing a lot to make its order look like Last.FM’s, so the sequencing disagreements are substantial.

### Rethinking: Bubble-Sort Distance (and Kendall Tau)

If we keep this line of "how hard will we had to work to make one list look like the other" idea, we could replace the insert/delete/move operations of the Edit Distance into one action: "swap".
[Bubble-Sort distance](add-link), based on the idea behind the famous [sorting algorithm](add-link), measures how many adjacent swaps you’d need to align the two orders.
For me this feels more appropriate for comparison which deals mainly with ranking.
Note that as there are songs which appear on one lists only, we can't get them by merely swapping, so I added a step on which we concatenated the missing songs to the end of the lists, one might argue that this isn't the perfect way of doing this but it was the most straight forward for me.
After digging a bit online I realized that this metric have another name: Kendall Tau Distance.
[Kendall Tau is Bubble-Sort Distance normalized](add-source).
I then also realized that this distance have a 'correlation cousin': The Kendall Tau Correlation Coefficient, [which can be calculated by using a different normalization factor](add-source).
Kendall Tau Correlation here is -0.089, almost neutral but slightly negative.
The normalized bubble-sort distance is 0.521. So even if you only let yourself swap neighbors, you’d be doing about half the possible swaps to get alignment, still a messy reorder.

### Niche Idea: RBO

While looking online about Kendall Tau I found a paper which mentioned a slightly different metric which I found interesting:
[Rank-Biased Overlap (RBO)](add-link).
This one is top-heavy by design, early positions count more and the influence decays with depth, using a 'decay factor' `p`.
Using the default `p=0.9`, we get 0.654.
That says the highest-ranked songs overlap more than the tail suggests.
The lists agree more on what’s “very top” than on the mid-to-low ranks.
Interesting.

## Which metric makes more sense?

To be honest, I am not sure.
Even though Jaccard ignores the order of the songs, it is important to note that all the ranking-aware metrics doesn't take into account **all the songs in the world which were not listed at neither list!**.
Meaning that this view as the lists being uncorrelated or even negatively correlated is in the narrow world for those 100-200 songs on the two lists.
In a way they can be seen as complimentary metric to Jaccard.
From those ranking-aware metrics I can't really decide as it feels that each tells me a slightly different story and highlight a slightly different aspect.
My gut goes with Kendall Tau.
But it might be a matter of taste.

Anyway, the results point to the fact that the top is quite similar but just quite.
As we keep going down the list the discrepancies seems to get larger, or maybe just some songs "fall off" out of one of the top-100 but not the other.

## Putting all the scores in some context

### Creating mock data

I found it hard to make sense of all those numbers. Is 0.52 high? Is it low? What about 0.88?
In order to put those number in prespective I created 3 mock-lists to compare:
1. Shuffled - My Spotify list randomly shuffled
2. Swapped - My Spotify list when every two adajcent songs got swapped
3. Fake - Dummy list with entries such as "Song 1" by "Artist 1"

First let's look at those visually.
![four-plots](add-image)

I feels sensible to say that the "Fake" one is our "worst cast". The "Shuffled" is really bad even though it contains all my top-100 songs and the swapped is actually quite OK, even good.
Armed with this I ran the same comparisons as above and aggregated them all into one nice table:

| target | edit distance | edit distance (norm) | bubblesort distance | kendall tau | spearman | jaccard | rbo | composite score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Last.fm | 88 | 0.88 | 0.21 | 0.58 | -0.2 | 0.64 | 0.65 | 0.48 |
| Shuffeled | 99 | 0.99 | 0.49 | 0.03 | 0.04 | 1.0 | 0.08 | 0.34 |
| Swapped | 51 | 0.51 | 0.01 | 0.98 | 0.999 | 1.0 | 0.84 | 0.9 |
| Fake | 100 | 1.0 | 0.5 | -0.01 | -0.86 | 0.0 | 0.0 | 0.0 |

I guess we can that my Last.fm data sits somewhere between the “Swapped” (very similar) and “Shuffled” (very different) baselines, but noticeably closer to Shuffled than I expected.
Note: the composite score I built isn’t meant to be a canonical metric, but it’s a sanity check that captures the general magnitude of difference across all methods.
Here, Last.fm’s composite score (0.48) is far from the near-perfect “Swapped” scenario (0.90), and much closer to the chaotic “Shuffled” case (0.34).
In other words: there is a serious gap between Spotify's list and Last.fm's list.
It’s not "total randomness," but it’s also not "a few mistakes."

### Table comparison

## Spotify raw data!

### Realization that this exists and sending a request

### Comparing top songs according to the raw data and the Wrapped list

### Computing the metrics for raw-vs-wrapped

## Conclusion? Is there any?

