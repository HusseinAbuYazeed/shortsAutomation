# Short Maker

FastAPI backend that turns a raw story into a watchable YouTube Short:
story → AI script → voiceover → (soon: trimmed audio → captions → final video).

## Pipeline (big picture)

```
User story (raw text)
    │
    ▼
[Gemini: Analyzer + Structurer + Writer]   ← ONE Gemini API call
    │  (returns: analysis, structure, final_script)
    ▼
[TTS provider: edge-tts | Gemini TTS]      ← user-selectable
    │
    ▼  voice.wav
[Cut dead parts]   ← NOT BUILT YET (ffmpeg/pydub, no AI quota used)
    │
    ▼  voice_trimmed.wav
[Captions]         ← NOT BUILT YET
    │
    ▼  captions.srt
[Merge with background video]  ← NOT BUILT YET (ffmpeg)
    │
    ▼
final.mp4  →  watchable YouTube Short
```

### Why one Gemini call instead of four?

The original design had separate AI calls for Cleaner, Analyzer, Structurer,
and Writer (4 calls per story = 4x quota). This project merges Analyzer +
Structurer + Writer into a single call (`src/services/prompts.py` →
`STORY_PIPELINE_PROMPT`), and drops the Cleaner entirely (stories are
pasted in manually, so heavy noise-removal isn't needed). Result: ~75%
less Gemini quota used per story.

## Project structure

```
src/
├── core/
│   ├── config.py     # loads GEMINI_API_KEY from .env
│   └── paths.py       # all job-related file paths (single source of truth)
├── models/
│   └── schemas.py      # StoryRequest (story_text, tts_provider)
├── services/
│   ├── prompts.py        # the merged Analyzer+Structurer+Writer prompt
│   ├── story_service.py   # calls Gemini once, returns analysis/structure/script
│   └── tts/
│       ├── base.py           # TTSProvider interface (all providers implement this)
│       ├── edge_provider.py   # free, local (Microsoft edge-tts)
│       ├── gemini_provider.py # Gemini native TTS (uses Gemini quota)
│       └── factory.py          # get_tts_provider("edge" | "gemini")
main.py    # FastAPI app, POST /generate endpoint
dev/       # manual test scripts (git-ignored, not part of the deliverable)
```

## Output structure

Every generated story becomes a "job" with its own folder:

```
outputs/
└── {job_id}/
    ├── script.json          # analysis + structure + final_script
    ├── voice.wav              # raw TTS output
    ├── voice_trimmed.wav       # NOT BUILT YET
    ├── captions.srt             # NOT BUILT YET
    ├── background.mp4            # NOT BUILT YET (user-provided)
    └── final.mp4                  # NOT BUILT YET (the finished short)
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

Run the server:
```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to test, or use the scripts in `dev/`:
```bash
python -m dev.test_request
```

## API

### `POST /generate`

**Request body:**
```json
{
  "story_text": "Your story here...",
  "tts_provider": "edge"
}
```
- `tts_provider`: `"edge"` (free, default) or `"gemini"` (uses Gemini quota)

**Response:**
```json
{
  "job_id": "uuid",
  "analysis": { ... },
  "structure": { ... },
  "final_script": "...",
  "audio_path": "outputs/{job_id}/voice.wav"
}
```

## Status

- [x] FastAPI project structure
- [x] Story pipeline (single Gemini call: analysis + structure + script)
- [x] Retry logic for transient Gemini errors (503)
- [x] TTS providers: edge-tts, Gemini TTS (provider pattern, easy to add more e.g. ElevenLabs)
- [x] Job-based output organization
- [ ] Cut dead air from voiceover (ffmpeg/pydub)
- [ ] Generate captions
- [ ] Merge voice + captions + background video into final short (ffmpeg)
- [ ] Job status tracking (for async/background processing)
- [ ] Deploy online (Render/Railway) for friends to test