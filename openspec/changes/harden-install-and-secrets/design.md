## Context

BT setup requires privileged server operations. The current quick-install command collapses transport, trust, and execution into one unauthenticated step.

## Goals / Non-Goals

**Goals:** require authenticated transport, explicit integrity verification, human review before execution, and secret-aware host configuration.

**Non-Goals:** install BT automatically or provision a live panel during CI.

## Decisions

- Documentation will use HTTPS and require a checksum supplied by the official release channel.
- The guide will refuse to invent a checksum and will keep execution as a separate explicit command.
- Static tests will scan both README and skill documentation.

## Risks / Trade-offs

The safer flow is longer and requires the operator to obtain an official checksum, but prevents silent network substitution.

## Migration Plan

Update documentation and manifest, add offline tests and CI, bump the plugin, then publish a corrected release.
