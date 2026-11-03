# Architecture
RSS feeds → topic scoring → optional local GGUF LLM / fallback script → Pexels or Wikimedia Commons still images → Pillow motion-card scenes → Piper narration (optional) → FFmpeg MP4 → Actions artifacts → platform publisher.

Actions runners are ephemeral. JSON in `data/` is committed as durable state. Artifacts expire. No VPS or Docker is used. Optional LLM runs locally on runner CPU; it is not a fact checker. Piper voice model licenses must be checked individually. Pexels is a free API service, not open-source. Commons image licenses are item-specific.

Current implementation limitations: no automated per-video public media upload; no speech-aligned subtitles; no automatic platform Insights queries; no automatic claim verification. See ROADMAP.
