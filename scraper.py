"""
Prompt Motion Full Archiver
============================
Scrapes all motion design prompts, skills, templates, blog posts, and videos
from https://prompt-motion.com/ and creates a complete, offline-capable archive
ready for GitHub.
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://prompt-motion.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

ROOT_DIR = Path(__file__).parent.resolve()
DATA_DIR = ROOT_DIR / "data"
VIDEOS_DIR = ROOT_DIR / "videos"
BLOG_DIR = ROOT_DIR / "blog"
ARCHIVE_DIR = ROOT_DIR / "archive"

for d in [DATA_DIR, VIDEOS_DIR, BLOG_DIR, ARCHIVE_DIR]:
    d.mkdir(parents=True, exist_ok=True)


async def fetch_html(client: httpx.AsyncClient, url: str) -> str | None:
    for attempt in range(3):
        try:
            r = await client.get(url, headers=HEADERS, timeout=25.0)
            if r.status_code == 200:
                return r.text
            elif r.status_code == 404:
                return None
            await asyncio.sleep(1.0)
        except Exception as e:
            if attempt == 2:
                print(f"  [Error] {url}: {e}")
            await asyncio.sleep(1.5)
    return None


async def get_homepage_items(client: httpx.AsyncClient) -> list[str]:
    print("[1/5] Fetching homepage links...")
    html = await fetch_html(client, BASE_URL)
    if not html:
        raise RuntimeError("Failed to fetch homepage")
    
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") and "-" in href:
            parts = href.split("-")
            if len(parts[-1]) == 6:
                links.append(href)
    unique_links = list(dict.fromkeys(links))
    print(f"  Found {len(unique_links)} unique prompt/skill pages on homepage.")
    return unique_links


def parse_prompt_page(slug: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    url = f"{BASE_URL}{slug}"
    slug_id = slug.strip("/").replace("/", "_")

    # Title
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else slug_id

    # Video
    video_el = soup.find("video")
    video_url = ""
    if video_el:
        if video_el.has_attr("src"):
            video_url = video_el["src"]
        elif video_el.find("source") and video_el.find("source").has_attr("src"):
            video_url = video_el.find("source")["src"]

    # Local video filename
    video_filename = f"{slug_id}.mp4" if video_url else ""

    # Tags
    tags = [a.get_text(strip=True) for a in soup.find_all("a", href=lambda h: h and "/tags/" in h)]
    tags = list(dict.fromkeys(tags))

    # Metadata dt/dd
    metadata = {}
    for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd")):
        metadata[dt.get_text(strip=True)] = dd.get_text(strip=True)

    # Section type: 'Prompt' or 'Skill'
    h2 = soup.find("h2")
    section_type = h2.get_text(strip=True) if h2 else "Prompt"

    # Author
    author = ""
    author_post_url = ""
    author_link = soup.find("a", href=lambda h: h and "x.com/" in h and "/status/" in h)
    if author_link:
        author_post_url = author_link["href"]
        m = re.search(r"x\.com/([^/]+)/status", author_post_url)
        if m:
            author = f"@{m.group(1)}"
    
    if not author:
        # Check links
        for a in soup.find_all("a", href=lambda h: h and "x.com/" in h):
            txt = a.get_text(strip=True)
            if txt.startswith("@") and txt != "@p4nthera_":
                author = txt
                break

    prompt_text = ""
    skill_data = None

    if section_type.lower() == "skill":
        # It's a skill
        section = h2.find_parent("section") if h2 else None
        skill_desc = ""
        install_commands = []
        github_repos = []

        if section:
            p_desc = section.find("p")
            if p_desc:
                skill_desc = p_desc.get_text(strip=True)
            
            for code in section.find_all("code"):
                c_txt = code.get_text(strip=True)
                if c_txt:
                    install_commands.append(c_txt)
            
            for a in section.find_all("a", href=True):
                if "github.com" in a["href"]:
                    github_repos.append(a["href"])

        # Also search whole page for github links if not found
        if not github_repos:
            for a in soup.find_all("a", href=True):
                if "github.com" in a["href"]:
                    github_repos.append(a["href"])
        github_repos = list(dict.fromkeys(github_repos))

        skill_data = {
            "description": skill_desc,
            "installCommands": install_commands,
            "githubRepos": github_repos,
        }
        # Also fill prompt_text with skill description & install commands for unified search
        prompt_text = f"{skill_desc}\n\nInstall:\n" + "\n".join(install_commands) if install_commands else skill_desc

    else:
        # Regular prompt
        section = h2.find_parent("section") if h2 else None
        if section:
            # find inner div containing prompt
            main_div = section.find("div", recursive=False)
            if main_div:
                div_children = [c for c in main_div.children if c.name == "div"]
                if len(div_children) >= 2:
                    prompt_text = div_children[1].get_text("\n", strip=True)
                elif len(div_children) == 1:
                    prompt_text = div_children[0].get_text("\n", strip=True)
            
            if not prompt_text:
                # Fallback: extract text between copy and attribution
                sec_text = section.get_text("\n", strip=True)
                lines = sec_text.splitlines()
                # filter out 'Prompt', 'Customize', 'Copy', 'Copied'
                filtered = [l for l in lines if l not in ("Prompt", "Customize", "Copy", "Copied") and not l.startswith("This prompt was taken")]
                prompt_text = "\n".join(filtered).strip()

    return {
        "slug": slug,
        "id": slug_id,
        "pageUrl": url,
        "title": title,
        "contentType": "Skill" if section_type.lower() == "skill" else "Prompt",
        "author": author,
        "sourcePostUrl": author_post_url,
        "tags": tags,
        "metadata": metadata,
        "videoUrl": video_url,
        "videoFile": f"videos/{video_filename}" if video_filename else "",
        "promptText": prompt_text,
        "skillData": skill_data,
    }


def parse_template_page(path: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    url = f"{BASE_URL}{path}"
    slug_id = path.strip("/").replace("/", "_")

    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else slug_id

    video_el = soup.find("video")
    video_url = ""
    if video_el:
        if video_el.has_attr("src"):
            video_url = video_el["src"]
        elif video_el.find("source") and video_el.find("source").has_attr("src"):
            video_url = video_el.find("source")["src"]

    video_filename = f"{slug_id}.mp4" if video_url else ""

    sections = {}
    for sec in soup.find_all("section"):
        h2 = sec.find("h2")
        if h2:
            h2_title = h2.get_text(strip=True)
            # clone section and remove h2
            sec_copy = BeautifulSoup(str(sec), "html.parser")
            h2_c = sec_copy.find("h2")
            if h2_c:
                h2_c.decompose()
            sections[h2_title] = sec_copy.get_text("\n", strip=True)

    improved_prompt = sections.get("Improved prompt", "")
    # Clean copied/copy artifacts
    improved_prompt = re.sub(r"^(?:Copied|Copy)\s*", "", improved_prompt).strip()

    return {
        "slug": path,
        "id": slug_id,
        "pageUrl": url,
        "title": title,
        "contentType": "Template",
        "author": "@p4nthera_",
        "sourcePostUrl": "",
        "tags": ["Template", "Opus 5.5"],
        "metadata": {"Model": "Opus 5.5", "Type": "Template"},
        "videoUrl": video_url,
        "videoFile": f"videos/{video_filename}" if video_filename else "",
        "promptText": improved_prompt,
        "templateSections": sections,
        "skillData": None,
    }


async def scrape_all_entries():
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=20)
    async with httpx.AsyncClient(limits=limits) as client:
        # Step 1: get all links
        slugs = await get_homepage_items(client)
        
        # Add template links
        templates_to_fetch = ["/templates/realtime", "/templates/showreel"]
        
        print(f"\n[2/5] Scraping {len(slugs)} prompt pages and {len(templates_to_fetch)} templates...")
        sem = asyncio.Semaphore(10)
        all_entries = []
        errors = []

        async def fetch_and_parse(slug: str, is_template: bool = False):
            async with sem:
                html = await fetch_html(client, f"{BASE_URL}{slug}")
                if not html:
                    errors.append(slug)
                    return None
                try:
                    if is_template:
                        return parse_template_page(slug, html)
                    else:
                        return parse_prompt_page(slug, html)
                except Exception as e:
                    print(f"  [Parse Error] {slug}: {e}")
                    errors.append(slug)
                    return None

        # Gather prompts
        prompt_tasks = [fetch_and_parse(s, False) for s in slugs]
        template_tasks = [fetch_and_parse(t, True) for t in templates_to_fetch]
        
        results = await asyncio.gather(*prompt_tasks, *template_tasks)
        all_entries = [r for r in results if r is not None]
        
        skills_count = sum(1 for e in all_entries if e["contentType"] == "Skill")
        prompts_count = sum(1 for e in all_entries if e["contentType"] == "Prompt")
        templates_count = sum(1 for e in all_entries if e["contentType"] == "Template")

        print(f"  Successfully parsed {len(all_entries)} entries:")
        print(f"    - Prompts: {prompts_count}")
        print(f"    - Skills: {skills_count}")
        print(f"    - Templates: {templates_count}")
        if errors:
            print(f"    - Errors: {len(errors)}")

        # Step 3: Archive blog posts
        print("\n[3/5] Archiving blog posts...")
        blog_posts = [
            "/blog/ai-explainer-video-prompts",
            "/blog/ai-launch-video-prompts",
            "/blog/ai-motion-graphics-prompts",
            "/blog/make-ai-motion-graphics-look-less-ai",
            "/blog/remotion-vs-hyperframes",
        ]
        blog_data = []
        for bp in blog_posts:
            b_html = await fetch_html(client, f"{BASE_URL}{bp}")
            if b_html:
                b_soup = BeautifulSoup(b_html, "html.parser")
                h1 = b_soup.find("h1")
                b_title = h1.get_text(strip=True) if h1 else bp
                main = b_soup.find("main") or b_soup.find("article")
                b_text = main.get_text("\n\n", strip=True) if main else b_soup.get_text("\n\n", strip=True)
                bp_slug = bp.split("/")[-1]
                md_path = BLOG_DIR / f"{bp_slug}.md"
                md_content = f"# {b_title}\n\nSource: {BASE_URL}{bp}\n\n---\n\n{b_text}\n"
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                blog_data.append({"title": b_title, "slug": bp_slug, "url": f"{BASE_URL}{bp}"})
                print(f"  Saved blog post: {b_title[:50]}")

        # Save JSON files
        print("\n[4/5] Saving data JSON and Markdown documents...")
        all_data_file = DATA_DIR / "prompts.json"
        with open(all_data_file, "w", encoding="utf-8") as f:
            json.dump(all_entries, f, indent=2, ensure_ascii=False)
        print(f"  Saved {all_data_file}")

        # Skills-only dataset
        skills_entries = [e for e in all_entries if e["contentType"] == "Skill"]
        skills_data_file = DATA_DIR / "skills.json"
        with open(skills_data_file, "w", encoding="utf-8") as f:
            json.dump(skills_entries, f, indent=2, ensure_ascii=False)
        print(f"  Saved {skills_data_file} ({len(skills_entries)} skills)")

        # Generate markdown tables
        generate_markdown_indexes(all_entries, skills_entries)

        # Step 5: Download Videos
        print(f"\n[5/5] Downloading MP4 videos to {VIDEOS_DIR}...")
        await download_all_videos(client, all_entries)

        # Generate browsable HTML archive
        generate_html_viewer(all_entries)

        print("\n" + "=" * 60)
        print("ARCHIVE GENERATION COMPLETE!")
        print("=" * 60)


async def download_all_videos(client: httpx.AsyncClient, entries: list[dict]):
    download_list = [e for e in entries if e.get("videoUrl")]
    print(f"  Total videos to download: {len(download_list)}")

    sem = asyncio.Semaphore(6)
    completed = 0
    skipped = 0
    failed = 0
    total_bytes = 0

    async def download_one(entry: dict):
        nonlocal completed, skipped, failed, total_bytes
        url = entry["videoUrl"]
        slug_id = entry["id"]
        target = VIDEOS_DIR / f"{slug_id}.mp4"

        # Resume / skip if already downloaded and > 50KB
        if target.exists() and target.stat().st_size > 50000:
            skipped += 1
            total_bytes += target.stat().st_size
            return

        async with sem:
            for attempt in range(3):
                try:
                    async with client.stream("GET", url, headers=HEADERS, timeout=45.0) as resp:
                        if resp.status_code == 200:
                            with open(target, "wb") as f:
                                async for chunk in resp.aiter_bytes(chunk_size=65536):
                                    f.write(chunk)
                            size = target.stat().st_size
                            completed += 1
                            total_bytes += size
                            cur = completed + skipped
                            pct = cur / len(download_list) * 100
                            mb = size / (1024 * 1024)
                            tot_mb = total_bytes / (1024 * 1024)
                            if cur % 10 == 0 or cur == len(download_list):
                                print(f"  [{cur}/{len(download_list)}] ({pct:.0f}%) Downloaded {slug_id}.mp4 ({mb:.1f}MB) | Total: {tot_mb:.1f}MB")
                            return
                except Exception as e:
                    if attempt == 2:
                        print(f"  [Failed] {slug_id}: {e}")
                        failed += 1
                    await asyncio.sleep(1.0)

    tasks = [download_one(e) for e in download_list]
    await asyncio.gather(*tasks)

    tot_gb = total_bytes / (1024 * 1024 * 1024)
    print(f"\n  Download Summary:")
    print(f"    - Newly downloaded: {completed}")
    print(f"    - Skipped (already existed): {skipped}")
    print(f"    - Failed: {failed}")
    print(f"    - Total video archive size: {tot_gb:.2f} GB")


def generate_markdown_indexes(all_entries: list[dict], skills_entries: list[dict]):
    # 1. SKILLS.md
    skills_md = ["# Motion Design Skills Archive", "", "A curated list of Claude Code skills for motion graphics and video creation found on Prompt Motion.", ""]
    skills_md.append("| Skill / Film | Author | GitHub Repo | Install Command | Stack | Video |")
    skills_md.append("|---|---|---|---|---|---|")

    for s in skills_entries:
        title = s.get("title", "")
        author = s.get("author", "")
        sk = s.get("skillData") or {}
        repos = sk.get("githubRepos", [])
        cmds = sk.get("installCommands", [])
        stack = s.get("metadata", {}).get("Stack", s.get("metadata", {}).get("Model", "Opus 5.5"))
        vid_file = s.get("videoFile", "")
        vid_url = s.get("videoUrl", "")

        repo_link = f"[{repos[0].split('/')[-1]}]({repos[0]})" if repos else "N/A"
        cmd_text = f"`{cmds[0]}`" if cmds else "N/A"
        vid_link = f"[Watch Video]({vid_url})" if vid_url else "N/A"

        skills_md.append(f"| **{title}** | {author} | {repo_link} | {cmd_text} | {stack} | {vid_link} |")

    skills_md.append("\n## Detailed Skill Profiles\n")
    for s in skills_entries:
        sk = s.get("skillData") or {}
        skills_md.append(f"### {s['title']}")
        skills_md.append(f"- **Author:** {s.get('author')}")
        skills_md.append(f"- **Source Page:** [{s.get('pageUrl')}]({s.get('pageUrl')})")
        if s.get("sourcePostUrl"):
            skills_md.append(f"- **Original Post:** [{s.get('sourcePostUrl')}]({s.get('sourcePostUrl')})")
        if s.get("videoUrl"):
            skills_md.append(f"- **Video:** [{s.get('videoFile')}]({s.get('videoUrl')})")
        
        repos = sk.get("githubRepos", [])
        if repos:
            skills_md.append("- **GitHub Repositories:**")
            for r in repos:
                skills_md.append(f"  - [{r}]({r})")
        
        cmds = sk.get("installCommands", [])
        if cmds:
            skills_md.append("- **Install Command:**")
            for c in cmds:
                skills_md.append(f"  ```bash\n  {c}\n  ```")

        desc = sk.get("description", "")
        if desc:
            skills_md.append(f"\n**Description:**\n> {desc}\n")
        skills_md.append("---\n")

    with open(ROOT_DIR / "SKILLS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(skills_md))
    print(f"  Saved {ROOT_DIR / 'SKILLS.md'}")

    # 2. PROMPTS.md
    prompts_md = ["# Motion Design Prompts Archive", "", f"Complete catalog of all {len(all_entries)} motion design prompts.", ""]
    prompts_md.append("| # | Title | Type | Author | Tags | Model / Effort | Prompt Preview | Video |")
    prompts_md.append("|---|---|---|---|---|---|---|---|")

    for i, e in enumerate(all_entries, 1):
        title = e.get("title", "").replace("|", "-")
        c_type = e.get("contentType", "Prompt")
        author = e.get("author", "")
        tags = ", ".join(e.get("tags", [])[:2])
        meta = e.get("metadata", {})
        meta_str = f"{meta.get('Model', '')} / {meta.get('Effort', meta.get('Iterations', ''))}".strip(" /")
        
        pt = e.get("promptText", "").replace("\n", " ")
        if len(pt) > 80:
            pt = pt[:77] + "..."
        pt = pt.replace("|", "-")

        vid_url = e.get("videoUrl", "")
        vid_link = f"[Video]({vid_url})" if vid_url else "-"

        prompts_md.append(f"| {i} | [{title}]({e['pageUrl']}) | {c_type} | {author} | {tags} | {meta_str} | {pt} | {vid_link} |")

    with open(ROOT_DIR / "PROMPTS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(prompts_md))
    print(f"  Saved {ROOT_DIR / 'PROMPTS.md'}")


def generate_html_viewer(entries: list[dict]):
    html_path = ARCHIVE_DIR / "index.html"
    json_data = json.dumps(entries, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Motion Design Prompt & Skill Archive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #09090b;
    --surface: #121215;
    --surface-hover: #18181c;
    --surface-card: #141418;
    --border: #222228;
    --border-hover: #383842;
    --text: #f4f4f5;
    --text-dim: #a1a1aa;
    --text-muted: #71717a;
    --accent: #6366f1;
    --accent-light: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.15);
    --tag-bg: #1e1b4b;
    --tag-text: #c7d2fe;
    --skill-badge: #059669;
    --skill-bg: #064e3b;
    --green: #10b981;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
  }}

  /* Top Bar */
  .header {{
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(9, 9, 11, 0.88);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--border);
    padding: 14px 28px;
  }}
  .header-inner {{
    max-width: 1600px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo-icon {{
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 15px;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
  }}
  .brand h1 {{
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.02em;
  }}
  .stats-pill {{
    display: flex;
    gap: 14px;
    font-size: 0.8rem;
    color: var(--text-muted);
    background: var(--surface);
    padding: 6px 14px;
    border-radius: 99px;
    border: 1px solid var(--border);
  }}
  .stats-pill strong {{ color: var(--text); font-weight: 600; }}

  .search-box {{
    flex: 1;
    max-width: 460px;
    position: relative;
  }}
  .search-box input {{
    width: 100%;
    padding: 9px 16px 9px 38px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-size: 0.85rem;
    font-family: inherit;
    outline: none;
    transition: all 0.2s;
  }}
  .search-box input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }}
  .search-icon {{
    position: absolute;
    left: 13px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
    font-size: 14px;
  }}

  /* Filter Tabs */
  .tabs-bar {{
    background: #0d0d10;
    border-bottom: 1px solid var(--border);
    padding: 10px 28px;
  }}
  .tabs-inner {{
    max-width: 1600px;
    margin: 0 auto;
    display: flex;
    gap: 8px;
    align-items: center;
    overflow-x: auto;
  }}
  .tab-btn {{
    padding: 6px 14px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text-dim);
    font-size: 0.8rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    white-space: nowrap;
  }}
  .tab-btn:hover {{
    color: var(--text);
    border-color: var(--border-hover);
    background: var(--surface);
  }}
  .tab-btn.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: white;
    font-weight: 600;
  }}
  .tab-badge {{
    margin-left: 6px;
    padding: 1px 6px;
    border-radius: 99px;
    background: rgba(255,255,255,0.15);
    font-size: 0.7rem;
  }}

  /* Layout */
  .layout {{
    max-width: 1600px;
    margin: 0 auto;
    display: flex;
    gap: 24px;
    padding: 24px 28px;
  }}
  .sidebar {{
    width: 220px;
    flex-shrink: 0;
  }}
  .sidebar h3 {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 12px;
  }}
  .tag-cloud {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .tag-chip {{
    padding: 4px 10px;
    border-radius: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .tag-chip:hover {{
    border-color: var(--accent);
    color: var(--text);
  }}
  .tag-chip.active {{
    background: var(--tag-bg);
    border-color: var(--accent-light);
    color: var(--tag-text);
    font-weight: 600;
  }}

  .content {{
    flex: 1;
    min-width: 0;
  }}
  .results-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    font-size: 0.85rem;
    color: var(--text-muted);
  }}

  /* Grid */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    gap: 20px;
  }}

  .card {{
    background: var(--surface-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    position: relative;
  }}
  .card:hover {{
    border-color: var(--border-hover);
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
  }}

  .card-media {{
    position: relative;
    aspect-ratio: 16/9;
    background: #000;
    overflow: hidden;
  }}
  .card-media video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .type-badge {{
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    backdrop-filter: blur(8px);
    z-index: 2;
  }}
  .badge-skill {{
    background: rgba(16, 185, 129, 0.85);
    color: #fff;
  }}
  .badge-prompt {{
    background: rgba(99, 102, 241, 0.85);
    color: #fff;
  }}
  .badge-template {{
    background: rgba(245, 158, 11, 0.85);
    color: #fff;
  }}

  .card-body {{
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    flex: 1;
  }}
  .card-title {{
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
    line-height: 1.35;
  }}
  .card-author {{
    font-size: 0.8rem;
    color: var(--accent-light);
    margin-bottom: 10px;
    font-weight: 500;
  }}
  .card-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 12px;
  }}
  .card-tag {{
    font-size: 0.68rem;
    padding: 2px 7px;
    border-radius: 4px;
    background: rgba(255,255,255,0.05);
    color: var(--text-dim);
  }}
  .prompt-preview {{
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin-bottom: 14px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    flex: 1;
  }}
  .card-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 10px;
    border-top: 1px solid var(--border);
    font-size: 0.72rem;
    color: var(--text-muted);
  }}

  /* Modal */
  .modal-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    z-index: 200;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .modal-overlay.open {{ display: flex; }}
  .modal-content {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    max-width: 860px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 25px 60px rgba(0,0,0,0.8);
  }}
  .modal-video-box {{
    aspect-ratio: 16/9;
    background: #000;
    border-bottom: 1px solid var(--border);
  }}
  .modal-video-box video {{
    width: 100%;
    height: 100%;
    object-fit: contain;
  }}
  .modal-body {{
    padding: 24px 28px;
  }}
  .modal-header {{
    margin-bottom: 18px;
  }}
  .modal-title {{
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
  }}
  .modal-meta {{
    display: flex;
    gap: 16px;
    font-size: 0.85rem;
    color: var(--text-muted);
    flex-wrap: wrap;
    align-items: center;
  }}
  .modal-meta a {{
    color: var(--accent-light);
    text-decoration: none;
  }}
  .modal-meta a:hover {{ text-decoration: underline; }}

  .skill-install-box {{
    background: #064e3b;
    border: 1px solid #059669;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 16px 0;
  }}
  .skill-install-box h4 {{
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #6ee7b7;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
  }}
  .skill-code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #ecfdf5;
    background: rgba(0,0,0,0.3);
    padding: 10px 14px;
    border-radius: 6px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }}
  .repo-btn {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 10px;
    color: #6ee7b7;
    font-size: 0.8rem;
    font-weight: 600;
    text-decoration: none;
  }}
  .repo-btn:hover {{ text-decoration: underline; }}

  .prompt-display {{
    margin: 20px 0;
  }}
  .prompt-display-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }}
  .prompt-display-header span {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
  }}
  .copy-btn {{
    padding: 5px 12px;
    border-radius: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    font-size: 0.78rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .copy-btn:hover {{
    border-color: var(--accent);
    background: var(--surface-hover);
  }}
  .copy-btn.copied {{
    background: #064e3b;
    border-color: #059669;
    color: #6ee7b7;
  }}

  .prompt-text-content {{
    background: #09090b;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--text-dim);
    max-height: 380px;
    overflow-y: auto;
  }}

  .modal-actions {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
  }}
  .action-btn {{
    padding: 8px 16px;
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}
  .action-btn:hover {{
    border-color: var(--accent);
    color: var(--accent-light);
  }}
  .close-btn {{
    position: absolute;
    top: 14px;
    right: 14px;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10;
    transition: all 0.15s;
  }}
  .close-btn:hover {{
    background: rgba(255,255,255,0.2);
  }}

  @media (max-width: 900px) {{
    .sidebar {{ display: none; }}
    .header-inner {{ flex-direction: column; align-items: stretch; }}
    .search-box {{ max-width: none; }}
    .cards-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <div class="brand">
      <div class="logo-icon">▶</div>
      <div>
        <h1>Motion Design Prompts & Skills</h1>
      </div>
    </div>

    <div class="stats-pill">
      <span><strong id="statTotal">0</strong> Total</span>
      <span><strong id="statSkills" style="color:#10b981;">0</strong> Skills</span>
      <span><strong id="statPrompts">0</strong> Prompts</span>
    </div>

    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="Search prompts, skills, authors, tools, stack...">
    </div>
  </div>
</div>

<div class="tabs-bar">
  <div class="tabs-inner">
    <button class="tab-btn active" data-tab="all">All Items <span class="tab-badge" id="tabAllCount">0</span></button>
    <button class="tab-btn" data-tab="Skill" style="border-color:#059669;">⚡ Skills Only <span class="tab-badge" id="tabSkillCount">0</span></button>
    <button class="tab-btn" data-tab="Template">📐 Templates <span class="tab-badge" id="tabTemplateCount">0</span></button>
    <button class="tab-btn" data-tab="Prompt">💬 Prompts <span class="tab-badge" id="tabPromptCount">0</span></button>
  </div>
</div>

<div class="layout">
  <aside class="sidebar">
    <h3>Filter by Tag</h3>
    <div class="tag-cloud" id="tagCloud"></div>
  </aside>

  <main class="content">
    <div class="results-meta">
      <span id="resultsCount">Showing all items</span>
    </div>

    <div class="cards-grid" id="cardsGrid"></div>
  </main>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal-content">
    <button class="close-btn" onclick="closeModal()">✕</button>
    <div class="modal-video-box" id="modalVideo"></div>
    <div class="modal-body">
      <div class="modal-header">
        <h2 class="modal-title" id="modalTitle"></h2>
        <div class="modal-meta" id="modalMeta"></div>
      </div>
      <div id="modalSkillContent"></div>
      <div class="prompt-display">
        <div class="prompt-display-header">
          <span id="promptLabel">Prompt</span>
          <button class="copy-btn" id="copyPromptBtn">📋 Copy Prompt</button>
        </div>
        <div class="prompt-text-content" id="modalPromptText"></div>
      </div>
      <div class="modal-actions" id="modalActions"></div>
    </div>
  </div>
</div>

<script>
const ITEMS = {json_data};
let currentTab = 'all';
let selectedTag = null;
let searchQuery = '';

function init() {{
  const skillsCount = ITEMS.filter(i => i.contentType === 'Skill').length;
  const promptsCount = ITEMS.filter(i => i.contentType === 'Prompt').length;
  const templatesCount = ITEMS.filter(i => i.contentType === 'Template').length;

  document.getElementById('statTotal').textContent = ITEMS.length;
  document.getElementById('statSkills').textContent = skillsCount;
  document.getElementById('statPrompts').textContent = promptsCount;

  document.getElementById('tabAllCount').textContent = ITEMS.length;
  document.getElementById('tabSkillCount').textContent = skillsCount;
  document.getElementById('tabTemplateCount').textContent = templatesCount;
  document.getElementById('tabPromptCount').textContent = promptsCount;

  // Build tag cloud
  const tagsMap = {{}};
  ITEMS.forEach(i => {{
    (i.tags || []).forEach(t => {{
      tagsMap[t] = (tagsMap[t] || 0) + 1;
    }});
  }});

  const tagCloud = document.getElementById('tagCloud');
  Object.keys(tagsMap).sort((a,b) => tagsMap[b] - tagsMap[a]).forEach(tag => {{
    const chip = document.createElement('div');
    chip.className = 'tag-chip';
    chip.textContent = `${{tag}} (${{tagsMap[tag]}})`;
    chip.onclick = () => {{
      if (selectedTag === tag) {{
        selectedTag = null;
        chip.classList.remove('active');
      }} else {{
        selectedTag = tag;
        document.querySelectorAll('.tag-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
      }}
      render();
    }};
    tagCloud.appendChild(chip);
  }});

  // Tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.onclick = () => {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTab = btn.dataset.tab;
      render();
    }};
  }});

  // Search
  document.getElementById('searchInput').addEventListener('input', e => {{
    searchQuery = e.target.value.toLowerCase().trim();
    render();
  }});

  // Modal close
  document.getElementById('modalOverlay').onclick = e => {{
    if (e.target.id === 'modalOverlay') closeModal();
  }};
  document.addEventListener('keydown', e => {{
    if (e.key === 'Escape') closeModal();
  }});

  render();
}}

function getFiltered() {{
  return ITEMS.filter(item => {{
    if (currentTab !== 'all' && item.contentType !== currentTab) return false;
    if (selectedTag && !(item.tags || []).includes(selectedTag)) return false;
    if (searchQuery) {{
      const text = [
        item.title,
        item.author,
        item.promptText,
        ...(item.tags || []),
        item.skillData?.description,
        ...(item.skillData?.installCommands || []),
        ...(item.skillData?.githubRepos || []),
        item.metadata?.Model,
        item.metadata?.Stack
      ].filter(Boolean).join(' ').toLowerCase();
      if (!text.includes(searchQuery)) return false;
    }}
    return true;
  }});
}}

function render() {{
  const filtered = getFiltered();
  const grid = document.getElementById('cardsGrid');
  const countEl = document.getElementById('resultsCount');

  countEl.textContent = `Showing ${{filtered.length}} of ${{ITEMS.length}} entries`;

  grid.innerHTML = filtered.map((item, idx) => {{
    const globalIdx = ITEMS.indexOf(item);
    const badgeClass = item.contentType === 'Skill' ? 'badge-skill' : (item.contentType === 'Template' ? 'badge-template' : 'badge-prompt');
    const badgeText = item.contentType;
    const localVideo = `../videos/${{item.id}}.mp4`;
    const remoteVideo = item.videoUrl;

    const tagsHtml = (item.tags || []).slice(0, 3).map(t => `<span class="card-tag">${{t}}</span>`).join('');

    return `
      <div class="card" onclick="openModal(${{globalIdx}})">
        <div class="card-media">
          <span class="type-badge ${{badgeClass}}">${{badgeText}}</span>
          ${{item.videoUrl ? `
            <video src="${{localVideo}}" onerror="this.onerror=null;this.src='${{remoteVideo}}'" muted loop preload="metadata"
              onmouseenter="this.play()" onmouseleave="this.pause();this.currentTime=0;"></video>
          ` : ''}}
        </div>
        <div class="card-body">
          <div class="card-title">${{esc(item.title)}}</div>
          <div class="card-author">${{esc(item.author || '')}}</div>
          <div class="card-tags">${{tagsHtml}}</div>
          <div class="prompt-preview">${{esc(item.promptText || item.skillData?.description || '')}}</div>
          <div class="card-footer">
            <span>${{item.metadata?.Model || 'Opus 5.5'}}</span>
            <span>${{item.metadata?.Posted || item.metadata?.Effort || ''}}</span>
          </div>
        </div>
      </div>
    `;
  }}).join('');
}}

function openModal(idx) {{
  const item = ITEMS[idx];
  const overlay = document.getElementById('modalOverlay');

  document.getElementById('modalTitle').textContent = item.title;
  
  // Meta
  const metaParts = [];
  if (item.author) metaParts.push(`<span>By <strong>${{esc(item.author)}}</strong></span>`);
  if (item.metadata?.Model) metaParts.push(`<span>Model: ${{esc(item.metadata.Model)}}</span>`);
  if (item.metadata?.Stack) metaParts.push(`<span>Stack: <strong>${{esc(item.metadata.Stack)}}</strong></span>`);
  if (item.metadata?.Posted) metaParts.push(`<span>Posted: ${{esc(item.metadata.Posted)}}</span>`);
  if (item.sourcePostUrl) metaParts.push(`<a href="${{item.sourcePostUrl}}" target="_blank">Original Post ↗</a>`);
  document.getElementById('modalMeta').innerHTML = metaParts.join(' • ');

  // Video
  const vidBox = document.getElementById('modalVideo');
  if (item.videoUrl) {{
    const local = `../videos/${{item.id}}.mp4`;
    vidBox.innerHTML = `
      <video src="${{local}}" onerror="this.onerror=null;this.src='${{item.videoUrl}}'" controls autoplay muted loop style="width:100%;height:100%;object-fit:contain;"></video>
    `;
  }} else {{
    vidBox.innerHTML = '';
  }}

  // Skill box
  const skillBox = document.getElementById('modalSkillContent');
  if (item.contentType === 'Skill' && item.skillData) {{
    const sk = item.skillData;
    let reposHtml = '';
    if (sk.githubRepos && sk.githubRepos.length > 0) {{
      reposHtml = sk.githubRepos.map(r => `<a href="${{r}}" target="_blank" class="repo-btn">📂 GitHub: ${{r}} ↗</a>`).join('<br>');
    }}

    let cmdHtml = '';
    if (sk.installCommands && sk.installCommands.length > 0) {{
      cmdHtml = sk.installCommands.map(cmd => `
        <div class="skill-code">
          <code>${{esc(cmd)}}</code>
          <button class="copy-btn" onclick="event.stopPropagation();copyText('${{esc(cmd)}}', this)">Copy</button>
        </div>
      `).join('');
    }}

    skillBox.innerHTML = `
      <div class="skill-install-box">
        <h4>⚡ Claude Code Skill</h4>
        <p style="font-size:0.85rem;color:#d1fae5;margin-bottom:10px;">${{esc(sk.description)}}</p>
        ${{cmdHtml}}
        ${{reposHtml}}
      </div>
    `;
    document.getElementById('promptLabel').textContent = 'Skill Full Text / Prompt';
  }} else {{
    skillBox.innerHTML = '';
    document.getElementById('promptLabel').textContent = 'Prompt';
  }}

  // Prompt Text
  document.getElementById('modalPromptText').textContent = item.promptText || '(No prompt text available)';
  
  // Copy button
  const copyBtn = document.getElementById('copyPromptBtn');
  copyBtn.className = 'copy-btn';
  copyBtn.textContent = '📋 Copy Prompt';
  copyBtn.onclick = () => {{
    copyText(item.promptText, copyBtn);
  }};

  // Actions
  const actions = document.getElementById('modalActions');
  actions.innerHTML = `
    ${{item.videoUrl ? `<a href="${{item.videoUrl}}" target="_blank" class="action-btn">▶ Open CDN Video</a>` : ''}}
    ${{item.pageUrl ? `<a href="${{item.pageUrl}}" target="_blank" class="action-btn">🔗 Prompt Motion Page</a>` : ''}}
  `;

  overlay.classList.add('open');
}}

function closeModal() {{
  const overlay = document.getElementById('modalOverlay');
  overlay.classList.remove('open');
  const vid = overlay.querySelector('video');
  if (vid) vid.pause();
}}

function copyText(text, btn) {{
  navigator.clipboard.writeText(text).then(() => {{
    const old = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.classList.add('copied');
    setTimeout(() => {{
      btn.textContent = old;
      btn.classList.remove('copied');
    }}, 2000);
  }});
}}

function esc(str) {{
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}}

init();
</script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Saved {html_path}")


if __name__ == "__main__":
    asyncio.run(scrape_all_entries())
