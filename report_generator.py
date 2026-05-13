from typing import Dict, Any

def build_markdown_report(result: Dict[str, Any]) -> str:
    lines = []
    lines.append("# Resume Optimization Report\n")
    lines.append(f"## Overall Match Score\n\n**{result.get('overall_match_score', 0)}/100**\n")

    lines.append("## Job Requirements Summary\n")
    for item in result.get("job_requirements_summary", []):
        lines.append(f"- {item}")

    lines.append("\n## Matched Skills\n")
    for skill in result.get("matched_skills", []):
        lines.append(f"- {skill}")

    lines.append("\n## Missing or Weak Skills\n")
    for skill in result.get("missing_skills", []):
        lines.append(f"- {skill}")

    lines.append("\n## Weak Resume Bullets\n")
    weak = result.get("weak_resume_bullets", [])
    if weak:
        for bullet in weak:
            lines.append(f"- {bullet}")
    else:
        lines.append("- No major weak bullet points identified.")

    lines.append("\n## Improved Resume Bullets\n")
    for item in result.get("improved_resume_bullets", []):
        if isinstance(item, dict):
            lines.append(f"**Original:** {item.get('original', '')}\n")
            lines.append(f"**Improved:** {item.get('improved', '')}\n")
        else:
            lines.append(f"- {item}")

    lines.append("\n## Suggested Professional Summary\n")
    lines.append(result.get("suggested_summary", ""))

    lines.append("\n## Action Plan\n")
    for item in result.get("action_plan", []):
        lines.append(f"- {item}")

    return "\n".join(lines).strip() + "\n"
