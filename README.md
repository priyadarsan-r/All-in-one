# CurioDaily Media Engine

Docker-free, GitHub Actions-based short-video pipeline. Private repo: `curiodaily-media-engine`. Public repo: `curiodaily-media-assets` (release assets only). Target: 3 videos/day.

## Quick start
1. Create the two repositories in GitHub (private engine, public assets).
2. Upload this project to the private repository's `main` branch.
3. Add the secrets in `docs/DEPLOYMENT.md`.
4. Run **Tests**, **Topic discovery**, then **Daily production** manually.
5. Review generated videos and manifests. Publishing workflows are manual and default to dry-run.

Python 3.11/3.12 and FFmpeg required locally. No Docker, VPS or always-on PC.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.cli discover
python -m src.cli generate --count 3
python -m src.cli produce --count 3
```

## Commands
`python -m src.cli discover|generate|produce|publish|analytics|validate`
Use `--help` for command arguments. Optional local GGUF inference uses `llama-cpp-python`; otherwise a deterministic draft generator is used. No paid AI API.

## Important limitations
YouTube uploads directly from the runner. Instagram requires a public HTTPS MP4 URL. The included Meta publisher expects `PUBLIC_VIDEO_URL`; automated per-video asset upload to the public repository is a remaining integration step. GitHub Release assets are a prototype handoff, not a guaranteed CDN. Review `docs/ROADMAP.md` before enabling unattended publishing.

Never publish unverified claims or assets with unclear rights. Default queue status is `review_required`.
