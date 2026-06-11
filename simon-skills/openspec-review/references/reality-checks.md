# Reality Checks

`CODE_PASS` is not `RUNTIME_VALIDATED`.

A compiling codebase and green tests can confirm the same false assumptions as the implementation.

## Reality Evidence

Runtime claims need at least one of:

- real DB query;
- live API call;
- actual LLM call or trace with raw response;
- browser run or screenshot/trace;
- production-like command output;
- persisted trace with input, prompt, output, validation, and handoff.

## Red Flags

- evidence path missing;
- report says "passed" without command output;
- trace only has final output;
- mock test proves external behavior;
- `.sql` file treated as applied migration;
- raw LLM answer missing for structured-output claim;
- `assumed_not_verified` empty for external-system work.

Any external reality discrepancy is a DECISION finding.

