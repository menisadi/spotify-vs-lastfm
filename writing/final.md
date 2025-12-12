# Spotify Wrapped Was Off - But By How Much? A Statistical Deep Dive

## Background

Every December, Spotify Wrapped drops into our feeds like clockwork,
offering a personalized summary of our listening habits.
It’s fun, vibrant, and sometimes feels spot-on.
But let’s be honest, almost every year there are some details that just feel off.
I'm not talking about the fact that "Baby Shark" made its way to my top songs -
this one I can explain.
I'm talking about that one song which you *do* listen to, but you are quite sure not **that** much.
Or a song you had on repeat and still didn’t manage to crack your top 10 somehow.
Last year, [several](https://switchedonpop.com/episodes/breaking-through-doechii-mkgee-rose) [claims](https://www.musicradar.com/music-industry/streaming-sharing/spotify-says-they-got-your-wrapped-2024-wrong-but-this-year-theyre-going-to-fix-it) about the [inaccuracy](https://www.reddit.com/r/truespotify/comments/1h6fxdc/2024_spotify_wrapped_was_awful/) of Spotify Wrapped cropped up in the media.
For me it was ["Sunset"](https://open.spotify.com/track/203bhpOhWluOytYjvwQfl7?si=254130e627294591) by the talented Caroline Polachek, which I just couldn't get enough of,
yet Spotify placed it at the modest no. 17.
Meanwhile, one spot below came ["Two Weeks"](https://open.spotify.com/track/0iTpQYzJnYgh7kIxyq8A2O) by Grizzly Bear.
Now, don't get me wrong, this is a great song which I did listen to - but not *this much*.
Faced with the mystery of my missing favorites,
I turned to a tool that has quietly, faithfully tracked my listening habits for years: Last.fm.

### Last.fm

For those unfamiliar, [Last.fm](https://www.last.fm/) is a music tracking service that "scrobbles," or records,
every song you listen to across various platforms.
It creates a detailed log of your music history, minute by minute, play by play.
While it isn’t as flashy as Spotify Wrapped, it's built around the idea of precision and transparency.
If you listened to "Sunset" three times in a row at 2 a.m.,
Last.fm knows, and it is open to remind you when you wish it to.
I have had it tracking my music for more than a decade, before I was even listening to any streaming service.

To perform the comparison, I needed Spotify’s version of my listening stats.
Unfortunately, Spotify doesn't provide users with a full, downloadable record of their annual listening history.
However, they do generate a playlist called "Your Top Songs 2024,"
which compiles what they claim are your most played songs of the year.
I extracted the tracklist from this playlist and used it as the best available proxy for Spotify’s internal ranking.

With the two lists - Last.fm’s data and Spotify’s playlist - side by side,
the discrepancies became immediately obvious.

![visual-comarison](plots/spotvslast.png)

As you can see, my instincts were right regarding "Sunset."
In general, the two lists don’t look unrelated, but there are significant discrepancies.
But how bad is it?
How far are the two lists from each other?
What does "far" even mean in this context?

## How different are the lists?

### Intuitive metric: Jaccard Similarity

First, do the lists even talk about the same songs?
[Jaccard Similarity](https://en.wikipedia.org/wiki/Jaccard_index) looks only at membership, not order: overlap / union.
When running this similarity test on my Spotify vs. Last.fm data, it gives 0.639,
meaning roughly 64% of the unique tracks appear on both lists.
Good news: the playlists are not strangers.
Bad news: a third of the songs are unique to one source.
Still, as intuitive and simple as this metric is, it is clear it misses a crucial point - order and ranking.
Placing "Sunset" outside my top 10 of the year really feels off, and Jaccard doesn't reflect such a miss.

### The stats-head instinct: Spearman list correlation

This is the statistician’s immediate go-to tool for such analysis.
[Spearman list correlation](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) asks:
if I rank both lists, do the positions line up?
If we number the songs somehow, will the resulting lists of numbers move up and down together,
even if not at the same speed?
Here it landed at -0.201.
Negative means the rank orders tilt against each other - when Spotify says "high," Last.fm often says "mid" or "low."
It’s not a perfect inversion, but it shows order disagreements even among the shared songs.

### The ML-flavored: Edit Distance

Anyone who has ever dealt with some sort of natural language processing task (NLP) knows this one.
Our lists are not words, but we can pretend they are.
If we treat each list as a sequence, [edit distance](https://en.wikipedia.org/wiki/Edit_distance) counts how many insert/delete/move operations it takes to morph one into the other.
The raw distance here is 88 (normalized 0.880 out of 1), which is high.
Translation: if you start with Spotify's list, you’d be editing a lot to make its order look like Last.fm’s,
so the sequencing disagreements are substantial.

### Rethinking: Bubble-Sort Distance (and Kendall Tau)

If we keep this line of "how hard would we have to work to make one list look like the other,"
we could replace the insert/delete/move operations of the edit distance with one action: **swap**.
Bubble-sort distance, based on the idea behind the famous [sorting algorithm](https://en.wikipedia.org/wiki/Bubble_sort),
measures how many adjacent swaps you’d need to align the two orders.
For me this feels more appropriate for a comparison that deals mainly with ranking.
Note that, as there are songs which appear on one list only, we can't get them by merely swapping,
so I added a step in which we concatenated the missing songs to the end of the lists.
One might argue that this isn't the perfect way of doing this, but it was the most straightforward for me.

After digging a bit online, I realized that this metric has another name: **Kendall Tau Distance**.
[Kendall Tau is Bubble-Sort Distance normalized.](https://en.wikipedia.org/wiki/Kendall_tau_distance)
I then also realized that this distance has a "correlation cousin": the **Kendall Tau Correlation Coefficient**,
[which can be calculated by using a different normalization factor.](https://en.wikipedia.org/wiki/Kendall_tau_distance#Comparison_to_Kendall_tau_rank_correlation_coefficient)

Kendall Tau correlation here is -0.089, almost neutral but slightly negative.
The normalized bubble-sort distance is 0.521.
So even if you only let yourself swap neighbors, you’d be doing about half the possible swaps to get alignment - still a messy reorder.

### Niche idea: RBO

While looking online about Kendall Tau, I found a paper that mentioned a slightly different metric I found interesting:
[Rank-Biased Overlap (RBO)](https://github.com/changyaochen/rbo).
This one is top-heavy by design: early positions count more,
and the influence decays with depth using a "decay factor" `p`.
Using the default `p=0.9`, we get 0.654.
That says the highest-ranked songs overlap more than the tail suggests.
The lists agree more on what’s "very top" than on the mid-to-low ranks.
Interesting.

## Which metric makes more sense?

To be honest, I am not sure.
Even though Jaccard ignores the order of the songs, it is important to note that all the ranking-aware metrics ignore **all the songs in the world which were not listed on either list!**
Meaning that this view of the lists being uncorrelated or even negatively correlated is in the narrow world of the 100–200 songs on the two lists.
In a way, they can be seen as complementary to Jaccard.

From those ranking-aware metrics I can't really decide,
as it feels that each tells me a slightly different story and highlights a slightly different aspect.
My gut goes with Kendall Tau.
But it might be a matter of taste.

Anyway, the results point to the fact that the top is quite similar - but just quite.
As we keep going down the list, the discrepancies seem to get larger,
or maybe just some songs "fall off": out of one top 100 but not the other.

## Putting all the scores in some context

### Creating mock data

I found it hard to make sense of all those numbers. Is 0.52 high? Is it low? What about 0.88?
In order to put those numbers in perspective, I created 3 mock lists to compare:

1. **Shuffled** - my Spotify list randomly shuffled
2. **Swapped** - my Spotify list where every two adjacent songs got swapped
3. **Fake** - a dummy list with entries such as "Song 1" by "Artist 1"

First, let’s take a peek at those visually.

|  # | Spotify             | Swapped             | Shuffled                    | Fake     |
| -: | :------------------ | :------------------ | :-------------------------- | :------- |
|  0 | Red Wine Supernova  | Bunny Is A Rider    | labour                      | Track 1  |
|  1 | Bunny Is A Rider    | Red Wine Supernova  | Real Love Baby              | Track 2  |
|  2 | Too Sweet           | CHIHIRO             | Ship To Wreck               | Track 3  |
|  3 | CHIHIRO             | Too Sweet           | boys  bugs and men          | Track 4  |
|  4 | Don't Blame Me      | God Needs The Devil | Vampire Empire              | Track 5  |
|  5 | God Needs The Devil | Don't Blame Me      | Now I'm In It - Bonus Track | Track 6  |
|  6 | Silk Chiffon        | BIRDS OF A FEATHER  | Oh Caroline                 | Track 7  |
|  7 | BIRDS OF A FEATHER  | Silk Chiffon        | Two Weeks                   | Track 8  |
|  8 | Sailor Song         | Ship To Wreck       | Blinding Lights             | Track 9  |
|  9 | Ship To Wreck       | Sailor Song         | CHIHIRO                     | Track 10 |

It feels sensible to say that the "Fake" one is our "worst case."
The "Shuffled" one is really bad even though it contains all my top-100 songs,
and the "Swapped" one is actually quite OK - even good.

### Comparison Table

Armed with this, I ran the same comparisons as above and aggregated them all into one nice table:

| target   | edit distance | edit distance (norm) | bubblesort distance | kendall tau | spearman | jaccard | rbo  | composite score |
| :------- | :------------ | :------------------- | :------------------ | :---------- | :------- | :------ | :--- | :-------------- |
| Last.fm  | 88            | 0.88                 | 0.21                | 0.58        | -0.2     | 0.64    | 0.65 | 0.48            |
| Shuffled | 99            | 0.99                 | 0.49                | 0.03        | 0.04     | 1.0     | 0.08 | 0.34            |
| Swapped  | 51            | 0.51                 | 0.01                | 0.98        | 0.999    | 1.0     | 0.84 | 0.9             |
| Fake     | 100           | 1.0                  | 0.5                 | -0.01       | -0.86    | 0.0     | 0.0  | 0.0             |

I guess we can see that my Last.fm data sits somewhere between the "Swapped" (very similar) and "Shuffled" (very different) baselines,
but noticeably closer to Shuffled than I expected.
Note: the composite score I built isn’t meant to be a canonical metric,
but it’s a sanity check that captures the general magnitude of difference across all methods.
Here, Last.fm’s composite score (0.48) is far from the near-perfect "Swapped" scenario (0.90),
and much closer to the chaotic "Shuffled" case (0.34).
In other words: there is a serious gap between Spotify's list and Last.fm's list.
It’s not "total randomness," but it’s also not "a few mistakes."

## Spotify raw data!

### Realization that this exists and sending a request

At some point in this rabbit hole, I had a very simple thought:

> "Wait… Spotify *must* have the real numbers. Can’t I just… ask for them?"

Turns out: yes, you actually can.

Hidden behind a few menus in your account settings is a privacy/data section
where you can request a full export of your Spotify data.
Among other things (login logs, account info, etc.), you can ask for your extended streaming history -
basically a raw log of what you listened to, when, and for how long.

So I sent the request, forgot about it, and a few days later an email showed up with a link to a zip file.

Inside the archive were several JSON files with names like:

* `Streaming_History_Audio_2024_0.json`
* `Streaming_History_Audio_2024_1.json`

At last, the source of truth: every play, every skip, every late-night loop of "Sunset" is in there.

To make this comparable to Wrapped, I did a few basic cleanup steps,
aggregated play counts for each track, and filtered the top 100.
From that, I built **Spotify Raw Top 100**.

### Comparing top songs according to the raw data and the Wrapped list

Once I had the raw-based top-100 list, I put it side-by-side with the Wrapped playlist.

![spotify-vs-spotify](plots/spotvsspot.png)

Long story short - they are not the same.
Subjectively, the raw top 20 felt much more like "yes, this is my year in music."

That’s the qualitative side. Now, let’s look at the numbers.

### Computing the metrics for raw-vs-wrapped

I ran exactly the same battery of metrics as before.
Here is the updated table:

| target      | edit distance | edit distance (norm) | bubblesort distance | kendall tau | spearman | jaccard | rbo  | composite score |
| ----------- | ------------- | -------------------- | ------------------- | ----------- | -------- | ------- | ---- | --------------- |
| **Last.fm** | 88            | 0.88                 | 0.21                | 0.58        | -0.20    | 0.64    | 0.65 | **0.48**        |
| **Raw**     | 93            | 0.93                 | 0.17                | 0.67        | -0.21    | 0.70    | 0.61 | **0.46**        |
| Shuffled    | 99            | 0.99                 | 0.49                | 0.03        | 0.04     | 1.00    | 0.08 | 0.34            |
| Swapped     | 51            | 0.51                 | 0.01                | 0.98        | 0.999    | 1.00    | 0.84 | 0.90            |
| Fake        | 100           | 1.00                 | 0.50                | -0.01       | -0.86    | 0.00    | 0.00 | 0.00            |

### So where does Raw vs Wrapped actually land?

**In one sentence:**
**Spotify Wrapped disagrees with Spotify’s own raw listening logs almost exactly as much as it disagrees with Last.fm** - both sit around the same mid-range "not random, but not close enough" zone.*

## Conclusion? Is there any?

I'm not sure I know what Spotify did or how their numbers ended up being such a mismatch.
Is this intentional?
Is there a reason or a deliberate bias?
I don't know, and I have no indication that this is the case.
I just know that the folks there are sitting on a huge gold mine of cool data,
and what they end up doing with it is this mess.
It might not bother me as a user, but it offends me as a data scientist.

