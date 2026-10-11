# Why AI motion graphics look AI-made, and the prompt lines that fix it

Source: https://prompt-motion.com/blog/make-ai-motion-graphics-look-less-ai

---

Blog

Why AI motion graphics look AI-made, and the prompt lines that fix it

Glows, particle bursts, crossfades, text in the corners. The effects that give AI motion graphics away, taken from the banned lists in real Claude prompts.

Oct 10, 2026

Banned: shockwave rings, particle bursts, RGB split, camera shake, lens flares, neon glows, grid floors, flashing backgrounds, bouncy easing.

That line comes from the prompt behind a promo video for a user-generated ad tool, which got 607 likes. Prompts with a list like it are rare in the Prompt Motion gallery: 16 of the 230, from 12 creators. But they include four of the 20 most-liked entries, and their median of 56 likes compares with 7 for the gallery as a whole.

Every one of those lists is trying to remove the same thing: the look of motion graphics nobody designed. Here's what's on them and why each item gives a video away.

What the banned lists ban

Banned

Prompts

Creators

Glows, including neon

7

4

"Anything that looks like a template"

7

5

Particle bursts

6

3

Long holds, frozen frames, dead time

6

4

Crossfades

5

4

Bouncy easing

3

2

Gradients

3

3

3D effects

3

3

Stock footage or stock UI kits

3

2

Text in the corners

2

2

Math.random

2

1

Some creators posted several videos with the same list, so the creators column is the fairer count.

T

@

twoclipping

Prompt

U

@

ultimaxbt

Prompt

N

@

notdwd

Prompt

1

@

1littlecoder

Prompt

Why these effects read as AI-made

Glows and particle bursts

Glows, particle bursts and lens flares are the quickest ways to make a frame look rich, which is why they're the first things on most lists. The trouble isn't the effects themselves. When nothing in the video calls for them, they read as decoration.

One prompt puts the rule better than a list can. It bans "motion that isn't connected to an element already on screen." If a burst doesn't come from something and go somewhere, it's filler.

Crossfades and blur-ins

A crossfade is what you get when no one designed the transition. One shot dissolves into the next, and nothing connects them. The prompts that ban crossfades usually say what to do instead, such as "every state is the same element morphing" or "The orange dot connects every scene." The transition becomes part of the idea, not a gap between ideas.

Bouncy easing

Springy overshoot on every element makes motion feel cartoonish. The prompts that ban it still use springs, but they limit them: "Springs everywhere, a tiny overshoot at most." Another says "avoid cartoon springiness."

Text in the corners

Two creators ban it in the same words: "Avoid the frames and texts on the corners which are typical ai made giveaways!" This usually means small labels, frame markers and readouts placed around the edges like a heads-up display. They suggest detail without carrying any information.

Dead time

"Holds longer than 1s" and "dead time" appear in six prompts. A held frame works when the viewer needs time to read something. Without that reason, it's a stretch where nothing happens, and it makes a 15-second video feel slow.

Anything that looks like a template

This is the catch-all, and seven prompts end their list with it. It doesn't name an effect. It tells Claude the standard it's being held to, so effects not on the list get the same scrutiny.

Math.random

This one is about the build, not the look. If an animation uses random numbers, every render comes out different, so a frame you fixed can change on the next run. Banning it keeps each frame reproducible.

How to write your own banned list

Start with the common tells.

Glows, particle bursts, crossfades, bouncy easing, text in the corners.

Add what you've seen go wrong.

Run your prompt once and list anything in the result you didn't ask for. That's your list.

Say what to do instead.

"No crossfades: every scene grows out of the one before" works better than "no crossfades" alone.

End with the standard.

"Anything that looks like a template" covers what you didn't think to list.

Keep it short.

Most lists in the gallery are a single line of five to nine items.

Here's the full prompt behind the orange dot video above, which builds its banned list into its direction:

Prompt by

@

ultimaxbt

Copied

Copy

<inputs>
Ask me for: a short label for the opening toggle, one hero word, a percentage for the graph, the text for the final card, one accent color, and a track with a clear beat.
</inputs>

<direction>
A 2D motion design film in 16:9. Use a warm off-white canvas, near-black backgrounds, bold typography and one vivid orange accent. The orange dot connects every scene: it starts in the UI, becomes the dot over a letter, traces a spring graph, grows into a shape and returns on the end card. A cursor makes the opening click feel real. Keep the motion sharp and controlled, with small spring overshoots and no dead time.
Banned: stock footage, gradients, glows, particle bursts, random transitions and motion that isn't connected to an element already on screen.
</direction>

<structure>
Around 15 seconds, with a visual change on every major beat.
Open: a cursor clicks the orange toggle beside "Reduce Motion". The letters bend and move into place until only "Motion" remains, with the orange dot above the "i".
Spring: the dot jumps away from the word and lands on a graph. Its path draws a spring response, overshoots the target and settles beside a "+22%" callout.
Shape: the dot shoots across a line, grows into an orange circle and fills the frame. A black rounded square rotates inside it, then stretches into a pill. The scene contracts to a single orange dot on black.
Type: words like "SPRINGS", "EASING", "KINETIC TYPE", "3D" and "SOUND" orbit the dot. The circle of type opens out into a field of tiny dots.
Reveal: the halftone field expands and flips to black, revealing the final card: "Opus 5.5", "Motion designer." and "0 keyframes".
Return: the orange dot moves back through the halftone, graph and toggle. Match the final frame to the first so the video loops cleanly.
</structure>

<build>
1. One HTML file, 1920x1080 at 60fps. Compute every visual from time inside seek(t): no CSS transitions, timers or state carried between frames.
2. Use closed-form springs for the toggle, bouncing dot and graph. Draw the graph from the same spring function that moves the dot.
3. Animate letters individually for the "Reduce Motion" to "Motion" transformation. Keep the orange dot attached to the "i" until it begins its jump.
4. Make the orange circle, rotating square and pill different states of the same shape. Preserve its position and motion through each transformation.
5. Place the orbiting words along a circular path, then move their letters outward to hand the frame over to the halftone grid.
6. Draw the halftone as a grid of dots whose sizes respond to the orange dot. Let it grow past the frame edges before revealing the end card.
7. Sync the click, dot landing, graph peak, shape changes and final title to measured beats. Render one frame per beat to check the pacing before the full export.
</build>

<gotchas>
The graph and dot must follow the same motion or the spring will feel fake. Keep the orange accent consistent across every scene. Give outgoing and incoming text separate timing so letters don't overlap. When a shape fills the screen, scale it past all four corners. Match the cursor, dot and typography in the first and last frames to avoid a loop stutter.
</gotchas>

<start>
Ask me for the inputs, then show me the beat map and four stills (toggle, graph, kinetic type, end card) before building the full video.
</start>

Show all

Our rewrite of the gallery's most-copied prompt includes a banned list too: no particle bursts, glows, camera shake or crossfades.

The showreel prompt

The most-used prompt on Prompt Motion: one line asking Opus 5.5 to show off as a motion designer. Our rewrite adds the direction it leaves out, and still needs nothing from you.

Customize it

See the template

For the other parts these prompts share (a single concept, a beat grid, a build method and a review step), see

what 230 AI motion graphics prompts show

.

How we counted

Source:

the 230 entries with prompts in the Prompt Motion gallery on October 10, 2026, each a video posted on X.

Banned lists:

prompts with a line starting "Banned," "Avoid," "Don't use," "Do not use" or "Never use," or one naming "AI giveaways." Counts are of prompts whose list includes each item.

Likes:

as of when we last fetched each post, between October 4 and 8, 2026. They also reflect the poster's audience, and people who write banned lists tend to write long, detailed prompts overall, so the lists alone don't explain the difference.

Every video here is on

Prompt Motion

, with the exact prompt that made it.
