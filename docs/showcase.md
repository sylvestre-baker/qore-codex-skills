# Prepare the public showcase

The first-party source is `showcase/index.html` and `showcase/styles.css`. Stage only the selected public case evidence and demonstration:

```sh
python3 -B tools/build_site.py --output /tmp/qore-showcase-new
python3 -B tools/check_site.py /tmp/qore-showcase-new
```

Run from this candidate's repository root with Python 3 and an unused output path. The first command copies a static folder; it never deploys. The second checks local HTML references, project-prefix-safe URLs, symlinks and byte budgets. Neither establishes rendered accessibility or playback. The page requires no JavaScript, fonts, analytics or hosted Qore service.

The selected MP4 is at most 25 MiB, poster 500 KiB, VTT and transcript 100 KiB each, and complete staged folder 35 MiB. The video is a technical montage of separate actual executions, distinct from a personal application video. No YouTube channel is required.

The intended project prefix is `/qore-codex-skills/`. Before publication, inspect 320px and 1280px layouts, 200% zoom, sequential keyboard/focus, reduced motion, captions/playback, direct links and a failed-video response. Keep readable evidence outside the video.

`.github/workflows/pages.yml` has only an explicit manual dispatch trigger and refuses branches other than main. Build has read-only repository permission; only the deployment job receives Pages and identity-token writes in the github-pages environment. All action references are pinned. Configure repository Pages for GitHub Actions and approve publication separately before dispatching. A prepared workflow is not evidence of a successful hosted deployment. [GitHub custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

This implementation has not deployed the candidate page or new release. Anonymous hosted URL and release checks belong to the later publication step.
