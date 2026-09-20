import json
import time

from google import genai
from google.genai.errors import ServerError

from src.core.config import GEMINI_API_KEY
from src.services.prompts import STORY_PIPELINE_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


def process_story(story: str) -> dict | None:
    """
    Run the full story pipeline (analysis + structure + script)
    in a SINGLE Gemini API call to minimize quota usage.

    Retries automatically on transient server errors (e.g. 503
    "model overloaded"), since these are temporary and not caused
    by our code.

    Returns a dict shaped like:
    {
        "analysis": {...},
        "structure": {...},
        "final_script": "..."
    }
    or None if something went wrong.
    """

    prompt = STORY_PIPELINE_PROMPT.replace("{story}", story)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            result = json.loads(response.text)

            # Basic sanity check on the shape we expect back.
            required_keys = {"analysis", "structure", "final_script"}
            if not required_keys.issubset(result.keys()):
                print("[ERROR] Gemini response missing expected keys.")
                return None

            return result

        except json.JSONDecodeError:
            print("[ERROR] Gemini returned invalid JSON.")
            return None

        except ServerError as e:
            print(f"[WARN] Gemini server error (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print("[ERROR] Gemini is still unavailable after retries.")
                return None

        except Exception as e:
            print(f"[ERROR] Failed to process the story: {e}")
            return None