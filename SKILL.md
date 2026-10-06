---
name: sf-shared-config
description: Prepare a shared Screaming Frog audit profile, guide user confirmation of sitemap and manual crawling, and hand saved crawl files back to onsite audit skills. Reuse suitable existing crawl evidence instead of reloading configuration.
---

# SF Shared Config

This skill is a prerequisite route for HTTPS, robots.txt and other onsite audit skills when usable crawl evidence is absent. Its scope ends at file handover. The user confirms the site/sitemap, starts and supervises the crawl in SF UI, and saves the result. Do not autonomously start, restart, pause or resume crawls. Do not perform audit judgments, generate the audit workbook, implement an independent crawler or configure unrelated global settings.

## Choose the route

1. Obtain the intended site/scope, caller and any existing crawl/file evidence. Verify as far as available tools allow that evidence belongs to this site, its time/scope are suitable, and it is usable by the caller. A latest filename, HTTP 200, binary signature or a nonempty file alone is insufficient. Existing evidence need not have every historical SF setting verified.
2. Suitable existing evidence: return its paths/crawl ID and provenance to the caller. Skip configuration and manual crawl guidance. If evidence covers only part of the caller's needs, retain it and identify the specific follow-up rather than forcing a whole-site repeat.
3. An active crawl: do not load a profile over it or interrupt it. Ask for the user's intended handover when necessary. Finish this interaction with a concrete next action rather than indefinitely polling.
4. No suitable evidence: use the preparation route below. Resume from accepted user confirmations; do not restart the setup every turn.

Read [profiles](references/profiles.md) when choosing/configuring a profile, and [handover](references/handover.md) for completion evidence and the caller record.

## Prepare without starting

- Main and secondary config paths are supplied by the user for this run. Do not hardcode another host's path, infer a Downloads directory from the current project or silently use bundled/default settings. Bundled profiles are review starting files; use one only when the user explicitly selects its actual host path. Request the secondary path only when a targeted follow-up is needed.
- Discover actual supported operations. Check that the selected file is accessible on the host running SF and within any applicable tool scope. Record the selected path and, when possible, file hash. A submitted path is not proof of a successful load.
- If reliable session evidence establishes that the intended config is already loaded and unchanged, skip loading. File existence alone does not establish this. Keep this record shared between callers; do not reload separately for HTTPS and robots.
- Back up/save the current configuration where supported before replacing it, and preserve existing crawl data. Load using a verified standalone config-load operation or supported native UI. No CLI/native capability may be assumed.
- Some MCP versions expose config_path only on sf_crawl. That operation starts a crawl, so it MUST NOT be used to load a profile in this manual-run workflow. When standalone loading cannot be performed, give the user the actual UI Load steps and selected file path. Unsupported native control ends that route immediately; do not loop initialization or guess tools.
- Never claim configuration loaded or verified without tool/UI evidence or explicit user confirmation (record the source). Configuration changes affect future crawls, not old saved evidence. Main Spider / secondary List Mode must be confirmed after profile loading; mode changes can affect settings.

## User sitemap and run checkpoint

After the profile is loaded, ask the user to confirm the intended start URL/site scope and inspect the sitemap in SF UI. The main profile enables linked sitemap crawling and robots discovery. The user confirms discovery or enables Crawl These Sitemaps and supplies this site's actual sitemap/index. Do not overwrite that site-specific modification by loading the generic profile again.

Bundle the checkpoint as one concise request: confirm loaded profile/mode, website and sitemap status, then manually Start and supervise the crawl. If no valid sitemap is available, record that fact and discovery limitation; do not invent a sitemap or prohibit all other checks. This manual confirmation is the user's requested workflow, not a requirement to verify every SF setting.

Remind the user to preserve error evidence. Isolated 404/410 and redirects can be audit findings, not reasons to restart everything. Sustained 429, repeated connection errors or obvious unbounded URL families merit pausing and review; the user decides whether to adjust/resume/restart in UI. JS rendering does not automatically click, scroll, log in or submit forms. Do not claim a render request rate caps every resource request.

After completion, ask the user to verify required Crawl Analysis has finished and save/export the crawl to their actual Downloads folder, then provide the exact path and completion status. Prefer a .seospider crawl when the caller can load it; otherwise use the caller's required exports. Database auto-save alone does not put a file in Downloads. A partial/stopped crawl must be labelled as such.

## Complete and return

Check accessible file existence, nonzero size and read access; preserve the website/time, completion and sitemap confirmations with their evidence sources. Inspect readable export structure where applicable. Do not deserialize arbitrary Java objects or declare a binary crawl fully usable without a supported SF load/caller check. If unavailable, state the exact unverified portion.

Write a small sf-handover.json in the existing run directory or another task-owned location using [handover](references/handover.md). It is a coordination record, not an audit Result. If the caller has not established its run directory, agree/use a writable task location and report the actual path; never create machine-local records in tracked source files.

Return the files/crawl identifiers and known limitations. The caller then validates actual data completeness, status codes, sitemap results and check-specific fields. Do not turn an unknown/429/missing row into Yes or NA. Do not wait indefinitely for user-run completion; return the current checkpoint and resume when the user supplies the result.

## Failure boundaries

Path/permission/schema errors need a concrete correction, not repeated calls or fallback defaults. An unsupported tool receives no retry. A safe transient load/read operation may receive at most two retries with backoff only when safe; a timeout with unknown load state requires state inspection first. MCP 429 and website HTTP 429 are different observations; preserve the source and obey Retry-After when supplied. This skill does not automatically recrawl URLs or manage the user's running crawl.

No automatic cleanup, website modification or GitHub publishing is part of a skill invocation. Keep credentials and local endpoint/storage/retention settings outside shared profiles. No third-party Python library is required by this instruction-only workflow.
