# Manual Load + sitemap after automation failure

Read this when a standalone/native config-load operation fails or cannot be used. The failed native tool/helper does not establish that the SF config file is corrupt. Capture the actual error, stop the automation route and deliver the complete manual path in the same response. Do not require native-control troubleshooting before the user can proceed.

Full-site preparation defaults to main; targeted follow-up retains the selected secondary. User overrides stay overrides; never substitute another profile without instruction.

## Deliver the configuration before Load instructions

Resolve the user's actual Downloads folder on the SF host using available host/file capabilities. Copy the selected binary there and verify nonzero size, readability and source/copy SHA-256 equality where possible. Reuse an identical copy; do not overwrite a different existing file. Choose an unused descriptive filename for a different version and report the actual resulting path. Record delivery separately from load_state: copying a profile does not load it into SF.

If the agent cannot write/access Downloads on that host, explain the actual limitation and give the selected binary download/copy step to Downloads first. A copy on the agent's separate computer is not delivery to the SF host. Link the actual binary download for a bundled profile, not a GitHub HTML page renamed as config. Do not report saved until observed or explicitly user-confirmed. An inaccessible user override requires its copy/transfer, not substitution with the bundled default. Once the file is available, give the Load and sitemap sequence below. A verified already loaded unchanged profile skips delivery/reloading.

## Main preparation instructions

Present this as one concise, numbered sequence in the user's language, substituting the resolved local path when available:

1. State the verified Downloads config path (or clearly label the user's download step if delivery cannot be performed). Save current crawl/config if needed; do not change settings during an active crawl. Open SF's Configuration > Load (or the version's configuration Load menu), and select that Downloads .seospiderconfig. Where already visibly loaded, confirm state instead of unnecessarily loading again.
2. Confirm Mode > Spider. Open Configuration > Spider > Crawl and find XML Sitemaps. Enable Crawl Linked XML Sitemaps. Check Auto Discover XML Sitemaps via robots.txt, or enable Crawl These Sitemaps and paste this site's actual sitemap/index when known or required. Remove another site's explicit sitemap entries. Do not claim the sitemap has been successfully fetched just because configured.
3. Confirm the website/start URL, allowed scope and sitemap configuration. Request one reply confirming config loaded + sitemap configured, or the actual missing/invalid sitemap situation. Do not ask for every SF toggle or another profile selection. Do not mark loaded until this reply or reliable tool/UI evidence exists.
4. The user manually clicks Start and supervises the crawl. Retain normal HTTP error evidence; sustained429, connection failures or unbounded loops warrant user review. After completion and relevant Crawl Analysis, save/export the result to the actual Downloads folder and return its file path plus completed/stopped status.

Do not reload the generic profile after the user edits sitemap settings. If a real UI import fails, request the exact SF import error/version and retain the unverified state; do not imply the profile has loaded or silently start with defaults. No retry loop or automatic crawl is needed.

## Targeted follow-up differences

Use onsite-targeted-content.seospiderconfig (or the supplied override), confirm List Mode/depth 0 and robots settings, keep linked sitemap crawling OFF, then upload the caller's selected URL list. Do not enable whole-site sitemap discovery for the targeted batch. Reference the already confirmed main sitemap rather than forcing its confirmation again.

## Checkpoint

Record phase=awaiting_user, selected source and delivered Downloads paths when known, delivery verification/source, load_state=unknown until confirmed and original error/tool source. next_action is "Save selected config to SF-host Downloads" if delivery is unavailable, otherwise "Manual UI Load from Downloads, then site/sitemap confirmation". This is a finite handover, not a background pending task. Resume from the actual completed step. A native error is not a website audit issue.
