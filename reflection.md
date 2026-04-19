# Reflection: Profile Comparisons

For each pair of profiles below, a short comparison of what changed
between the top recommendations and why the difference makes sense.
The goal is to show that the scoring logic is actually testing for what
the user profile says, not producing the same list regardless of input.

## High-Energy Pop vs. Chill Lofi

- **Pop profile** surfaced Sunrise City (pop/happy, energy 0.82) as #1.
- **Lofi profile** surfaced Library Rain (lofi/chill, energy 0.35,
  acoustic) as #1.

The top pick flips entirely. The pop profile's high target energy (0.85)
pushes fast tracks up; the lofi profile's low target energy (0.35)
rewards slow tracks. The acoustic bonus only activates for the lofi
profile, which is why the pop profile's #2 is a non-acoustic "gym"
track while the lofi profile's top two are both acoustic lofi tracks
in a near tie. This is the scoring logic behaving correctly: the
categorical matches line up and the energy curve visibly pulls the
recommendations toward different parts of the catalog.

## High-Energy Pop vs. Deep Intense Rock

- **Pop profile** top: Sunrise City (pop, happy).
- **Rock profile** top: Storm Runner (rock, intense).

Both profiles want high-energy music, but they want it from different
places. The pop profile rewards "happy" tracks; the rock profile
rewards "intense" tracks. Gym Hero, which is pop + intense, appears in
both lists but at different ranks (#2 for pop, #4 for rock) because
only one of the two categorical matches fires each time. That's a nice
sanity check that the weighting is doing what it claims: same song,
same features, but ranked differently depending on what the user
actually wants.

## Deep Intense Rock vs. Chill Lofi

- **Rock profile** prefers high energy (0.9) and intense mood.
- **Lofi profile** prefers low energy (0.35) and chill mood.

These two profiles share almost nothing. Their top lists have zero
overlap. Storm Runner (rock's #1) does not appear anywhere in lofi's
top 5; Library Rain (lofi's #1) does not appear anywhere in rock's top
5. This is a good sign that the system can actually separate
fundamentally different tastes.

## Clean Profiles vs. Adversarial (Contradictory)

- **Three clean profiles** returned top picks that felt musically right.
- **Contradictory profile** (indie + melancholic + energy 0.9) returned
  Holocene - genre and mood match, but at energy 0.42 it is the
  opposite of what the user asked for.

This is where the system visibly breaks. It breaks quietly, though: the
reasons list still sounds fine ("genre match, mood match, some energy
similarity"). The user would have to already know the song to realize
it is not "high energy" at all. This is why I don't think transparency
alone is enough. The scorer needs a way to warn when a profile's
numeric target (energy) and its categorical targets (genre + mood)
disagree sharply - and this one doesn't.

## Plain-language version (for a non-programmer)

The system gives every song a score. Songs that share the user's
favorite genre get 2 bonus points. Songs with the same mood get 1.5.
Songs close to the user's preferred energy get up to 1 more point.
Songs close to the user's preferred valence (how bright or sad the
song feels) get up to half a point. Acoustic fans get half a point for
acoustic songs. Whichever song ends up with the highest total wins.

So when "Gym Hero" keeps showing up for people who just asked for
"happy pop," it's because Gym Hero is a pop song with high energy,
which hits two out of the three things the user asked for, even though
its mood is "intense" rather than "happy." The system can't tell the
difference between "close enough" and "wrong" - it just adds up points.
