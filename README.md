# 🎬 Prompt Motion Archive

> **A complete, permanent offline archive of [Prompt Motion](https://prompt-motion.com/)** — 235 motion design prompts, skills, templates, and 2.54 GB of downloaded MP4 videos generated with Claude Opus 5.5.

[![Entries](https://img.shields.io/badge/Total_Entries-235-indigo.svg)](#)
[![Videos](https://img.shields.io/badge/Downloaded_Videos-235_%282.54_GB%29-emerald.svg)](#)
[![Skills](https://img.shields.io/badge/Claude_Code_Skills-4_Curated-purple.svg)](#)
[![Model](https://img.shields.io/badge/Model-Claude_Opus_5.5-orange.svg)](#)

---

## ⚡ Claude Code Skills (with GitHub Links)

Prompt Motion features specialized coding agent skills that let Claude Code interview you, read codebase components, and render complete animated motion graphics or launch films:

| Skill | Author | GitHub Repository | Install Command | Stack |
|---|---|---|---|---|
| **Cinetic** | [@LexnLin](https://x.com/LexnLin) | [Leonxlnx/cinetic](https://github.com/Leonxlnx/cinetic) | `npx skills add Leonxlnx/cinetic` | Code / Canvas |
| **Product Film Skill** | [@anthonyriera](https://x.com/anthonyriera) | [Rieranthony/product-film-skill](https://github.com/Rieranthony/product-film-skill) | `/plugin marketplace add Rieranthony/product-film-skill`<br>`/plugin install product-film@product-film-skill` | Remotion |
| **Session Story** | [@jake11moran](https://x.com/jake11moran) | [heygen-com/hyperframes-community-skills](https://github.com/heygen-com/hyperframes-community-skills/tree/master/skills/session-story) | `npx skills add heygen-com/hyperframes-community-skills --skill session-story` | HyperFrames |
| **Generative Film Skill** | [@BuildFastWithAI](https://x.com/BuildFastWithAI) | [buildfastwithai/buildfast-skills](https://github.com/buildfastwithai/buildfast-skills/tree/main/generative-film-skill) | `npx skills@latest add https://github.com/buildfastwithai/buildfast-skills` | Three.js / MP4 |

*See [`SKILLS.md`](SKILLS.md) for full descriptions, breakdown, and source links.*

---

## 📂 Repository Structure

```
prompt-motion-archive/
├── archive/
│   └── index.html          # Standalone web app viewer with video player, search & filters
├── data/
│   ├── prompts.json        # Complete structured dataset (all 235 items)
│   └── skills.json         # Dedicated skills-only dataset
├── videos/                 # 235 downloaded MP4 video files (2.54 GB)
│   ├── steventey-0d20e4.mp4
│   ├── emollick-8661a8.mp4
│   └── ...
├── blog/                   # Archived prompt engineering essays & guides
│   ├── ai-explainer-video-prompts.md
│   ├── ai-launch-video-prompts.md
│   ├── ai-motion-graphics-prompts.md
│   ├── make-ai-motion-graphics-look-less-ai.md
│   └── remotion-vs-hyperframes.md
├── SKILLS.md               # Directory of all Claude Code motion skills
├── PROMPTS.md              # Full table index of all 235 prompts
├── scraper.py              # Automated archiver script
└── README.md               # This documentation
```

---

## 🖥️ Interactive Web Archive Viewer

A dark-mode web viewer is included at [`archive/index.html`](archive/index.html).

### Features:
- **Instant Search:** Search across all 235 titles, authors, prompt text, tags, and install commands.
- **Filter Tabs:** Quickly toggle between *All Items*, *Skills Only*, *Templates*, or *Prompts*.
- **Tag Cloud:** Filter by tags like *Product UI*, *Charts*, *Characters*, *Code*, *3D*, *Diagrams*, etc.
- **Local & CDN Dual-Playback:** Automatically plays local `videos/<id>.mp4` files. If videos are not cloned, it falls back to streaming from the CDN.
- **1-Click Copy:** Instant clipboard copy for prompt text and skill install commands.
- **Direct Links:** Quick access to original X/Twitter posts, GitHub repos, and Prompt Motion pages.

To open the viewer, double-click [`archive/index.html`](archive/index.html) or run a local server:
```bash
python -m http.server 8000
# Open http://localhost:8000/archive/
```

---

## 🚀 How to Push this Archive to GitHub

The entire repository with all 235 MP4 videos is **2.54 GB**. Every individual video is between 1.5 MB and 36 MB (well below GitHub's 100 MB per-file hard limit).

### Option 1: Using Git LFS (Recommended for GitHub)

Git LFS (Large File Storage) keeps your repository history lightweight and fast:

```bash
# 1. Initialize git and install Git LFS
git init
git lfs install

# 2. Track MP4 video files with Git LFS
git lfs track "videos/*.mp4"
git add .gitattributes

# 3. Add all files and commit
git add .
git commit -m "feat: complete archive of prompt-motion.com (235 prompts, skills, and videos)"

# 4. Link your GitHub remote and push
git remote add origin https://github.com/<your-username>/prompt-motion-archive.git
git branch -M main
git push -u origin main
```

### Option 2: Code & Prompts Only + Release Assets

If you prefer keeping your main git repository under 5 MB:

```bash
# 1. Ignore the videos directory in git
echo "videos/" >> .gitignore

# 2. Commit and push code, archive viewer, data, and docs
git init
git add .
git commit -m "feat: prompt-motion prompts, skills, and web viewer"
git remote add origin https://github.com/<your-username>/prompt-motion-archive.git
git push -u origin main

# 3. Zip the videos and upload to a GitHub Release:
# The web viewer (archive/index.html) will still stream videos seamlessly from CDN!
```

---

## 📄 Data Schema (`data/prompts.json`)

Each entry in `prompts.json` contains:

```json
{
  "slug": "/steventey-0d20e4",
  "id": "steventey-0d20e4",
  "pageUrl": "https://prompt-motion.com/steventey-0d20e4",
  "title": "Dub promo video",
  "contentType": "Prompt",
  "author": "@steventey",
  "sourcePostUrl": "https://x.com/steventey/status/2103625902211088880",
  "tags": ["Product UI", "Charts"],
  "metadata": {
    "Model": "Opus 5.5",
    "Effort": "High",
    "Iterations": "One-shot",
    "Posted": "Sep 25, 2026"
  },
  "videoUrl": "https://media.prompt-motion.com/steventey-claude-opus-5-5-feels/video.1d1039db.mp4",
  "videoFile": "videos/steventey-0d20e4.mp4",
  "promptText": "make a dynamic 15-second motion graphics video...",
  "skillData": null
}
```

For entries with `contentType: "Skill"`:
```json
{
  "skillData": {
    "description": "An agent skill that has your coding agent concept, brand, score and render a short cinematic launch film or motion piece from code.",
    "installCommands": [
      "npx skills add Leonxlnx/cinetic"
    ],
    "githubRepos": [
      "https://github.com/Leonxlnx/cinetic"
    ]
  }
}
```

---

## ⚖️ Attribution & Disclaimer

Videos, prompts, and skills belong to their original creators, linked on each entry. Curated originally by [@p4nthera_](https://x.com/p4nthera_). This archive is created for educational and personal reference purposes.
