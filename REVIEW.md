# Profile preview — compare before merging

This branch proposes items **2–12** from the profile improvement plan. New product-demo recordings (item 1) are deferred. The existing DocuRelay walkthrough is reused.

## Open both versions

| Before | Proposed |
| :--- | :--- |
| [Current README snapshot](https://github.com/phlppgdfry/phlppgdfry/blob/345d84a6aecb84cc60dcfe541361b6224945dc7a/README.md) | [Preview this branch](https://github.com/phlppgdfry/phlppgdfry/blob/profile/interactive-portfolio-preview/README.md) |
| [Live GitHub profile](https://github.com/phlppgdfry) | [Engineering notes](BUILD_NOTES.md) · [Milestones](MILESTONES.md) |

Use the two README links for the closest comparison: both use GitHub's repository Markdown renderer. The live profile has a narrower content column and a personal sidebar.

## What to compare

| Item | Current version | Proposed version |
| :--- | :--- | :--- |
| **2 · Try it** | Contact links first | Three direct routes to a download, browser simulator and existing recorded workflow |
| **3 · Project stories** | Short project descriptions | Three expandable problem / decision / next-step stories |
| **4 · Harbor map** | Decorative crane animation | Four clickable districts, with equivalent text links |
| **5 · Project covers** | Plain two-column project table | Six matching covers; real screenshots available in expandable panels |
| **6 · Monthly side quest** | General experiments list | September 2026: Git Personality Profiler, with a local run command |
| **7 · Engineering lessons** | General working method | Four specific lessons with linked evidence and extended build notes |
| **8 · Milestones** | Latest pushes and releases | Dated milestone log linked to commits, releases and runtime validation |
| **9 · Museum** | General programming humor | Three expandable exhibits based on documented issues and trade-offs |
| **10 · Useful statistics** | Repository and language counts | Curated app/demo/walkthrough counts with direct links; repo context retained |
| **11 · Mobile** | Two narrow project columns | One project per row and expandable detail |
| **12 · GIF variety** | Two general coding GIFs | Query-debugging and release-checklist illustrations alongside existing themed animations |

## Statistics, before and after

| Current | Proposed |
| :--- | :--- |
| ![Current repository-count card](https://raw.githubusercontent.com/phlppgdfry/phlppgdfry/345d84a6aecb84cc60dcfe541361b6224945dc7a/assets/activity.svg) | ![Proposed exploration card](assets/activity.svg) |

## Suggested review route

1. Open the proposed README and try its three action buttons.
2. Click the four harbor districts and confirm each route feels useful.
3. Open a screenshot and a project story. Compare the single-column layout at phone width.
4. Read the side quest and expand the museum exhibits for the playful parts.
5. Compare the activity card and check the milestone evidence.

## Editorial boundaries

- The monthly side quest is a dated editorial selection; a schedule does not invent a new pick.
- Museum captions are playful framing around documented engineering facts. They do not invent time spent, client incidents or personal reactions.
- Covers and new GIFs are illustrations. Existing product screenshots remain unaltered.
- The exploration counts describe the explicit selection in `data/showcase.json`, not all products or a continuous availability check.
- No live profile metadata or pins are changed by this PR. The daily updater continues to use `main` until a merge.

## Validation

The PR runs read-only checks for local links, image alt text, SVG validity, activity filtering, generated counts and preservation of editorial content. The activity generator was also run locally with public GitHub data on this branch.
