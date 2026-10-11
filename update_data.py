import json
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
from scraper import generate_html_viewer, generate_markdown_indexes

DATA_DIR = Path("data")
data = json.load(open(DATA_DIR / "prompts.json", encoding="utf-8"))

# Fetch and enrich buildfastwithai-53234e
for item in data:
    if item["id"] == "buildfastwithai-53234e":
        r = httpx.get(item["pageUrl"], headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        skill_h2 = None
        for h2 in soup.find_all("h2"):
            if h2.get_text(strip=True).lower() == "skill":
                skill_h2 = h2
                break
        if skill_h2:
            sec = skill_h2.find_parent("section")
            desc = sec.find("p").get_text(strip=True) if sec and sec.find("p") else ""
            cmds = [c.get_text(strip=True) for c in sec.find_all("code")]
            repos = [a["href"] for a in sec.find_all("a", href=True) if "github.com" in a["href"]]
            item["contentType"] = "Skill"
            item["skillData"] = {
                "description": desc,
                "installCommands": cmds,
                "githubRepos": repos
            }
            orig_prompt = item.get("promptText", "")
            item["promptText"] = f"{orig_prompt}\n\n[Claude Code Skill]\n{desc}\n\nInstall:\n" + "\n".join(cmds)
            print("Successfully enriched buildfastwithai-53234e!")

# Save prompts.json
with open(DATA_DIR / "prompts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Save skills.json
skills_entries = [e for e in data if e.get("contentType") == "Skill" or e.get("skillData")]
with open(DATA_DIR / "skills.json", "w", encoding="utf-8") as f:
    json.dump(skills_entries, f, indent=2, ensure_ascii=False)

print(f"Total entries: {len(data)}, Total skills: {len(skills_entries)}")

# Regenerate Markdown indexes & HTML viewer
generate_markdown_indexes(data, skills_entries)
generate_html_viewer(data)
print("Updated all markdown tables and HTML viewer!")
