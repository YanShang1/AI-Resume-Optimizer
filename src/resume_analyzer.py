import json
from typing import Any, Dict
from openai import OpenAI

ANALYSIS_SYSTEM_PROMPT = """
You are an expert technical recruiter and resume coach.
Compare a resume against a target job description and return a strict JSON object.
Be practical, specific, and honest. Do not invent experience.
"""

ANALYSIS_USER_TEMPLATE = """
Resume:
{resume_text}

Target Job Description:
{job_description}

Return only valid JSON with this exact schema:

{{
  "overall_match_score": 0,
  "job_requirements_summary": ["requirement 1", "requirement 2"],
  "matched_skills": ["skill 1", "skill 2"],
  "missing_skills": ["skill 1", "skill 2"],
  "weak_resume_bullets": ["weak bullet 1", "weak bullet 2"],
  "improved_resume_bullets": [
    {{
      "original": "original bullet",
      "improved": "improved bullet"
    }}
  ],
  "suggested_summary": "A 3-4 sentence professional summary targeted to this role.",
  "action_plan": ["action 1", "action 2", "action 3"]
}}

Rules:
- overall_match_score must be an integer from 0 to 100.
- Missing skills must be based on the job description.
- Improved bullets should be truthful and based on the resume.
- Use strong action verbs and measurable impact where possible.
- Do not include markdown outside the JSON.
"""

def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end + 1])
        raise

def analyze_resume(resume_text: str, job_description: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    client = OpenAI()
    prompt = ANALYSIS_USER_TEMPLATE.format(
        resume_text=resume_text[:16000],
        job_description=job_description[:12000],
    )
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return _extract_json(response.choices[0].message.content)

def generate_cover_letter(
    resume_text: str,
    job_description: str,
    analysis: Dict[str, Any],
    model: str = "gpt-4o-mini",
) -> str:
    client = OpenAI()
    prompt = f"""
Write a concise, professional cover letter based on the resume, job description, and analysis.

Resume:
{resume_text[:12000]}

Job Description:
{job_description[:10000]}

Analysis:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

Requirements:
- Keep it under 400 words.
- Make it specific to the job description.
- Do not invent experience.
- Use a confident but natural tone.
- Format as a polished cover letter in Markdown.
"""
    response = client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {"role": "system", "content": "You are an expert career coach and professional resume writer."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
