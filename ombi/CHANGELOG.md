# Changelog

## 4.60.14 (2026-08-06)

- Updated Ombi upstream version to `4.60.14`.

## 4.60.12 (2026-07-29)

- Updated Ombi upstream version to `4.60.12`.

## 4.60.10 (2026-07-08)

- Updated Ombi upstream version to `4.60.10`.

## 4.60.9 (2026-07-07)

- Updated Ombi upstream version to `4.60.9`.

## 4.60.8 (2026-07-03)

- Updated Ombi upstream version to `4.60.8`.

## 4.60.7 (2026-07-02)

- Updated Ombi upstream version to `4.60.7`.

## 4.60.6 (2026-06-19)

- Updated Ombi upstream version to `4.60.6`.
- Added a scheduled Ombi-only updater workflow.
- Switched Home Assistant to the generic multi-arch image `ghcr.io/wheemer/ombi-app`.
- Clarified the docs for Ombi's Base URL when running through Home Assistant ingress.
- Removed the internal ingress Base URL toggle from the user-facing app options.
- Fixed direct port access so published port `3579` is not blocked by the ingress proxy.
- Switched README branding to repo-hosted images and added a GitHub social preview image for forum link previews.
- Moved Ombi data to Home Assistant's backed-up app config storage and added a legacy config copy path.
- Fixed legacy Ombi migration so Ombi App imports existing `addons_config/ombi` data whenever the new app config does not already contain Ombi databases.
- Removed the old legacy config folder after a successful migration when Home Assistant permits it.
- Mounted Home Assistant config read/write so the legacy config folder can be removed after migration.
- Added explicit migration docs for users moving from the old alexbelgium Ombi add-on, including the instruction not to delete old add-on data before Ombi App imports it.
- Renamed the Home Assistant add-on display name to `Ombi App`.
- Clarified user-facing docs to refer to the Home Assistant add-on as `Ombi App`.
- Removed the broken upstream preview screenshot from the README files.

## 4.55.2-6 (2026-06-19)

- Restructured the fork as a normal single-app repository with Ombi at `ombi/`.
- Added Home Assistant ingress support by setting Ombi's `BASE_URL` from the Supervisor ingress path.
- Published images under `ghcr.io/wheemer/ombi-app`.
- Restored Ombi `icon.png` and `logo.png` so Home Assistant shows the right branding.
- Removed broad device passthrough and the old custom AppArmor profile.
- Removed obsolete/deprecated warnings from the active fork metadata.
- Trimmed the build workflow and template scripts to the pieces this app actually uses.
- Rewrote README and funding links for the fork.

## 4.55.2-archived (2026-02-18)

- Upstream app was archived in `alexbelgium/hassio-addons`.
- Users were directed to migrate to Seerr.
- Automated upstream updates were paused.

## Earlier Upstream History

Older versions followed `linuxserver/docker-ombi` updates in the original upstream app repository.
