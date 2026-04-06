"""AI analysis — calls the Qwen LLM to identify distortions and generate reframes."""

import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

# Configuration from environment variables.
# Inside Docker, QWEN_API_BASE_URL should be http://qwen-code-api:42005/v1
# From the VM shell, it's http://localhost:42005/v1
QWEN_API_BASE_URL = os.getenv("QWEN_API_BASE_URL", "http://localhost:42005/v1")
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "unused")
QWEN_MODEL = os.getenv("QWEN_MODEL", "coder-model")

client = OpenAI(base_url=QWEN_API_BASE_URL, api_key=QWEN_API_KEY)

SYSTEM_PROMPT = """\
You are a CBT (Cognitive Behavioral Therapy) assistant. Your job is to analyze \
negative thoughts and identify the cognitive distortion present.

Common cognitive distortions include:
- All-or-nothing thinking
- Catastrophizing
- Mind reading
- Overgeneralization
- Personalization
- Should statements
- Emotional reasoning
- Magnification or minimization
- Labeling

You MUST respond with ONLY valid JSON containing exactly two fields:
- "distortion": the name of the cognitive distortion (string)
- "reframe": a short, gentle, compassionate reframe of the thought in 2-3 sentences (string)

Do NOT include any other text, explanations, or markdown. Only JSON.\
"""


def analyze_thought(thought: str) -> dict:
    """
    Send the user's thought to Qwen and return {"distortion": ..., "reframe": ...}.

    If the LLM returns invalid JSON or the call fails, return a safe fallback
    response instead of crashing.
    """
    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": thought},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        raw_text = response.choices[0].message.content.strip()

        # Try to parse the response as JSON.
        result = json.loads(raw_text)

        # Validate that required keys exist.
        if "distortion" not in result or "reframe" not in result:
            raise ValueError("Missing required keys in LLM response")

        return {
            "distortion": str(result["distortion"]),
            "reframe": str(result["reframe"]),
        }

    except Exception as e:
        # Fallback if the LLM call fails or returns bad JSON.
        logger.error(f"LLM call failed: {e}")
        return {
            "distortion": "Unknown",
            "reframe": "It sounds like you're going through a tough time. "
                       "Consider talking to a trusted friend or professional "
                       "about how you're feeling. You're not alone.",
        }


def analyze_thought_raw(prompt: str, is_summary: bool = False) -> str:
    """
    Send a raw prompt to Qwen and return the raw text response.
    Used for the weekly summary (which should be plain text, not JSON).
    """
    try:
        response = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise
