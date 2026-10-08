# Collection combination crawl guard

The bundled main profile excludes multi-condition paths of the form `/collections/<collection>/<filterA>+<filterB>` (including case-insensitive `%2B`). The exact rule is in [collection-combination-exclude.txt](../assets/sf-configs/collection-combination-exclude.txt) and embedded in the main profile's Exclude field. It is host-independent. It does not exclude collection roots, single filters, `?page=2` pagination or product paths. The targeted profile remains available for representative excluded URLs.

## Before the user starts

- Reuse existing evidence normally; do not recrawl merely to apply this guard.
- For a new main crawl, verify the exclusion is present in Configuration > Exclude after profile loading. For explicit custom profiles, add the rule through supported controls or include paste instructions in the existing manual setup checkpoint; preserve other exclusions and site-specific sitemap settings. No invented MCP setter or automatic Start.
- Check available navigation/URL samples: a literal `+` can be a legitimate slug. If this site's matching paths are intended primary landing pages rather than filter combinations, use a narrower site-specific rule and record it. Keep exclusions in run provenance/coverage, never call excluded URLs audited or defect-free.
- Query-string filters, alternative category paths and parameter permutations need separate evidence-based rules. Do not strip all parameters or remove pagination globally. Respect Canonical hides rows but does not stop crawling their outlinks; it is not this guard.

## Existing crawl has expanded

Ask the user to pause and save the current crawl, retaining representative combination URLs and Inlinks. Add/verify the rule and preserve site-specific sitemap settings. Exclusions do not erase already-crawled rows; use a fresh main crawl when a clean bounded inventory is required, only when the user is ready to start. Do not reload a generic profile over an active crawl.

## Runtime observation

At the first normal progress checkpoint, and when progress stalls while discovered URLs grow, inspect only a small URL sample and counts. If combinations are expanding, return one concrete pause/save/exclusion action; do not keep polling at the same progress or increase speed to compensate. Reuse the caller's poll budget and existing observations rather than adding a separate monitoring loop. A 5 URL/s cap does not limit the total URL inventory.

Use a small user-selected List Mode sample for canonical/robots/noindex checks where needed. Preserve missing coverage; never automatically enumerate combinations to reconstruct the excluded inventory.
