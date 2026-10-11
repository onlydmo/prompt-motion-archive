# AI motion graphics prompts: what 230 real examples show

Source: https://prompt-motion.com/blog/ai-motion-graphics-prompts

---

Blog

AI motion graphics prompts: what 230 real examples show

One 26-word prompt was copied 33 times, and its results ranged from 0 likes to 17,000. What 230 real Claude prompts reveal about getting good motion graphics.

Oct 10, 2026

Thirty-three people pasted the same 26-word prompt into Claude and posted the video it made. The least successful posts got no likes at all. The most successful got 17,023.

That spread is the clearest lesson in the Prompt Motion gallery, which collects motion graphics videos made with Claude, each shown with the exact prompt behind it. Between September 23 and October 8, 2026, it took in 233 entries from 216 creators, 230 of them with the prompt included. We went through every one.

The gallery in numbers

What we counted

Result

Entries

233, from 216 creators

Entries with the prompt shared

230

Model

Claude Opus 5.5, every one

Median prompt length

26 words

Middle half of prompts

18 to 36 words

Longest prompt

2,082 words

Most common kinds of video

Launch videos (94), showreels (78), explainers (27)

Most common subjects

Product UI (100), kinetic type (97)

Most prompts are a sentence or two. A small number run to hundreds or thousands of words, and those turn out to matter.

What is the most popular AI motion graphics prompt?

The most-copied prompt in the gallery asks Claude to make a 15-second showreel of its own skills as a motion designer. Thirty-three entries use it word for word, one in seven prompts in the gallery. Here it is:

Prompt by

@

stephanlivera

Copied

Copy

make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's your showreel for a résumé. go all out.

Its influence goes further than the exact copies. Five more entries use a shorter Chinese prompt along the same lines, and 78 prompts, a third of the total, open with the same "Make a dynamic N-second motion graphics video" line before changing the length or the subject.

It spread for good reasons. The first post of it in the gallery got 6,760 likes, and the most-liked entry in the whole gallery is one of its runs. It also asks for nothing: no product, no brand, no assets. Anyone can paste it and see what Claude does on its own.

Does the same prompt give the same video?

No. Four of the 33 runs:

S

@

stephanlivera

Prompt

H

@

himanshutwtxs

Prompt

B

@

blue_clarity

Prompt

M

@

m1n9_k7

Prompt

How the likes spread across all 33:

Likes

Runs

Under 10

19

10 to 99

6

100 to 999

3

1,000 or more

5

The median run got 5 likes.

Likes aren't a clean measure of quality. They depend on how many followers the poster has and on timing, and early posts of a trend get attention later copies can't. But the videos vary too, because the prompt leaves almost every decision open. "Go all out" doesn't say what the video is about, what it should look like, how it's timed or what to avoid. Each run settles those on its own, so the results scatter.

Settings outside the prompt didn't close the gap. Six of the 33 creators said they used Claude's maximum effort setting, and their runs landed at both ends of the table, from 1 like to 17,023.

What the strongest long prompts do differently

The second most-liked entry in the gallery, at 12,103 likes, is one shape morphing through a dozen UI states:

T

@

twoclipping

Prompt

Its prompt is 474 words:

Prompt by

@

twoclipping

Copied

Copy

<inputs>
Ask me for: 8 to 12 UI states I want the shape to become (e.g. button, loader, player, slider, toggle, tabs, chart, command palette, toast), pure black and white or one accent color, and a royalty-free song around 120 BPM (e.g. Mixkit, free for commercial use).
</inputs>

<direction>
Dribbble-level UI motion. One shape, never cut: every state is the same element morphing its size, radius and color while its content swaps with a short blur. A cursor drives every change with real clicks and drags. Light warm-gray canvas, black and white components, one clean UI font (Geist). Springs everywhere, a tiny overshoot at most. The camera zooms so each state fills the frame. The last frame is the first frame, so it loops.
Banned: bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template.
</direction>

<structure>
120 BPM, 7 bars, something happens on every beat.
Button → loader → check → dynamic island → music player with a play/pause morph → scrub the progress bar → it becomes a volume slider that stretches when dragged past max → a toggle flips on the beat → the knob becomes a liquid tab indicator → the tabs open into a chart that draws itself, with a tooltip on hover → it collapses into ⌘K → type to filter → enter → toast → back to the button.
</structure>

<build>
1. One HTML file, square 1440x1440. Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames.
2. Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change, so it stays a pure function of time.
3. The tab indicator's two edges ride different springs, so the leading edge stretches ahead of the trailing one. Same trick for the toggle knob.
4. Drags are direct manipulation: while the cursor is held, the value is computed from its position. On release it springs back from wherever it was.
5. Analyze the song with numpy for the beat grid and start on a downbeat. Place every UI sound by its measured peak.
6. Render with Playwright: 4 subframes per frame, blended with ffmpeg tmix for motion blur at 60fps.
7. Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read.
</build>

<gotchas>
Never put will-change on anything the camera scales or the text renders blurry. Text that swaps inside a morphing container needs its own enter and exit timing or it overlaps. Make the last frame identical to the first, cursor position and speed included, or the loop stutters.
</gotchas>

<start>
Ask me for the inputs, then show me the state list on the beat grid before you write any code.
</start>

Show all

The same five parts keep showing up in the long prompts behind the gallery's best-received videos.

One concept.

"One shape, never cut" gives every shot a reason to exist. When a prompt leaves the concept open, Claude tends to make a tour of effects instead.

A banned list.

Glows, particle bursts, bouncy easing, crossfades, "anything that looks like a template." Only 16 prompts in the gallery have one, but four of the 20 most-liked entries do. We cover these in

why AI motion graphics look AI-made

.

Timing to a beat.

A tempo and a bar count, such as "120 BPM, 7 bars, something happens on every beat," in place of the word "dynamic." Cuts then have a grid to land on.

A build method.

How the video gets rendered, not just what it shows. The common recipe is one HTML file where every frame is computed from the time, captured frame by frame in a headless browser and blended for motion blur. That avoids the dropped frames and timing drift of screen-recording a live animation. More in

Remotion vs HyperFrames vs plain HTML

.

A review step.

"Render one frame per beat before the full render. Fix anything off the grid, cramped or hard to read." Claude checks its own output before finishing, which catches overlapping text and empty frames.

Length isn't the goal in itself. Each of these parts makes a decision Claude would otherwise make by default.

The numbers lean the same way. The 19 prompts over 100 words got a median of 56 likes, against 5 for prompts of 26 words or fewer. Treat that with care: it's a small group, and people who write long prompts may also be more experienced or have bigger audiences. The 33 runs of one identical prompt make the stronger case that a short prompt leaves too much to chance.

What people make with it

Launch videos are the biggest category, at 94 entries, and more than a quarter of their prompts are built on the showreel prompt. We looked at those separately in

how to prompt an AI launch video

. Explainers are the category with the shortest prompts, a median of 15 words, and they show it. See

what 27 AI explainer prompts get right and wrong

.

Start from a tested version

We rewrote the showreel prompt with the five parts above. It still needs nothing from you, and you can change the length, style and subject before copying it.

The showreel prompt

The most-used prompt on Prompt Motion: one line asking Opus 5.5 to show off as a motion designer. Our rewrite adds the direction it leaves out, and still needs nothing from you.

Customize it

See the template

Every entry in the

gallery

shows its exact prompt, and you can filter by subject, such as

product UI

or

kinetic type

.

How we counted

Source:

every published entry in the Prompt Motion gallery on October 10, 2026, each a video posted on X with the prompt that made it.

Likes:

as of when we last fetched each post, between October 4 and 8, 2026.

Word counts:

these leave out the 18 prompts written in Chinese, Japanese or Korean, where spaces don't separate words.

Identical prompts:

two prompts count as the same if they match after ignoring capitalization and punctuation.

Settings and tools:

effort level and rendering tool are as reported by each creator, and most didn't say.

Every video here is on

Prompt Motion

, with the exact prompt that made it.
