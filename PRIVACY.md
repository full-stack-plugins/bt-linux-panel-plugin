# Privacy

Baota Linux Panel Plugin does not include telemetry, advertising, or a hosted data service of its own.

## Local processing

The plugin package contains guidance, Skills, commands, and host manifests. It ships no local MCP
server and stores no panel credential. The user's coding-agent host connects to the remote Baota MCP
endpoint that the user explicitly configures.

## Network activity (disclosed)

When an MCP tool is invoked, panel identifiers, operation arguments, and the configured Bearer Token
are sent by the host directly to the user-selected remote Baota MCP endpoint. Users are responsible
for the endpoint's deployment, transport security, access controls, logging, and privacy practices.
Do not place credentials in prompts, repository files, screenshots, receipts, or issue reports.

No credentials are stored in this repository, and no project file is uploaded by this plugin
itself. Opening the returned Jimeng link is what transfers the video to the Jimeng web app, and
that transfer is governed by Jimeng's own terms.

Users should review third-party product privacy terms before enabling integrations.
