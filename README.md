<p align="center">
  <img src="https://raw.githubusercontent.com/Wheemer/ombi-app/master/ombi/ombi.png" alt="Ombi logo" width="537">
</p>

___

[![Version](https://img.shields.io/badge/dynamic/yaml?label=Version&query=%24.version&url=https%3A%2F%2Fraw.githubusercontent.com%2FWheemer%2Fombi-app%2Fmaster%2Fombi%2Fconfig.yaml)](ombi/config.yaml)
[![Ingress](https://img.shields.io/badge/dynamic/yaml?label=Ingress&query=%24.ingress&url=https%3A%2F%2Fraw.githubusercontent.com%2FWheemer%2Fombi-app%2Fmaster%2Fombi%2Fconfig.yaml)](ombi/config.yaml)
[![Builder](https://github.com/Wheemer/ombi-app/actions/workflows/onpush_builder.yaml/badge.svg)](https://github.com/Wheemer/ombi-app/actions/workflows/onpush_builder.yaml)
[![Update Ombi](https://github.com/Wheemer/ombi-app/actions/workflows/update_ombi.yaml/badge.svg)](https://github.com/Wheemer/ombi-app/actions/workflows/update_ombi.yaml)
[![Add repository to Home Assistant](https://img.shields.io/badge/Add%20repository%20to-Home%20Assistant-41BDF5?logo=home-assistant)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fombi-app)

# Welcome

Ombi is a friendly media request tool for Plex, Emby, and Jellyfin.

This repository packages Ombi as a Home Assistant App with ingress support. It opens from the Home Assistant sidebar and also exposes Ombi on port `3579` for direct local access.

| Service | App |
|---------|:------:|
| Build | [![Builder](https://github.com/Wheemer/ombi-app/actions/workflows/onpush_builder.yaml/badge.svg)](https://github.com/Wheemer/ombi-app/actions/workflows/onpush_builder.yaml) |
| Update | [![Update Ombi](https://github.com/Wheemer/ombi-app/actions/workflows/update_ombi.yaml/badge.svg)](https://github.com/Wheemer/ombi-app/actions/workflows/update_ombi.yaml) |
| Image | `ghcr.io/wheemer/ombi-app` |

# Feature Requests

For Ombi application features, use the Ombi feature board:

[https://features.ombi.io](https://features.ombi.io)

For Home Assistant App issues, use this repository:

[https://github.com/Wheemer/ombi-app/issues](https://github.com/Wheemer/ombi-app/issues)

See [Contributing](CONTRIBUTING.md) for pull requests and testing requirements.

# Features

* Lets your users request movies, TV shows, and music from a clean web interface.
* Works with Plex, Emby, and Jellyfin.
* Connects to download and library tools such as Sonarr, Radarr, Lidarr, and other supported Ombi integrations.
* Supports request approval, user management, notifications, and availability tracking through Ombi.
* Opens inside Home Assistant through ingress.
* Exposes direct local access on port `3579`.
* Builds for `amd64` and `aarch64`.
* Uses the LinuxServer.io Ombi development image.
* Auto-updates from `Ombi-app/Ombi` prereleases to match the development image stream.
* Includes Ombi icon and logo assets for the Home Assistant App store and sidebar.
* Stores Ombi data in Home Assistant's backed-up app config storage.

# Installation

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fombi-app)

Manual repository URL:

```text
https://github.com/Wheemer/ombi-app
```

After adding the repository:

* Install `Ombi App`.
* Start the app.
* Open Ombi App from the Home Assistant sidebar or the app page's `Open Web UI` button.
* Direct local access is available on port `3579`.

# Migrating From The Old Ombi Add-on

If you already used the older alexbelgium Ombi add-on, keep its data until Ombi App has imported it.

Recommended migration:

* Stop the old Ombi add-on.
* Add this repository to Home Assistant.
* Install and start `Ombi App` from this repository.
* Ombi App automatically imports the old `addons_config/ombi` data into its own backed-up app config folder when the new config is empty.
* After Ombi App starts and your settings are present, uninstall the old Ombi add-on.

Alternative migration:

* Stop and uninstall the old Ombi add-on first.
* If Home Assistant asks whether to delete the add-on data, do not delete it.
* Install and start `Ombi App` from this repository.

If the old add-on data is deleted before Ombi App starts, there may be nothing left to import.

# First Setup

Use Ombi's setup wizard to connect Plex, Emby, or Jellyfin first. After that, add your request automation tools such as Sonarr, Radarr, or Lidarr from Ombi's settings.

When ingress is enabled, the app sets Ombi's Base URL to Home Assistant's ingress path. In Ombi settings this looks like `/api/hassio_ingress/...`; leave it that way for sidebar access. The generic Ombi reverse-proxy instructions do not apply to Home Assistant ingress.

Ombi data is stored in the app's own backed-up config folder. If an older install has data in `addons_config/ombi`, the app copies it into the new storage location when `/config` is empty.

Ombi's own application docs are here:

* [Ombi installation docs](https://docs.ombi.app/installation/)

# Configuration

| Option | Default | Description |
|--------|:-------:|-------------|
| `PUID` | `0` | User ID used for Ombi files |
| `PGID` | `0` | Group ID used for Ombi files |
| `env_vars` | `[]` | Extra environment variables passed to Ombi |

Example:

```yaml
PUID: 1000
PGID: 1000
env_vars: []
```

# Updates

The scheduled update workflow checks `Ombi-app/Ombi` prereleases and bumps the app version when Ombi changes. This follows the same stream used by the LinuxServer.io development image.

# Images

Published image:

* `ghcr.io/wheemer/ombi-app`

# Social Preview

Use `.github/social-preview.png` for GitHub's repository social preview image so Home Assistant forum links show Ombi branding.

# Links

* [Ombi](https://github.com/Ombi-app/Ombi)
* [Ombi website](https://ombi.io/)
* [LinuxServer Ombi image](https://github.com/linuxserver/docker-ombi)
* [Original archived app source](https://github.com/alexbelgium/hassio-addons/tree/master/zzz_archived_ombi)

# Donation

[![Paypal](https://img.shields.io/badge/paypal-donate-yellow.svg)](https://www.paypal.me/wheemer)
