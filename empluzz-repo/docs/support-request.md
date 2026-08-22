# Support request: enable artifact reads through the session gateway

Send from joaquinz0721@gmail.com at https://support.claude.com. Paste the body below as is. Do not add screenshots of the dashboard, since it carries wage figures.

---

**Subject:** Enable artifact reads through the session gateway for my account

**Body:**

I use a Claude artifact as a live tracker and I need cloud sessions to be able to read it so they can publish updates to it.

When any cloud session tries to read the artifact with WebFetch, it fails with a message naming two separate routes, both unavailable:

> this environment's network allowlist blocks da80ff29-3a14-48a4-9d69-762e79ff2594.frame.claudeusercontent.com, and the session gateway could not serve the read either (artifact reads through the session gateway are not enabled for this session, or the artifact service no longer serves this version); your access to the artifact itself is fine (the permission check passed).

My question is about the second route only. I have searched docs.claude.com, code.claude.com, and support.claude.com and can find no documentation of "artifact reads through the session gateway" anywhere, so I cannot tell whether it is a setting I can change, a plan feature, an admin toggle, or something still rolling out.

**What I am asking for:** please enable artifact reads through the session gateway for my account, or tell me what controls it if it is something I can turn on myself.

**Why the documented workaround does not cover my case.** I know that adding `*.frame.claudeusercontent.com` to a cloud environment's Custom allowed-domains list fixes artifact reads, and I have already created an environment with exactly that entry. But the sessions I need this for are Cowork sessions, and Cowork does not appear to use Claude Code cloud environments. A Cowork container reports `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` regardless of my environment, and the environment selector only appears on the Code tab. The domain allowlist under Settings, Capabilities appears to be a Team and Enterprise feature, and I am on an individual plan, so I have no way to allowlist that host for Cowork.

**Identifiers, if they help:**

- Account UUID: `07e84edc-c715-4218-a6bf-24aa39c3069b`
- Organization UUID: `83a248d3-6955-4581-9e0f-62227f8e187e`
- A session that hit the error: `cse_01LqfmzfdUtqwo6RbfZSTEoK`
- Artifact: `https://claude.ai/code/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594`
- Date observed: 2026-08-21

**Secondary question:** is there any supported way to run a Cowork session in a specific Claude Code cloud environment? If that becomes possible, it solves my problem without any gateway change.

---

## What to expect

This is a background long shot, not the plan. Support may not have a switch for this at all. Do not wait on it before running the smoke test in `artifact-write-routes.md`, which does not depend on the answer.

If the reply asks you to add the domain to an environment, reply that you already have, and that the blocked sessions are Cowork sessions which do not use cloud environments. That distinction is the whole request and it is the part most likely to get skimmed.
