# AI explainer video prompts: what 27 examples get right and wrong

Source: https://prompt-motion.com/blog/ai-explainer-video-prompts

---

Blog

AI explainer video prompts: what 27 examples get right and wrong

The prompts behind 27 explainer videos made with Claude. The best gave Claude a process to show from start to finish. None asked it to check its facts.

Oct 10, 2026

The most-liked explainer in the Prompt Motion gallery shows how to make a Negroni. Its prompt is 65 words, and it got 1,028 likes. A prompt asking for "a professional explainer video" for a business website got none.

The gallery has 27 explainer videos made with Claude, each with its prompt. They have the shortest prompts of any category, a median of 15 words, against 26 for the gallery as a whole. Here's what the ones that worked have in common, and what nearly all of them leave out.

The best-received explainers

R

@

Ror_Fly

Prompt

E

@

emollick

Prompt

A

@

alex_prompter

Prompt

L

@

LinearUncle

Prompt

The top four take different routes: a cocktail recipe, recursion told in a different video style each time, a 30-second business explainer, and a lesson on derivatives made with Manim, a Python animation library built for math videos. The first three share one thing: the prompt tells Claude what the video is made of, not just what it's about.

Give Claude a process with a start and an end

Here's the Negroni prompt:

Prompt by

@

Ror_Fly

Copied

Copy

We're going to try a little test. Do you think you could render a recipe motion graphic animation using javascript or html (w/e you think will produce the best) to show the full recipe from start to finish (empty glass to completed cocktail) - Explainer video style - Showing the recipe ingreidents + measurements as they're going into the cup. Should be a 30s video.

"From start to finish (empty glass to completed cocktail)" does the heavy lifting. A recipe is a sequence with a visible beginning, middle and end, so the video has a structure before Claude designs a single frame. "Ingredients and measurements as they're going into the cup" says what the labels are and where they go.

Compare a prompt like "make a video highlighting key moments in the history of AI." That's a topic, not a sequence. Claude has to choose which moments, how many, and how to connect them, and those choices are where explainers go generic.

If your topic isn't a physical process, find the sequence inside it: a request moving through a system, a number changing as each input changes, a timeline with a fixed number of stops.

Or give it the scenes

The third most-liked explainer uses a prompt written as a reusable template:

Prompt by

@

alex_prompter

Copied

Copy

Adopt the role of an expert motion designer. Build a 30-second animated explainer for my business as a single HTML page. 5 scenes. The customer's problem, what I do, how it works in 3 steps, one proof point, and my name at the end. Bold text, smooth transitions, my brand colours. My business [DESCRIBE WHAT YOU SELL, WHO IT'S FOR AND YOUR COLOURS]

"5 scenes. The customer's problem, what I do, how it works in 3 steps, one proof point, and my name at the end" is a storyboard in one sentence. It also fixes the length, so each scene gets about six seconds.

The recursion video does something different. "Every explanation about recursion has a radically different video style" is a structural idea, and it makes the subject self-referential. That's hard to copy for every topic, but it shows that a concept can stand in for a scene list.

What most explainer prompts leave out

Across all 27 prompts:

What the prompt specifies

Prompts

A length

8

A visual style (whiteboard, hand-drawn, pixel art and so on)

8

Narration, music or sound

6

Who the video is for

2

Checking facts or citing sources

0

Facts.

An explainer is only useful if it's right, and no prompt asks Claude to check what it puts on screen. For anything with numbers, names or dates, add a line like "Research it first and keep every fact right; never invent numbers or quotes." Then check the result yourself.

Audience.

Only two prompts say who the video is for. One Chinese prompt about Git asks for something "someone with zero computer background can understand." That one line sets the vocabulary, the pace and what needs explaining.

Sound.

Six prompts ask for narration or sound. Without it, every idea has to be readable on screen, which limits how much a 30-second explainer can carry. If you want a voiceover, say so and say how. One prompt asks for edge-tts, a free text-to-speech tool.

A short explainer prompt that covers the gaps

The topic and the audience.

"How a token bucket rate limiter works, for developers who've never built one."

The sequence.

The steps, stages or scenes, in order.

The length.

About five seconds per idea is a reasonable starting point.

The style.

Diagram, whiteboard, hand-drawn or 3D, and a palette.

Accuracy.

"Research it first; never invent numbers."

Sound.

Music, narration, or none.

Every entry has a customize page that turns its prompt into a fill-in template. Start from the

Negroni prompt

for a process, or the

business explainer

for a scene list. The

diagrams

filter shows more explainers.

The same pattern runs through the whole gallery, where long, specific prompts get noticeably more likes. See

what 230 AI motion graphics prompts show

.

How we counted

Source:

the 27 entries in the Prompt Motion gallery's explainer category on October 10, 2026, each a video posted on X with the prompt that made it.

Likes:

as of when we last fetched each post, between October 4 and 8, 2026.

Word counts:

these leave out the four explainer prompts written in Chinese, Japanese or Korean.

Table:

counts come from reading each prompt, so "a length" means the prompt names a duration in seconds or minutes.

Every video here is on

Prompt Motion

, with the exact prompt that made it.
