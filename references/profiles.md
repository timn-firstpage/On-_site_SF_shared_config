# Audit profile specifications

These are SF 24.0 sample-derived candidates. No SF native-class roundtrip, UI import or live crawl has been tested here. The manifest records field-level changes and SHA256 hashes. First-time/full-site preparation defaults to the bundled main profile; only targeted follow-up uses secondary. Resolve actual installed-host paths without asking the user to select main/secondary. Explicit user paths override these defaults, and invalid overrides must not silently fall back. Inaccessible defaults require concrete file-location/transfer guidance, not guessed local paths.

```text
主配置 onsite-main-js.seospiderconfig
用途：整套 onsite checklist 的共用主 crawl，上万 URL、动态链接发现、链接关系和内容相似度分析。
Mode：Spider（沿用 sample；运行前确认）。
User-agent / rendering：沿用 sample Googlebot Smartphone / JavaScript。
robots：Respect；显示内部/外部被挡 URL；不使用 custom override。
Sitemap：Crawl Linked XML Sitemaps ON；Auto Discover via robots ON；Crawl Specified Sitemaps OFF，不写死网站地址。用户在 UI 确认自动发现结果；没有声明或发现错误时，勾选 Crawl These Sitemaps 并填实际地址。完成本次修改后直接手动 run，不重新加载通用候选而覆盖网站输入。
Internal / External Hyperlinks、Images、CSS、JavaScript、Canonicals、Next/Prev、Hreflang：Store/Crawl ON，相关网站范围由用户确认。
Iframe：Store/Crawl ON，保留整站发现；SWF：Store/Crawl OFF。
AJAX timeout 5 秒；response timeout 20 秒；5xx retries 1；threads 4；URL rate 3/s（启用限速）。这是 SF URL 请求上限，不保证实际达到每秒 3 页；JS 渲染、响应耗时及机器资源可能限制吞吐。JS 页面可额外发起资源请求，不能把 3/s 理解成全部网络请求上限。出现持续 429、5xx 或超时时由用户暂停并在 UI 将限速降回 2/s；稳定后可按网站情况手动试 4/s，不自动提高或重跑。
Titles、Descriptions、H1/H2、Indexability、Word Count、Hash、Page Size、Response Time、Last Modified、Meta Robots、X-Robots、HTTP Headers：沿用 ON。
SRCSET：ON，包含响应式图片候选，记录量可能增加。
Structured Data：JSON-LD、Microdata、RDFa、Schema.org/Google validation ON。
Store Original/Rendered HTML：OFF；Screenshots/Website Archive：OFF。
Respect Noindex/Canonical/Next-Prev：OFF。
Ignore Non-Indexable URLs for Issues：OFF；Ignore Paginated URLs for Duplicate Filters：OFF。保留筛选证据，不意味着所有非 indexable / 分页告警都必须修复。
Always Follow Redirects：ON；Respect HSTS：沿用 OFF，方便检查原始 HTTP 响应；渲染浏览器行为需另外解释。
Near Duplicates：ON，90%，Only Indexable OFF；正文范围先保留 sample 默认，按网站模板确认。
Auto Crawl Analysis：ON，sample 未禁用分析任务；完成后核实实际需要的分析已生成，不能从空筛选推断通过。
Crawl total：保留 sample 5,000,000，不是 10,000 上限；depth/folder/query/per-depth/per-subdomain 小上限均未启用。
Fragment crawling、强制小写、移除全部参数：OFF。其余保护值保留 sample。
不自动排除分页/筛选 URL；运行中发现循环时用户保存证据、暂停并调整，不保证无限 crawl 完成。

次配置 onsite-targeted-content.seospiderconfig
用途：已有主 crawl 之后，对用途不明、soft 404、动态指令等选定页面保留内容证据。
Mode：List；切换模式后重新核对配置，不假设导入会覆盖所有模式转换行为。
User-agent / rendering / robots：Googlebot Smartphone / JavaScript / Respect。
Sitemap：关闭，不重新发现/抓取整站 sitemap。
Depth：启用 0；每批约 25 个上传 URL，由用户清单控制，不在 profile 中硬写 25 总上限。
Internal / External Hyperlinks：Store ON / Crawl OFF。
Canonicals、Next/Prev、Hreflang、Iframe：Store ON / Crawl OFF。需要核实目标时显式加入清单。
Images、CSS、JavaScript：Store/Crawl ON；Meta Refresh Store/Crawl ON；SWF OFF。
AJAX 5 秒；response timeout 20 秒；5xx retries 1；threads 2；URL rate 1/s。
提取字段、schema validation、SRCSET、Respect/Ignore 筛选选项：同主配置。
Store Original/Rendered HTML：ON；Screenshots/Website Archive：OFF。
Near Duplicates：OFF；Auto Crawl Analysis：OFF，避免每批重复分析。需比较内容时把相应 URL 放在同一批，手动开启 Near Duplicates 并执行分析；不能把批次结果当整站结果。
重定向/渲染资源可产生额外请求，depth 0 不代表只发 25 次请求。External Links Crawl OFF 可能使某些外部资源没有独立响应记录；核实结果，必要时针对资源清单补查或临时开启并记录范围。
被 robots 挡住的公开页面仍不会取得 HTML；必要时使用用户知情的独立 Ignore robots but report status 诊断批次，之后恢复。诊断取到 noindex 不能证明 Google 可读取。

Checklist 覆盖
9 HTTPS：HTTP/重定向/资源关系；www 四版本仍需额外 URL 检查，单个主域名 crawl 不能证明四版本一致。
10 Robots：实时 robots 配合主 crawl 与内容补查；Python/Agent 按各项实际证据判断。
11 Sitemap：用户确认来源，crawl 后分析响应、indexability 和来源关系；GSC 提交情况需 GSC。
12-15 Directives/Canonical/Pagination/Hreflang：保留原始 URL、指令、关系和相关分析；Google-selected canonical 需 GSC。
17-18 Titles/Descriptions：提取及问题筛选；字符/像素阈值先用 sample 默认，按最终检查标准单独调整，不把 155 字符等旧阈值直接当质量判定。
20 Images：图片记录、大小、alt 及 srcset；不保存整站图片归档。
21 内部重复与22薄内容：主 crawl Near Duplicates/word count；中文词数不是自动薄内容结论，内容判断用补查证据。外部重复、E-E-A-T 另需来源/人工判断。
23 Schema：提取和验证；Google 展示/增强报告需当前官方资格与 GSC，旧 checklist 的 schema 展示假设不由 config 证明。
24-27 Internal Links/Crawl/URLs/Status：链接与响应关系，软404/循环必要时补内容；真实 Google 抓取量需 GSC/日志。
7-8、16、28-31：GSC、移动UX/交互、竞争对手、速度/CWV、Local、Analytics/Backlinks需各自数据来源，不能只靠此 profile 完成。

本机单独设置（不假设随 profile 迁移）
Database Storage，SSD；Memory Allocation 暂不指定，待用户确认 Mac RAM。
Crawl Retention 建议30天，进行中或需对比的 crawl锁定。独立导出/报告不会因此自动清理。
MCP endpoint/allowed directory、本机路径、API凭据由运行机提供，不写入共享配置。
```

[Field manifest](../assets/sf-configs/profile-manifest.json). Configuration values are chosen audit settings, not guarantees of site completeness.
