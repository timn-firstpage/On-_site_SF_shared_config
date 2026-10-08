# Saved crawl entry and operational checkpoints

Applies to HTTPS, robots.txt and sitemap audits. User-supplied completed `.seospider` files are a first-class entry point, not a reason to run shared configuration again. “spiderseo file” in conversation may mean this format; inspect the supplied file/path rather than assuming its extension. These steps supplement each audit's existing rules, not its scoring or fatal-error policy.

## One entry, no setup loop

1. **Select evidence once.** An explicitly attached/named file for this run wins over stale config source fields or the current SF session. Set `source.mode=saved_crawl`, `source.crawl_file=<actual path>`. Relative paths resolve against the provided config directory. If several supplied files conflict on site/scope, ask one bundled question. Do not silently fall back to an unrelated loaded crawl. Usable matching exports can bypass opening the binary entirely.
2. **Local preflight once.** Check file existence, readable nonempty regular file, extension and source fingerprint. `scripts/preflight_saved_crawl.py` provides this check using Python standard libraries. `.seospiderconfig` is configuration, not a crawl; do not rename it to make it pass. Never modify the user's input. Avoid hashing/copying the same large file for every audit: reuse its unchanged source record. File checks cannot establish site, crawl completeness, SF compatibility or field coverage.
3. **Check tools and session before opening.** Discover an actual supported saved-crawl open/import operation and export capability. Do not guess a tool name, use `sf_crawl`, Start/Resume, or load a generic configuration. Preserve any active/unsaved crawl. If it cannot be preserved through verified operations, use supplied exports or ask the user to open the saved file in a separate SF instance/after saving their current work. Never switch the active Spider concurrently from two audit flows.
4. **Open at most once per file/session.** Reuse the loaded crawl ID when the source fingerprint and session still match. If the session has changed, validate its identity before reuse; do not trust a prior ID blindly. One failed/unsupported open switches to the saved-crawl manual fallback below. No native-helper hunt, configuration fallback, or automatic recrawl.
5. **Validate usable data.** Obtain actual site/hosts, crawl timestamp (not filesystem mtime), saved completed/partial state when available and the caller's required fields. Infer an unambiguous site from loaded metadata rather than asking the user to type it again. If only historical/partial evidence exists, retain supported checks and label the date/scope; no blanket age cutoff or requirement to have used today's profile. In particular, do not add an analysis-completion gate to sitemap 11.7's accepted empty-result rule.
6. **Export once, consume locally.** Each flow declares only the needed filters/columns. Cache by source fingerprint + SF session/crawl ID + export/filter + field set + analysis/render context. Archive full exports with actual row counts and truncation/page-completion flags; a model preview is not an export. If required, finish local Crawl Analysis on existing data only when the operation is known not to recrawl; otherwise ask for the specific export. Changing configuration does not retroactively populate missing data.
7. **Deliver or checkpoint once.** Use available evidence, permitted finite static checks and the flow's own error policy. Ask only for missing export/field evidence rather than restarting the full scan. New crawl preparation is a separate permitted follow-up, not an import fallback. For ordinary gaps deliver supported results with Human Check, then await new input without polling a user task. HTTPS fatal network interruption remains a failed run with no final workbook, as its skill requires.

`source.allow_new_crawl=false` does not disable opening/analyzing a supplied saved crawl. `checks.live_checks=false` disables new website HTTP reads, not local parsing or export inspection; if retrieval needs remote MCP transport, obey that tool's permissions and the caller's network-error policy.

## Saved-crawl manual fallback (different from config Load)

Give a single bundled action: open the supplied **saved crawl** using SF's saved-crawl Open command (typically File → Open; follow the installed version), verify the displayed site, then export the missing named tabs/filters and return their actual paths. **Do not instruct Configuration → Load, sitemap reconfiguration or Start for this route.** A version/corruption error should be captured once; ask for a fresh portable save or readable exports from the user's working SF version. A cross-host file needs one verified staging copy or manual open on the correct host, not a speculative local path.

If the user provided a database directory instead of a portable file, ask for a supported saved crawl/export; do not copy a live database as though it were a `.seospider` file. No SF access is needed for usable CSV/NDJSON exports. Without a saved-crawl reader or exports, only independent live checks can proceed when permitted; never claim the binary was analyzed.

## Shared local record and loop guards

Store `source-file.json`/`sf-handover.json` and export records under the existing integrated run directory. Suggested source fields:

```json
{
  "route": "saved_crawl",
  "source": {"path": null, "size_bytes": null, "mtime_ns": null, "sha256": null},
  "preflight_state": "unverified",
  "load_state": "not_attempted",
  "load_attempts": 0,
  "session_id": null,
  "crawl_id": null,
  "site_url": null,
  "crawl_timestamp": null,
  "crawl_state": "unknown",
  "exports": [],
  "errors": [],
  "next_action": null
}
```

Record provenance for observations. Session IDs/crawl IDs may be absent if the interface does not supply them; use supported identity evidence instead. Source mtime is for change detection only. Load failure stays terminal for unchanged input/capability during the run; a new supplied file, user-opened session, fixed path/permission or tool capability can trigger a fresh attempt. Do not call a failed export repeatedly without such a change, except bounded safe transient read retries allowed by the caller.

Known sitemap/robots sources and exports in the integrated run are reused across flows when scope/time/fields match. Do not re-fetch already obtained robots/sitemap XML per check. Identify snapshot differences when historical crawl data is combined with current live XML; live data does not silently rewrite historical evidence.

## Error handling

Persist stage, error code, original message, affected file/tool, time, attempts, recoverability and concrete next action. Keep operational errors in logs/handover; describe only their material evidence gap in the customer workbook.

| Condition | Next action; stopping point |
| --- | --- |
| File missing/unreadable/empty/wrong type | Correct path/permissions or ask for saved crawl/export; no repeated import |
| File changes during preflight | Ask for a completed stable save; no import until stable |
| No supported reader/export capability | Manual saved-crawl Open + exact required exports; no setup/crawl fallback |
| Busy active/unsaved SF session | Preserve it, reuse available exports, checkpoint once |
| Import rejected/version mismatch/corrupt file | Preserve error; manual open/resave or readable exports; no blind retry |
| Missing/truncated export | Request only missing fields/full export; retain confirmed findings; sitemap 11.7 remains its explicit exception for an available empty result |
| API/website 429 or transient reads | Preserve source and Retry-After, obey cumulative caller budget; never indefinite polling |
| HTTPS transport interruption | Follow HTTPS fatal rule; shared retry guidance does not override it |
| Workbook destination/runtime unavailable | Check before expensive retrieval; save findings and a clear generation error, never claim an XLSX was produced |

Before substantial retrieval, confirm a writable run/output directory and the caller's actual report runtime. Do not install unrelated packages or change a shared runtime merely by reading config. Scripts enforce only their documented local behavior; session serialization, cache reuse and retry budgets here are agent responsibilities, not a hidden background service.
