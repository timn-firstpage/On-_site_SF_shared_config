---
name: sf-shared-config
description: Prepare a shared Screaming Frog audit profile, guide user confirmation of sitemap and manual crawling, and hand saved crawl files back to onsite audit skills. Reuse suitable existing crawl evidence instead of reloading configuration.
---

# SF Shared Config

This skill is a prerequisite route for HTTPS, robots.txt and other onsite audit skills when usable crawl evidence is absent. Its scope ends at file handover. The user confirms the site/sitemap, starts and supervises the crawl in SF UI, and saves the result. Do not autonomously start, restart, pause or resume crawls. Do not perform audit judgments, generate the audit workbook, implement an independent crawler or configure unrelated global settings.

## Choose the route

Directly supplied `.seospider` files use [saved-crawl entry](references/saved-crawl-entry.md) first. Accept `source.mode=saved_crawl` and `source.crawl_file`; opening existing evidence does not require allow_new_crawl. Use the optional read-only preflight helper, preserve active sessions, open once or reuse matching exports, and share the source/export record across onsite flows. Import failure uses saved-crawl **Open + export** guidance, never profile Load + Start. Complete the caller's output/runtime preflight before expensive evidence retrieval.

1. Obtain the intended site/scope, caller and any existing crawl/file evidence. Verify as far as available tools allow that evidence belongs to this site, its time/scope are suitable, and it is usable by the caller. A latest filename, HTTP 200, binary signature or a nonempty file alone is insufficient. Existing evidence need not have every historical SF setting verified.
2. Suitable existing evidence: return its paths/crawl ID and provenance to the caller. Skip configuration and manual crawl guidance. If evidence covers only part of the caller's needs, retain it and identify the specific follow-up rather than forcing a whole-site repeat.
3. An active crawl: do not load a profile over it or interrupt it. Ask for the user's intended handover when necessary. Finish this interaction with a concrete next action rather than indefinitely polling.
4. No suitable evidence: use the preparation route below. Resume from accepted user confirmations; do not restart the setup every turn.

Read [profiles](references/profiles.md) when choosing/configuring a profile, and [handover](references/handover.md) for completion evidence and the caller record.

## Prepare without starting

- For first-time/full-site preparation, automatically select the bundled assets/sf-configs/onsite-main-js.seospiderconfig. Do not ask the user to choose main versus secondary or provide a path that can already be resolved from the installed skill. A targeted follow-up uses the bundled onsite-targeted-content.seospiderconfig only when that phase is actually needed. The user may override either selection with an explicit config path; an invalid override must not silently fall back to a bundled profile.
- Resolve bundled paths relative to the actual installed skill root on the executing host, then check access on the host running SF. A GitHub URL or a file on another machine is not a loadable local path. If necessary, stage a copy only through supported file operations into an accessible task/MCP directory and verify its hash. If no accessible copy can be established, return precise copy/download/Load instructions or request its actual host location; do not turn that into a main-versus-secondary choice. State the selected default profile and candidate verification status without adding a selection approval gate. Do not hardcode another host's path or infer a Downloads directory from the current project.
- Discover actual supported operations. Check that the selected file is accessible on the host running SF and within any applicable tool scope. Record the selected path and, when possible, file hash. A submitted path is not proof of a successful load.
- If reliable session evidence establishes that the intended config is already loaded and unchanged, skip loading. File existence alone does not establish this. Keep this record shared between callers; do not reload separately for HTTPS and robots.
- Back up/save the current configuration where supported before replacing it, and preserve existing crawl data. Load using a verified standalone config-load operation or supported native UI. No CLI/native capability may be assumed.
- Some MCP versions expose config_path only on sf_crawl. That operation starts a crawl, so it MUST NOT be used to load a profile in this manual-run workflow. When standalone loading cannot be performed, give the user the actual UI Load steps and selected file path. Unsupported native control ends that route immediately; do not loop initialization or guess tools.
- Before directing any manual Load, save/copy the already selected .seospiderconfig into the user's actual Downloads folder on the host running SF, then verify existence, nonzero size, read access and equality to the selected source (SHA-256 where possible). Discover the real Downloads location; do not infer it from the project or another host. Reuse an identical existing copy; preserve a different same-name file and choose an unused descriptive filename. Give the verified Downloads path for Load, not the internal skill asset path. If host access/permissions prevent saving, state the precise limitation and provide the selected binary's download/copy action to that host's Downloads first; do not claim saved or ask the user to Load a nonexistent path. This preparation file is distinct from the later saved .seospider crawl. No copy/load is needed for suitable existing evidence or an already verified unchanged loaded profile.
- Any native-control config-load failure (including inaccessible native-control helper/file, permissions, timeout or unsupported host) immediately switches to [manual Load + sitemap guidance](references/manual-load-fallback.md). Do not retry native initialization, hunt for helper files, switch to CLI or leave setup pending. Record the original tool error separately from a real SF profile-import error. First deliver and verify the selected config in Downloads as above, then give one bundled UI sequence: Load that file, verify mode, confirm/set this site's sitemap, manually run and save the crawl to Downloads. Do not ask the user to choose main/secondary again. A standalone load failure also receives this manual fallback rather than only a generic failure notice.
- Never claim configuration loaded or verified without tool/UI evidence or explicit user confirmation (record the source). Configuration changes affect future crawls, not old saved evidence. Main Spider / secondary List Mode must be confirmed after profile loading; mode changes can affect settings.

Before a new main crawl, apply [collection combination protection](references/collection-crawl-guard.md): the bundled main profile excludes multi-condition `/collections/<collection>/<filterA>+<filterB>` paths (including `%2B`). Verify Exclude in UI, preserve primary pages/pagination, and check observed site URLs for exceptions. An explicit custom profile needs the same check; do not silently replace it. Early signs of combination growth require one pause/save/correction action within the existing poll budget, never a new monitoring loop.

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

Path/permission/schema errors need a concrete correction, not repeated calls or fallback defaults. An unsupported tool receives no retry. Config-load failures use the immediate manual route above; a timed-out load remains unverified and the user checks current UI state before loading again. Only safe transient reads may receive at most two retries with backoff. MCP 429 and website HTTP 429 are different observations; preserve the source and obey Retry-After when supplied. This skill does not automatically recrawl URLs or manage the user's running crawl.

No automatic cleanup, website modification or GitHub publishing is part of a skill invocation. Keep credentials and local endpoint/storage/retention settings outside shared profiles. No third-party Python library is required by this instruction-only workflow.
