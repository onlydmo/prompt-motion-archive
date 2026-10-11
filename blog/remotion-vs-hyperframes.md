# Remotion vs HyperFrames vs plain HTML for AI motion graphics

Source: https://prompt-motion.com/blog/remotion-vs-hyperframes

---

Blog

Remotion vs HyperFrames vs plain HTML for AI motion graphics

How the creators of 56 AI motion graphics videos rendered them: Remotion, HyperFrames, plain HTML with Playwright, or Three.js. How each works and when to use it.

Oct 10, 2026

When Claude makes a motion graphics video, it doesn't produce pixels directly. It writes code that draws each frame, and something else turns that code into an MP4. Of the 233 videos in the Prompt Motion gallery, 56 say what did that job:

Rendering approach

Entries

Median likes

Mostly used for

Plain HTML or canvas, captured with a headless browser

23

12

Everything: explainers, launches, UI motion

Remotion

13

5

Launch videos (10 of 13)

HyperFrames

10

24

Launch videos (6 of 10)

Three.js

5

7

3D scenes

Other (Manim, Blender, Python with ffmpeg)

5

One each

The other 177 creators didn't say. Their median was 7 likes.

These are small groups, and likes depend mostly on the video and the poster's audience, not the renderer. Don't pick a tool from the likes column. What the table does show is that all three main approaches can make a well-received video, so the choice comes down to how you work.

R

@

Ror_Fly

Prompt

A

@

anthonyriera

Skill

G

@

gabrielbuzziv

Prompt

N

@

NFT_Chen

Prompt

In order: plain HTML, Remotion, HyperFrames and Three.js.

How each one works

All three main approaches do the same thing underneath. A headless browser loads the animation, moves it to an exact time, takes a screenshot, and repeats for every frame. ffmpeg then encodes the screenshots into a video. Because every frame is computed from the time, not played back live, a slow machine can't drop frames or drift off the beat.

They differ in what Claude writes.

Plain HTML with Playwright

Claude writes one HTML page and a function, usually called

seek(t)

, that sets every element's position, size and color for time

t

. A short script uses

Playwright

to step through the times and save each frame, and

ffmpeg

puts them together.

Nothing needs installing beyond those two, and Claude can use any web technique: CSS, SVG, canvas or WebGL. That's why it's the most common approach in the gallery. Of the ten most-liked entries, four name a tool: three are plain HTML and one is HyperFrames. The catch is that the prompt has to say how to build it. Eleven prompts in the gallery mention

seek(

, and nine mention Playwright. A typical line:

canvas only, no libraries, every frame a pure function of time so my renderer can screenshot it.

Seven prompts also render a few subframes per frame and blend them with ffmpeg, which adds motion blur to fast moves.

Remotion

Remotion

is a framework for making videos with React. Each scene is a React component that reads the current frame number, and Remotion handles the rendering. It also has a studio for previewing the video and adjusting inputs.

In the gallery it's used almost entirely for launch and product videos. That fits: if your product is already built in React, Claude can reuse its components and styles. Remotion isn't open source in the usual sense. Some companies need a paid license, so check

its license terms

before using it commercially.

HyperFrames

HyperFrames

, from HeyGen, renders plain HTML files to MP4 using headless Chrome and FFmpeg. It's open source under the Apache 2.0 license and was designed for AI agents to write. The video is described in HTML with data attributes, so there's no React to set up, and it works with animation libraries like GSAP.

It sits between the other two. You get a ready-made renderer, as with Remotion, while Claude writes HTML, as in the plain approach. Six of its ten entries in the gallery are launch videos, including the most-liked one, a promo for a baby products app at 1,415 likes.

Three.js for 3D

The five

Three.js

entries are all 3D scenes: a dogfight at sunset, an aircraft model, a ball bouncing to a beat. Three.js renders in the browser like the others, so the same capture approach works. If you want real 3D with lighting and a moving camera, it's the natural choice. For flat motion design it adds complexity you don't need.

Which should you use?

You want the simplest setup:

plain HTML with Playwright. Put the build method in the prompt (one HTML file, every frame computed from time, rendered with Playwright and ffmpeg) and Claude handles the rest.

Your product is built in React:

Remotion, so the video can reuse your real components. Check the license first.

You want a renderer built for AI agents without React:

HyperFrames.

You need real 3D:

Three.js, captured the same way.

You're explaining math:

Manim

. One explainer in the gallery used it, with free text-to-speech narration, and got 258 likes.

Whichever you pick, name it in the prompt. Without a build method, Claude chooses one each time, and the results are harder to repeat.

For 3D, our real-time template sets up the whole pipeline in the prompt:

The 3D template

The template behind the improved prompts for real-time three.js pieces. It's set up with Prompt Motion's gallery; swap in your subject.

Customize it

See the template

For what the rest of a strong prompt contains, see

what 230 AI motion graphics prompts show

.

How we counted

Source:

the 56 entries in the Prompt Motion gallery, out of 233 on October 10, 2026, whose creators named the tool used to render the video. The tool is as each creator reported it, and some entries used more than one.

Grouping:

"Plain HTML or canvas" covers entries listed as HTML, canvas, SVG, JavaScript or WebGL, with or without Playwright and ffmpeg.

Likes:

as of when we last fetched each post, between October 4 and 8, 2026.

Tool details:

from each project's own site or repository.

Every video here is on

Prompt Motion

, with the exact prompt that made it.
