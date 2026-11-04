---
title: Internal naming decision
head:
  - - meta
    - name: robots
      content: noindex, nofollow
---

# Naming decision

The public product name is **Sherpa** and the planned GitHub repository slug is `sherpa`. The npm package name is `sherpa-skill` because `npm view sherpa` returned an existing `0.1.8` package on 2026-11-04; `npm view sherpa-skill` returned 404 on that date. npm names are not reserved by an availability check, so recheck before publishing.

The repository API lookup for `Anshkaliya18/HackathonOS` returned 404 during the check. The prepared `scripts/finish-rename.sh` contains commented rename and metadata commands; it has not been run. Product strings use Sherpa while “hackathon” remains in descriptions of the use case.
