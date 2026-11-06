# Contributing

Report packaging, ingress, migration, and release issues in the
[issue tracker](https://github.com/Wheemer/ombi-app/issues). For security
reports, follow the [security policy](SECURITY.md).

Submit changes as pull requests against `master`. Describe the change and
how it was tested. Add automated tests for major new functionality and include
a regression test when fixing behavior that existing checks miss.

[PR validation](.github/workflows/pr-validation.yaml) runs Home Assistant app
lint, Dependency Review, and the updater's Atheris fuzz test. The workflow
contains the commands and hash-locked dependencies for running the fuzz test on
Linux with Python 3.12. The [Builder](.github/workflows/onpush_builder.yaml)
checks amd64 and arm64 container builds.
