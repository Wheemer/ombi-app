# Security Policy

Security fixes are applied to the latest published Ombi App release.

Use GitHub's [private vulnerability reporting](https://github.com/Wheemer/ombi-app/security/advisories/new) for vulnerabilities in this Home Assistant app, including its container, ingress, and migration code. Include the app version, affected configuration, and reproduction steps. Remove credentials, API keys, and private URLs from logs.

For vulnerabilities in Ombi itself, use the [upstream security policy](https://github.com/Ombi-app/Ombi/security/policy).

## Repository safeguards

The [branch rules](https://github.com/Wheemer/ombi-app/rules/26702586) require
`Validate Ombi` on up-to-date changes to `master` and block force pushes and
branch deletion. The release workflow uses a validated fast-forward so it can
publish and verify the multi-architecture container before advertising the new
version to Home Assistant. A PR-only rule would block that promotion with the
current release identity. This is the rationale for accepting [Scorecard alert
#3](https://github.com/Wheemer/ombi-app/security/code-scanning/3).

This is a solo-maintained repository. Contributions go through automated
validation, and Dependabot can merge validated updates without a second
maintainer's approval. Lint, dependency review, fuzzing, CodeQL, and container
builds provide automated coverage. Independent human review is not required.
This is the rationale for accepting [Scorecard alert
#34](https://github.com/Wheemer/ombi-app/security/code-scanning/34).
