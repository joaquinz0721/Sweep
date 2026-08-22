# Ending the manual pasting: which doors are locked, and the one that opens

Session of 2026-08-21. Research and diagnosis only. Nothing was published to the artifact, nothing was submitted or transmitted, and the console-script fallback in MEMORY section 3 is untouched.

---

## Summary in four lines

1. **Session-gateway artifact reads do not exist in any Anthropic documentation.** Not a setting, not a plan feature, not an admin toggle, not a documented rollout. Support is the only lever, and it may well be an internal capability with no customer-facing switch.
2. **Cowork cannot be pointed at a cloud environment.** Confirmed three independent ways. The `empluzz` environment will never be reached from a Cowork session.
3. **The Chrome route is closed, and now proven rather than assumed.** The artifact runtime is always one cross-origin hop beyond anything the browser tools can execute in. Hard rule 3 can stay exactly as written.
4. **`empluzz` is not wasted. It is pointed at the right fix and the wrong surface.** Two surfaces do enter it, and they are precisely the two cases that matter: an interactive Code-tab cloud session, and a cloud routine. The routine one fixes the sweeps, which had been written off as unfixable without door 1.

---

## Door 1: artifact reads through the session gateway

**State: locked, and not by anything on your account.**

The phrase appears nowhere across `docs.claude.com`, `code.claude.com`, or `support.claude.com`. Searched directly and through several phrasings. The artifacts documentation, the cloud-environments documentation, and the network-configuration documentation all describe exactly one way for a session to read an artifact, and it is the allowlist, not a gateway.

So the error message is naming an internal server-side capability. It is not something a user setting exposes, and nothing in the documentation suggests a plan tier or an admin page controls it. That does not prove no switch exists, only that no published document describes one, which is the honest answer to "is this a setting I can flip."

**What to do about it: send the support request in `support-request.md`.** Treat it as a long shot running in the background, not as the plan.

Confirmed again this session from a live call: the block message is identical to the one in MEMORY, and it still ends with "your access to the artifact itself is fine (the permission check passed)." Access was never the issue.

## Door 2: the network allowlist

**State: open, documented, and already applied by you. It just does not reach Cowork.**

The cloud-environments documentation says it outright:

> If sessions in the environment work with artifacts, include `*.frame.claudeusercontent.com` in your list. Claude Code fetches artifact content from that host. If you leave it out, Claude can't read artifacts in sessions that run in the environment.

That is the fix, and it is the fix you already made. The problem is only which sessions inherit it.

### Can a Cowork session be bound to a cloud environment?

**No.** Three independent confirmations:

1. **The surface list omits Cowork.** The cloud-environments doc enumerates where environments apply: Claude Code on the web, the terminal with `claude --cloud`, Claude Tag, routines, the mobile app, and the Desktop app. Cowork is not among them.
2. **"The Desktop app" means the Code tab.** The desktop documentation opens with: the app has three tabs, Chat, Cowork, and Code, and "This page is the reference for the Code tab." The environment selector is documented as a Code-tab control. That matches what you observed.
3. **Cowork runs on a different network setting entirely.** The Cowork architecture overview says "A cloud session uses the same network-access setting that governs local Cowork and chat." That setting lives at Settings, Capabilities. Its allowlist option, "Allow network egress to package managers and specific domains," is documented under the heading "Configuring network access (Team and Enterprise plans)." On an individual plan there is no domain list to add anything to.

One extra data point from this session: the scheduled-task tool available inside Cowork does accept an `environment_id` argument. I passed a deliberately invalid identifier. It was swallowed without an error and no environment was echoed back in the created task, which was then deleted. So that argument is not a usable binding either.

**Conclusion: stop tuning `empluzz` for Cowork's sake. Tune it for the two surfaces below.**

## Door 3: driving Chrome

**State: closed. Tested live this session with your approval, then reverted and the tab closed.**

Your Chrome session is fine. The artifact loaded fully, titled "Application Command Center," with the Share control and your avatar. Authentication was never in question.

The crux you named was whether the browser tools can execute JavaScript inside the artifact's iframe rather than the top `claude.ai` frame. They cannot, for a structural reason:

- `javascript_tool` executes in the top document of a tab. It has no frame-targeting parameter.
- From the top `claude.ai` frame, every access into the artifact frame throws `SecurityError`: `contentWindow.document`, `contentWindow.claude`, `contentWindow.eval`, and any query through it. The iframe carries `sandbox="allow-scripts allow-same-origin allow-forms"`, but `allow-same-origin` means same-origin with respect to its own origin, not with `claude.ai`.
- Navigating the tab straight at the frame URL does not help. It lands on `claude.ai/code/frame/<uuid>`, which is itself another `claude.ai` shell that nests `<uuid>.frame.claudeusercontent.com` inside it. `window.claude` is `undefined` at every level a tool can reach.

So the runtime is always exactly one cross-origin hop past where the tools run. This is not a permissions problem and no approval unlocks it.

**Hard rule 3 stands as written.** Lifting it cost nothing and bought a definite answer, which is now recorded so no future session re-litigates it. Even in the best case it would only have helped you and me in chat, never the sweeps.

## Door 4: the one that opens

Two surfaces do route into `empluzz`, and between them they cover both cases.

### 4a. Interactive changes: a Code-tab cloud session

This replaces console pasting for every change you and I make in conversation. The session reads the artifact through the allowlist, so the tracked base version gets set, so the Artifact tool publishes normally with no force and no baseVersion parameter needed.

### 4b. The sweeps: cloud routines

This is the finding that changes your conclusion. You wrote that the sweeps run unattended with no browser, so only door 1 or a working environment fix could help them. **The environment fix is available to them.** Routines at `claude.ai/code/routines` have an environment picker in the creation form, documented step by step, and they run as full unattended Claude Code cloud sessions with connectors. A routine pinned to `empluzz` can read the artifact and publish to it on a schedule with nothing open on your machine.

Caveats worth knowing before you commit:

- Runs as a Claude Code session, not a Cowork session. Different tool surface.
- Minimum interval is one hour, and there is a daily cap on routine runs per account.
- All your connectors are included by default. Strip them to what a sweep actually needs.
- Cloud sessions require a GitHub repository. This is the one real prerequisite, and it is what the migration below is for.

---

## Moving empluzz to Claude Code without losing anything

### What carries over on its own

**Skills.** The documentation is explicit: Cowork sessions and cloud sessions, routines included, load the skills enabled for your claude.ai account, synced at session start. `application-packet-builder` keeps working unchanged as long as it stays enabled for the account. Manage it under Customize in the Desktop sidebar.

**Connectors.** MCP servers added in claude.ai are automatically available in Claude Code when the session is signed in with a claude.ai account. Gmail, Drive, Indeed, and ZipRecruiter all carry across. Routines select connectors per routine.

**The artifact.** Account-level. Same URL, same version chain, same 14 ticks. A move changes nothing about it.

### What does not carry, and has to be rebuilt

**The project instructions and the four project docs.** Claude Code reads `CLAUDE.md` from the repository, not claude.ai project knowledge. These have to be committed. A side benefit: hard rule 6 still states the old relocation policy and a session cannot edit project settings from inside. In a repo, I can just fix it in the file.

**Device folder access.** A cloud session has no local files. The authored builds currently in `Downloads` on device `jz` should live in the repo instead, which is better anyway, since MEMORY section 3 step 2 warns that the canonical reconstruction is the fixed point and the last published file is not. Git history makes that a fact rather than a thing a session has to remember.

**The two Cowork scheduled tasks.** Recreate as routines. They cannot be edited from a cloud session today, so this happens in the Desktop UI.

**The Cowork-only tools.** The Projects tool, the device bridge, direct file delivery into chat. Different surface, different affordances.

### Proposed repository layout

```
empluzz/                        (private)
  CLAUDE.md                     project instructions, rule 6 corrected
  docs/MEMORY.md                the running memory file
  docs/next-session-prompt.md
  docs/desk-checklist-2026-08-21.md
  docs/source-expansion-scoping.md
  dashboard/application-command-center.html
  dashboard/verify/             verify.js, shell.py, mkbase2.py, mklive3.py
  .claude/skills/application-packet-builder/   optional, belt and braces
```

Committing the skill to `.claude/skills/` as well as leaving it enabled on the account is cheap insurance: cloud sessions load repo skills in addition to account skills.

### Order of operations, so nothing is lost

1. Create the private repo on GitHub, empty.
2. Commit the four docs and a `CLAUDE.md`. A first draft of `CLAUDE.md` is delivered alongside this file.
3. Move the authored dashboard build and the verification harness in from `Downloads`.
4. Confirm `empluzz` is set to **Custom**, with `*.frame.claudeusercontent.com` in Allowed domains and **Also include default list of common package managers** checked. Without that checkbox the session loses npm and PyPI, which the verification harness needs.
5. Run the smoke test below.
6. Only once the smoke test is green, recreate the two sweeps as routines pinned to `empluzz`.
7. **Keep the claude.ai project until step 6 passes.** It is the archive. Do not delete it, and do not touch the frozen Google Sheet at any point.

### The smoke test

This is your stated success criterion: a trivial reversible change, published with no console, and the 14 ticks intact.

Open a Code-tab cloud session, or use a prefilled URL. The documented parameters are `prompt`, `repositories`, and `environment`:

```
https://claude.ai/code?environment=empluzz&repositories=YOUR_GH_USER/empluzz&prompt=<url-encoded prompt below>
```

The prompt, with the gates that protect the ticks:

> Read https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594 with WebFetch.
>
> If the fetch fails for any reason, stop immediately, report the exact error text, and change nothing.
>
> If it succeeds: parse the block between the ACC-STATE markers, count the applied ticks, and state the count. Expect 14.
>
> Then make exactly one change: append the word CONFIRMED to the end of the newest Last Checked note in the CAL array. Change nothing else. Do not reformat, do not reorder, do not touch any other array.
>
> Publish back to the same artifact by passing its URL. Do not pass force. Do not pass a capabilities object at all, since omitting it carries the stored declaration forward and a non-empty object would revoke anything not restated.
>
> Then read the artifact again, parse ACC-STATE again, and report the tick count a second time. If the two counts differ, say so loudly and do not attempt any further publish.

Gate on the delta the edit produces, never on absolute document length. That mistake already cost one failed attempt on 2026-08-21, because a build whose state block held `applied:null` was 586 characters shorter than the live page.

**If it passes:** the console script is retired for interactive work, and step 6 unblocks.

**If it fails on the WebFetch:** the environment is not being applied. Check that the session really started in `empluzz` and not `Default`, and check the checkbox in step 4.

---

## Where this leaves the sweeps

Worth stating plainly, since you asked for it. Under the current arrangement the sweeps genuinely cannot write the dashboard, and their refusal to publish is correct behavior that should stay. Neither the Chrome route nor anything about Cowork changes that. The routines route does change it, and it is the only thing found this session that does.

---

## RESULT, 2026-08-21: the door that actually opened

**A LOCAL Code-tab session in the Desktop app reads and publishes the artifact.** No GitHub, no cloud environment, no console pasting. This was not on the original list of four doors and it is better than any of them for interactive work.

**Why it works:** cloud sessions sit behind the egress proxy, which is the entire reason the allowlist matters. A local session runs on Joaquin's machine, on his own network, with no proxy in front of it, so `WebFetch` reaches the frame host directly and the tracked base version gets set. The Artifact tool then publishes normally with the URL, no `force`, and no `capabilities` object.

**Smoke test result:**

- Tick count before: 14. Tick count after: 14, byte-for-byte identical ACC-STATE block.
- Edit delta: +10 characters (` CONFIRMED` appended to the newest Last Checked note in CAL).
- Build slug moved `1787336084-e040` to `1787338925-ba95`.
- Stored capability declaration carried forward intact: `{artifact, downloads}`, contract 0.2.11. Omitting `capabilities` is confirmed correct.
- Ticking still works on the live page afterwards.

**Two caveats that must be carried forward.**

1. **The reconstruction dance is not gone.** The read returns the shell's transformed copy, not the authored source, so the session still had to cut on the ACC-HEAD and ACC-BODY marker pairs and re-wrap, exactly as `buildDoc()` does. The win is that the pasting is gone, not that the reconstruction is gone. Every prompt for this route must say so, or a session will try to edit the served document directly and produce garbage.
2. **The Artifact tool wraps published content in its own body skeleton.** After the first publish through this route the authored document was nested one level deeper than before. All four markers and all content survived, and the page's own self-republish is expected to restore canonical shape on the next tick. **This is the compounding risk to watch:** if each publish through this route nests another level, the document grows a wrapper per change. Verify the nesting count after any publish through this route, not just the tick count.

**What this does NOT fix: the sweeps.** A local session needs the laptop open and awake. Unattended dashboard writes still require a cloud routine pinned to `empluzz`, which still requires GitHub. As of 2026-08-21 Claude has never been connected to Joaquin's GitHub: his account shows three authorized OAuth apps (Git Credential Manager, GitHub CLI, Visual Studio Code) and one GitHub App (Copilot Chat), none of them Claude. That connection is the remaining prerequisite for the routines route, and it is no longer urgent.

## RESULT, 2026-08-22: a second door, and it needs no laptop

**A CLOUD Claude Code session reads and publishes the artifact**, through a route nobody had tried: the **Artifact tool's own `read` action**, not `WebFetch`.

**Why it works.** The 2026-08-21 finding was that a cloud session sits behind the egress proxy and so cannot `WebFetch` the frame host, and that a successful read is what sets the tracked base version. Both halves are still true. What was missed is that `WebFetch` is not the only thing that can perform the read. The Artifact tool reads the artifact through Anthropic's own service rather than over the open network, returns the full document, and sets the base version exactly the same way. The publish that follows is ordinary: pass the URL and the favicon, no `force`, no `capabilities` object.

**Smoke test result, the delegation change to the Build letter button:**

- Tick count before 14, after 14, same slugs in the same order.
- 41 internship rows and 12 scholarship rows in, 41 and 12 out, 41 unique slugs.
- Stored capability declaration carried forward intact: `{artifact, downloads}`, contract 0.2.11. Omitting `capabilities` is confirmed correct a second time.
- Version moved `1787428545-d4e8` to `1787430085-95fa`.
- All 48 harness assertions passed against the payload before it was sent.

**Caveat 2 from the 2026-08-21 result fires here too, and it does not compound.** The published document came back with **two** html and body wrappers as markup where the payload had one. Checked rather than assumed: reconstructing the published version on the marker pairs collapses it back to exactly one of each, that reconstruction is byte-identical to a reconstruction of the payload that was sent, and a third generation of the same operation changes nothing. So the extra wrapper is cosmetic, the page's own `buildDoc()` normalises it on the next tick, and the shape is a fixed point rather than a ratchet. **Keep checking it after every publish anyway**, with `markupCounts` from `dashboard/verify/accdoc.js`; one confirmed non-compounding case is not a proof.

**Caveat 1 is unchanged.** The read returns the shell's transformed copy, so the reconstruction dance is still mandatory. Use `dashboard/verify/mkbase2.py`, plain for a publish payload and `--null-state` for the copy that gets committed.

**What this does NOT fix: the sweeps, still.** This is an interactive session doing the work. A scheduled routine is a different surface and nobody has tested whether the Artifact tool behaves the same way there. That test is now the highest-value plumbing item, and it is cheap: one routine that reads the artifact and reports the byte count.

**Note for whoever connects GitHub:** the documentation states a cloud session can reach any repository the connected GitHub account can see, not only the ones ticked during install. "Only select repositories" limits webhook delivery, not session read access. Decide that knowingly.

## RESULT, 2026-08-22, later the same day: routines can publish

**A SCHEDULED ROUTINE, firing a fresh unattended cloud session, reads and publishes artifacts.** This was the highest-value open plumbing item at the top of this file. It is now answered, and the answer is yes.

**How it was tested, and why not against the tracker.** Joaquin was away from his desk, so an unattended publish to the page holding his 14 ticks was not a risk worth taking to answer a plumbing question. Instead a disposable probe page was published from an interactive cloud session, declaring `capabilities: {artifact: {}}`, the same capability the tracker declares. That is the whole point of the substitute: the `artifact` capability is what makes the server demand a baseVersion, and the missing baseVersion is what has blocked every failed route recorded above. Clearing that guard on the probe is clearing the same guard.

Probe page: `https://claude.ai/code/artifact/246c3ac3-8229-4697-934e-aa0b6c58da43`

**The routine.** One-shot, `create_new_session_on_fire`, environment `Sweep` (`env_01WH8sUQuEos7n7pWtz8Z6iz`), created from inside a cloud session with the meta MCP `create_trigger` tool, fired 2026-08-22 22:47:14Z.

**Results, taken from what the routine itself wrote into the probe page:**

- **Probe read: OK, 16,942 bytes.** The Artifact tool's `read` action works from a routine.
- **Tracker read: OK, 123,859 bytes.** A routine can read the live Application Command Center. Read only, nothing was written to it.
- **Publish to the probe: OK.** Version `1787438884-c13f`, published 22:48:04Z, roughly 50 seconds after the routine fired. The routine's own log entry and its flip of the status pill from `Awaiting routine` to `Routine published` are both on the live page.
- **Readback: entry present.**

**One false alarm, recorded so nobody chases it.** The routine reported 0 occurrences of `slug:` in the tracker. That is correct and means nothing: the rows are positional arrays with the slug at index 13, not keyed objects, so the string `slug:` does not appear. The 123,859-byte length is consistent with the 117.5KB read logged earlier in this file plus the day's edits, so the read was complete.

**Leading indicator that turned out to be wrong, also recorded.** At creation time the trigger's stored `session_context.allowed_tools` enumerated `preset:default` plus Task, Bash, Glob, Grep, Read, Edit, MultiEdit, Write, NotebookEdit, WebFetch, TodoWrite, WebSearch, BashOutput, KillBash, Skill, Tmux, Monitor, SendUserFile and REPL, with **no Artifact tool named.** It looked like the routine would have no Artifact tool at all. It did. `preset:default` evidently carries it. Do not read that list as an inventory.

**Two caveats before anyone points a routine at the tracker.**

1. **The reconstruction dance still applies and is untested from a routine.** The read returns the shell's transformed copy, so a routine publishing to the tracker has to cut on the ACC-HEAD and ACC-BODY marker pairs and re-wrap, exactly as route 0a does, with `dashboard/verify/mkbase2.py`. The probe was small enough to edit as a plain string, so this run proves the transport, not the reconstruction.
2. **Connectors do not come along.** `create_trigger` from inside a session refused the parameter outright: *the connectors parameter is not available for this organization*. A routine created that way fires sessions with no `mcp__*` tools at all, so no Gmail, no Drive, no Indeed. A routine that needs them must be created from the routines page on claude.ai, where connectors are picked per routine.

**What this unlocks.** The sweeps can write the dashboard unattended. The refusal-to-publish guard in the sweep prompts was correct for the surface they ran on and is no longer forced by the plumbing. Whether to lift it is a separate decision, and the paste-design in MEMORY section 1 is now optional rather than the only path.
