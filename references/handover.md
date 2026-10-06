# File handover and caller contract

Use this reference when deciding whether an existing file can skip setup, or when the user saves a manually completed crawl.

## Existing evidence

Confirm the intended website and scope, crawl time and source. Match the caller's required fields/coverage using exports or SF metadata where accessible. Do not reject useful evidence solely because a historical profile or unrelated setting is unknown. Do not accept an arbitrary latest crawl. Keep the original ID when a different crawl is subsequently loaded for follow-up.

A .seospider file requires the caller's supported SF load/import route. A name, extension, Java header or hash does not prove it is a complete readable crawl. If only CSV/NDJSON is accessible, pass files with their mapped fields; loading a configuration is not necessary to analyze those files.

## Manual completion checkpoint

Request the exact saved file path, intended website, crawl date, completed/stopped status and sitemap outcome. Prefer a single bundled question over repeated questions. Read accessible files without modifying them. A user report is accepted provenance but must be labelled user-confirmed rather than tool-verified.

In Database Storage, SF auto-saves internally. The user must explicitly save/export a portable crawl or required exports to Downloads for this workflow. Do not copy an active database folder as a portable crawl. Saving configuration produces .seospiderconfig; this is not the result file (.seospider).

The shared skill does not judge sitemap health or page status. Record whether sitemap was configured/read and any reported errors; the downstream audit analyzes broken URLs, redirects, noindex, canonical and coverage. A sitemap can parse successfully but still list broken links.

## Coordination record

Use the existing run directory for sf-handover.json. Local paths/records are not committed. This is an example of record structure, not direct SF MCP arguments:

```json
{
  "schema_version": 1,
  "phase": "handover",
  "route": "manual_new_crawl",
  "site_url": "https://example.com",
  "allowed_hosts": ["example.com"],
  "caller": "onsite-audit-robots",
  "main_config": {
    "path": "/user-provided/onsite-main-js.seospiderconfig",
    "sha256": null,
    "load_state": "user_confirmed",
    "mode": "Spider"
  },
  "secondary_config_path": null,
  "sitemap": {
    "urls": ["https://example.com/sitemap.xml"],
    "configuration_source": "user_confirmed",
    "read_state": "unverified"
  },
  "crawl": {
    "id": null,
    "timestamp": null,
    "state": "completed",
    "state_source": "user_confirmed",
    "analysis_state": "user_confirmed"
  },
  "files": [{
    "path": "/user-provided/Downloads/example.seospider",
    "kind": "sf_crawl",
    "exists": true,
    "readable": true,
    "sf_load_verified": false
  }],
  "gaps": ["Caller must verify the saved crawl loads and contains its required fields"],
  "next_action": "Caller inspects saved crawl data"
}
```

phase: preparation / awaiting_user / handover. These are coordination states, never spreadsheet results.
Config-load failure switches immediately to awaiting_user with manual Load + sitemap confirmation as next_action. Preserve original native/tool errors without labelling them site errors. A manual instruction does not establish load_state=user_confirmed; wait for explicit confirmation or reliable observed evidence.
route: existing_evidence / active_user_crawl / manual_new_crawl / manual_targeted_followup.
Use null/unknown for facts not observed; never fill guessed paths, time, IDs or completion. Existing-evidence routes may have no config record. Load-state sources distinguish tool_verified, user_confirmed and unknown. A file can be present while SF readability remains unverified.

For a new config selection, also record main_config.selection_source as bundled_default or user_override. Default main paths are resolved from the installed skill root or a verified accessible copy, not required from the user. Secondary defaults apply only when a targeted follow-up is needed. The user-provided paths in the example illustrate overrides rather than required first-run inputs.

For manual loading add an optional config_delivery object: source_path, downloads_path, host, sha256, state (tool_verified / user_confirmed / unavailable / not_required) and reason when unavailable. Paths/hash are null until known. The delivery record describes the selected main or targeted file. main_config.path/secondary_config_path identify the actual file used for loading; retain the bundled/override source separately. A verified copy does not change load_state; user-confirmed transfer is not a tool-verified hash check. Reuse matching copies without overwriting a different existing version. The later files list describes crawl/results, not a delivered config masquerading as crawl evidence.

Resume from the recorded phase and shared config state. Do not repeat confirmed sitemap/config checkpoints unless website/profile/mode has changed. Stopped/partial evidence can still support selected checks, but cannot be called complete.
