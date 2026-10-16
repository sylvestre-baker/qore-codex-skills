# Focused correction verification

All five original medium-severity CONFIRMED claims are currently RESOLVED, with F-FEAS-02 qualified strictly as a scheduling-window correction. Original verdicts and severities are preserved in results.json; none is reclassified as refuted.

| Original claim | Current status | Evidence |
|---|---|---|
| C01 / F-FEAS-01 | RESOLVED | Documented `resume-production` CLI delegates to the tested correction transition. FAIL, PARTIAL and BLOCKED retain criteria hash, processed IDs, decisions and complete delivery/request/verdict history. New artifact revision and fresh request work; stale criteria, unchanged artifact revision and late old verdicts are rejected. Current PASS is subsequently received. Active review, ASSIGNED, DONE and BLOCKED without negative review cannot resume. |
| C02 | RESOLVED | Session/run checks precede pending-verdict writes and state changes. All eight field/verdict combinations (PASS/FAIL/PARTIAL/BLOCKED) are rejected without changing current wait or owner; subsequent matching verdicts are accepted. |
| S1 | RESOLVED | Explicit `ProxyHandler({})` disables environment proxies. Socket-free real urllib dispatch under synthetic proxy variables retains bearer on direct 127.0.0.1 host and relative selector. Remote/userinfo/HTTPS endpoints, missing token and redirects are refused. |
| F-FEAS-02 | RESOLVED, scheduling scope | Virtual-clock real receive test starts no ACK at/past deadline and caps each timeout at remaining budget. Fetch takes 2 seconds; six ACKs consume the remaining 118 seconds (last timeout 18); seventh ACK remains pending. All seven decisions are durably saved before ACK, and a later fast receive replays the pending ACK without altering register state/history. |

The documented window is a scheduling budget, not an absolute OS deadline. A synchronous urllib socket timeout limits blocking socket operations; continuously arriving slow-drip bytes can prolong a response beyond the overall window. The timed fake honors configured timeouts, so its exact 120-second finish is not evidence of a real wall-clock deadline. No live network or slow-drip service was used. Local processing and check-to-dispatch time also are not enforced by an OS timer.

Read the five current raw files and original verified.json/reproduce.py directly. The original reproduction asserts vulnerable outcomes and does not exercise the new explicit correction operation; those old assertions are not used as the correction oracle. Independent current checks are retained in check.py. No author chats, finder reports, home/auth files, browser, real services or credentials were used. No source changes or subagents.

Validation: 7 focused check groups passed; related unittest suites passed 10 coordination + 6 agent-mail + 18 task-gate tests (34 total). Logs are saved beside this report. The repository ACK test checks deadline behavior but does not itself execute pending replay; the independent check explicitly does. Focused verification, not an exhaustive second campaign. Unfinished requested work: none. CLI correction wiring was inspected; correction semantics were exercised through the actual function, not an end-to-end CLI subprocess.

SHA-256 hashes below were checked unchanged after verification; original input hashes are also in results.json.

- `tools/coordination.py`: `63d1016d10aa4118e646856b489c2452bd3a48f8c0a59fd5e839192795122908`
- `tools/agent_mail.py`: `e9c44155cd43c93672ffff145d45969d7cc0af06d653b34dea689e56f8bf97bf`
- `tests/test_coordination.py`: `2eb658dca810b7ede9908127b1fef4038c6982c3963a7356b14a99f9f1c48a60`
- `tests/test_agent_mail.py`: `16447bf323317aa72a214231173a6fce04680037e1ec511342f2a9db83b1f556`
- `docs/coordination.md`: `eae7ee3a0bcf18be0b0bb4db4d409318a7049e0b35475e6db2562e745b8ebce5`
