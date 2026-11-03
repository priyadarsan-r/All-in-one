# Before unattended publishing
1. Add per-video upload to public media repository or reliable object storage; store distinct URL per script ID.
2. Test Meta can fetch each URL. Do not assume GitHub Release assets work as a CDN.
3. Validate Meta endpoints/scopes against current app version and account.
4. Implement YouTube Analytics and Meta Insights metrics.
5. Add Whisper/faster-whisper word-level subtitles, audio mixing and QC for black frames, silence, clipping and duration.
6. Add stronger factual corroboration, duplicate detection, category balancing and human approval UI.
7. Pin GitHub Actions to full commit SHAs before production.
