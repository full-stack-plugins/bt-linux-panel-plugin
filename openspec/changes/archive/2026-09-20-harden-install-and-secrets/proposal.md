## Why

The installation guide downloads a root-level installer over plaintext HTTP and executes it immediately, while the ZCode manifest does not mark the panel bearer token as sensitive. These defects expose servers and credentials during routine setup.

## What Changes

- Replace plaintext download-and-execute guidance with HTTPS download, checksum verification, manual review, and separate execution.
- Mark bearer token configuration as sensitive.
- Add tests that prevent regressions in installation guidance and manifest secrecy.

## Capabilities

### New Capabilities

- `secure-panel-bootstrap`: Defines safe panel bootstrap and secret-handling requirements.

### Modified Capabilities

None.

## Impact

Affected files include BT setup skills, README installation guidance, ZCode configuration, tests, CI, and release metadata.
