# Deployment

## Repositories
Create `curiodaily-media-engine` as **private** and `curiodaily-media-assets` as **public**. Put this project in the private repo. The public repo is reserved for media Release assets; this version does not yet automate release uploads. Do not store credentials in the public repo.

## GitHub Actions
Enable Actions in Settings → Actions → General. Ensure workflow permissions allow contents write for the state-commit jobs. Do not expose secrets to untrusted pull-request workflows.

## Secrets
- `PEXELS_API_KEY` optional image search.
- `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` for YouTube upload scope.
- `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_PAGE_ID`, `META_GRAPH_VERSION` for Meta.
- `PUBLIC_VIDEO_URL` public HTTPS MP4 URL used by Instagram/Facebook API fetch.

## YouTube
Create Google Cloud project, enable YouTube Data API v3, configure OAuth and generate refresh token with `youtube.upload` scope. Store the values as Actions secrets.

## Meta
Use an Instagram professional account and a Meta app with current Reels publishing permissions. For Facebook, configure a Page and required Page permissions. API permissions and review vary by app/account. Verify current Meta documentation and test with dry-run first.

## Public media hosting caveat
YouTube receives direct uploads. Instagram requires a public HTTPS `video_url`. Current implementation uses a single `PUBLIC_VIDEO_URL` secret for manual testing; it is not an automated URL-per-video uploader. Add a GitHub Release upload step with a scoped PAT or use a suitable object-storage/CDN provider, then validate Meta can fetch it. A GitHub Release URL is not guaranteed to behave as a CDN.

## Safe rollout
1. Run Tests.
2. Run Topic discovery.
3. Run Daily production.
4. Download and inspect MP4s and manifests.
5. Confirm claims and asset licenses.
6. Run publishers with dry_run=true.
7. Only after successful end-to-end checks, set dry_run=false for a selected manual publish.
8. Queue status is `review_required`; manually approve before public publishing by changing it to `approved`.

## Schedule and capacity
Discovery runs every six hours. Production runs at 00:23 UTC (05:53 India time). Publishing is manual until media hosting and approval flow are completed. Three videos/day can exceed GitHub minutes, runner disk or time limits. Benchmark and adjust.
