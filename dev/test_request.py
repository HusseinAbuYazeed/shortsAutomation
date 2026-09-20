import requests

story = """
To watch the sun’s magnificent beauty
Is to watch it from afar

Staring at the sun, allowing its warmth to embrace you.
Gently
Kindly
Lovingly

Allowing it’s light to wrap around you at each glance
Like a gaze where all you can do is stare back

But there is something you must know about the sun…
You can only watch
You cannot embrace the sun back without burning yourself raw.

(This is a short poetry about unrequited love from my experience)

"""

# Change this to "gemini" to test the Gemini TTS provider instead.
tts_provider = "gemini"

response = requests.post(
    "http://127.0.0.1:8000/generate",
    json={"story_text": story, "tts_provider": tts_provider},
)

print("Status code:", response.status_code)
print(response.json())