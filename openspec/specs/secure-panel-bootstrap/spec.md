# secure-panel-bootstrap Specification

## Purpose
TBD - created by archiving change harden-install-and-secrets. Update Purpose after archive.
## Requirements
### Requirement: Installer transport is authenticated

The documentation SHALL only retrieve privileged installers over HTTPS.

#### Scenario: Plaintext installer URL is introduced

- **WHEN** release validation detects an HTTP installer URL
- **THEN** validation SHALL fail

### Requirement: Download and execution are separated

The setup flow SHALL download, verify, and review the installer before privileged execution.

#### Scenario: A remote script is piped or chained directly to a shell

- **WHEN** validation detects direct remote-script execution
- **THEN** validation SHALL fail

### Requirement: Bearer tokens are sensitive

Host manifests SHALL mark bearer-token inputs as sensitive.

#### Scenario: ZCode renders plugin settings

- **WHEN** the bearer-token field is displayed or persisted
- **THEN** it SHALL be handled as a secret field

