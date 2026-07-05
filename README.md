## Denon Advanced Audio -- Home Assistant Integration

Home Assistant custom integration exposing **advanced Denon AVR settings** that are not available in the built-in Denon integration -- Speaker Presets, MultEQ XT32, full Audyssey control, Zone Power, ECO / power-saving settings, Front Display brightness, Subwoofer Levels, Volume settings, Audio Delay, Restorer, Network Control, AirPlay, full network diagnostics, and (new in v0.3.0) **live "Now Playing" audio and video quality sensors**.

Developed and tested against **Denon AVR-X3700H**, but should work with any Denon AVR-X or AVC series receiver that exposes the standard /ajax/ web control endpoints.

**Primary transport is HTTP** (Denon web control API). One optional brief telnet query per poll cycle is used to read live audio/video format information that the /ajax/ API does not expose.

### Features

#### Speaker & Audyssey
- **Speaker Preset** -- switch between Preset 1 / Preset 2
- **MultEQ XT32** -- Reference / L/R Bypass / Flat / Off
- **Dynamic EQ** -- on / off switch
- **Dynamic Volume** -- Off / Light / Medium / Heavy
- **Reference Level Offset** -- 0 / 5 / 10 / 15 dB
- **Audyssey LFC** -- on / off switch
- **Containment Amount** -- 1 -- 7 (only available when LFC is On)

#### Volume
- **Volume Scale** -- 0-98 / -79.5 dB ... 18.0 dB
- **Volume Limit** -- Off, -20 dB ... 0 dB
- **Power On Level** -- -80 dB ... +18 dB
- **Mute Level** -- Full / -40 dB / -20 dB

#### Audio
- **Restorer** -- Off / Low / Medium / High
- **Subwoofer Level 1** -- -12.0 dB ... +12.0 dB in 0.5 dB steps
- **Subwoofer Level 2** -- -12.0 dB ... +12.0 dB in 0.5 dB steps
- **Auto Lip Sync** -- on / off
- **Audio Delay** -- 0 -- 999 ms

#### Now Playing Quality *(new in v0.3.0, read-only)*

Live information about the currently playing content, exposed as diagnostic sensors:

- **Audio Format** -- decoded format from the AVR (e.g. `Dolby Audio - DD`, `Dolby Atmos`, `DTS-HD MA`, `DTS:X`, `PCM`)
- **Audio Category** -- signal family (`Dolby`, `DTS`, `PCM`, `Multi-ch PCM`, `Auro-3D`, `HEOS/Streaming`, etc.)
- **Audio Sample Rate** -- `48 kHz`, `96 kHz`, `192 kHz`, etc.
- **Video Input Resolution** -- resolution received from the source device (e.g. `4K50`, `1080p60`)
- **Video Output Resolution** -- resolution sent to the TV (e.g. `4K50`, `1080p60`)
- **Video Scaling** -- `Passthrough` / `Upscaling` / `Downscaling`

These values change automatically as the source device (Blu-ray, streaming box, console) switches formats. Useful for verifying that Atmos, DTS:X, or 4K passthrough is actually reaching the AVR.

#### Zone Power
- **Main Zone Power** -- on / off
- **Zone 2 Power** -- on / off
- **Zone 3 Power** -- auto-hidden if not supported by your AVR
- **Zone 4 Power** -- auto-hidden if not supported by your AVR

Each switch uses the **custom zone name** configured on the AVR (e.g. if Zone 2 is renamed to "Kitchen", the entity appears as "Kitchen Power").

#### ECO / General
- **ECO Mode** -- On / Auto / Off
- **Power On Default** -- Last / On / Auto / Off
- **On Screen Display** -- Always On / Auto / Off
- **Auto Standby Main Zone** -- 60 min / 30 min / 15 min / Off
- **Auto Standby Zone 2** -- 8 hours / 4 hours / 2 hours / Off

#### Front Display
- **Front Display** -- Bright / Dim / Dark / Off (controls the AVR's front panel brightness)

#### Network
- **Network Control** -- Off / Always On
- **AirPlay** -- on / off

#### Network Diagnostics *(read-only)*

Hidden by default in HA's Diagnostic section:

- **IP Address**
- **MAC Address (Ethernet)**
- **MAC Address (Wi-Fi)**
- **Connection Type** -- Wired (Ethernet) / Wi-Fi / Not connected
- **DHCP** -- On / Off
- **Physical Connection** -- OK / Failed
- **Router Access** -- OK / Failed
- **Internet Access** -- OK / Failed

#### Device info
- Model and friendly name are read directly from the AVR at setup
- All entities are grouped under a single Home Assistant device
- Integration branding (icon + logo) available for HA UI and HACS
- Ethernet MAC address is added to the device registry so HA can link with other integrations (e.g. denonavr) that reference the same AVR

### Entities

| Entity | Platform | Notes |
|---|---|---|
| Speaker Preset | select | Preset 1 / Preset 2 |
| MultEQ XT32 | select | Reference / L/R Bypass / Flat / Off |
| Dynamic EQ | switch | on / off |
| Dynamic Volume | select | Off / Light / Medium / Heavy |
| Reference Level Offset | select | 0 -- 15 dB |
| Audyssey LFC | switch | on / off |
| Containment Amount | number | 1 -- 7, only available when LFC is On |
| Volume Scale | select | 0-98 / -79.5 dB ... 18.0 dB |
| Volume Limit | select | Off, -20 dB ... 0 dB |
| Power On Level | select | -80 dB ... +18 dB |
| Mute Level | select | Full / -40 dB / -20 dB |
| Restorer | select | Off / Low / Medium / High |
| Subwoofer Level 1 | number | -12.0 ... +12.0 dB, step 0.5 |
| Subwoofer Level 2 | number | -12.0 ... +12.0 dB, step 0.5 |
| Auto Lip Sync | switch | on / off |
| Audio Delay | number | 0 -- 999 ms |
| Main Zone Power | switch | Uses custom zone name |
| Zone 2 Power | switch | Uses custom zone name |
| Zone 3 Power | switch | Hidden if not supported |
| Zone 4 Power | switch | Hidden if not supported |
| ECO Mode | select | On / Auto / Off |
| Power On Default | select | Last / On / Auto / Off |
| On Screen Display | select | Always On / Auto / Off |
| Auto Standby Main Zone | select | 60 / 30 / 15 min / Off |
| Auto Standby Zone 2 | select | 8 / 4 / 2 hours / Off |
| Front Display | select | Bright / Dim / Dark / Off |
| Network Control | select | Off / Always On |
| AirPlay | switch | on / off |
| Audio Format | sensor | Diagnostic. e.g. `Dolby Atmos`, `PCM` |
| Audio Category | sensor | Diagnostic. `Dolby` / `DTS` / `PCM` / ... |
| Audio Sample Rate | sensor | Diagnostic. e.g. `48 kHz` |
| Video Input Resolution | sensor | Diagnostic. e.g. `4K50` |
| Video Output Resolution | sensor | Diagnostic. e.g. `4K50` |
| Video Scaling | sensor | Diagnostic. `Passthrough` / `Upscaling` / `Downscaling` |
| IP Address | sensor | Diagnostic |
| MAC Address (Ethernet) | sensor | Diagnostic |
| MAC Address (Wi-Fi) | sensor | Diagnostic |
| Connection Type | sensor | Diagnostic |
| DHCP | sensor | Diagnostic |
| Physical Connection | sensor | Diagnostic |
| Router Access | sensor | Diagnostic |
| Internet Access | sensor | Diagnostic |

All entities poll the AVR every 30 seconds by default. Diagnostic sensors are shown in a collapsed section below the main controls in Home Assistant's device page.

### Installation

#### Option 1 -- HACS (recommended)

This integration is a **custom repository**. Add it via HACS as follows:

- In Home Assistant, go to **HACS**
- Open **Integrations**
- Click the three-dot menu in the top right -> **Custom repositories**
- Enter:
  - **Repository**: https://github.com/triumfas/Denon-Advanced-Audio
  - **Category**: Integration
- Click **ADD**
- Close the dialog, search for **Denon Advanced Audio** in the HACS integration list
- Click **Download** on the integration
- Restart Home Assistant

#### Option 2 -- Manual

- Download this repository as a ZIP
- Copy the folder `custom_components/denon_advanced_audio` into your Home Assistant `config/custom_components/` directory
- Restart Home Assistant

Final folder structure:

```
config/
`-- custom_components/
    `-- denon_advanced_audio/
        |-- __init__.py
        |-- api.py
        |-- const.py
        |-- coordinator.py
        |-- config_flow.py
        |-- entity.py
        |-- manifest.json
        |-- number.py
        |-- select.py
        |-- sensor.py
        |-- switch.py
        `-- telnet.py
```

### Configuration

- Go to **Settings -> Devices & services -> Add integration**
- Search for **Denon Advanced Audio**
- Enter:

| Field | Example | Notes |
|---|---|---|
| **Base URL** | https://192.168.1.100:10443 | Denon web control URL (see below) |
| **Verify SSL certificate** | off | Denon uses a self-signed certificate; leave unchecked unless you use a reverse proxy with a valid certificate |

The device name and model are read automatically from the AVR -- no need to enter them manually.

#### Finding your Denon Base URL

Denon AVRs expose a web control interface on ports **8080 (HTTP)** and **10443 (HTTPS)**. Recommended URL formats:

| Setup | Base URL |
|---|---|
| Direct local access (HTTPS) | https://192.168.X.X:10443 |
| Direct local access (HTTP) | http://192.168.X.X:8080 |
| Behind reverse proxy | https://avr.example.com |

You can test by opening the URL in a browser -- you should see the Denon web control page.

#### Telnet requirement for Now Playing sensors *(new in v0.3.0)*

The six Now Playing Quality sensors require **TCP port 23 (telnet)** to be reachable on the AVR (which it is by default on all X-series receivers). The integration opens a very brief telnet connection (approximately 1 second) once per poll cycle, sends four query commands, and immediately closes the socket.

If you also use the **built-in Home Assistant Denon integration** with telnet enabled, occasional collisions may occur because the AVR only accepts one telnet connection at a time. To avoid this, either:

- Disable telnet in the built-in `denonavr` integration (Settings -> Devices & services -> Denon (built-in) -> Configure -> uncheck telnet), **or**
- Increase this integration's scan interval by editing `const.py` (`DEFAULT_SCAN_INTERVAL`) to 60 seconds or more.

The Now Playing sensors will simply return `None` on collision and pick up correct values on the next poll.

### Tested devices

| Model | Status |
|---|---|
| Denon AVR-X3700H | Fully tested |

Should also work on any Denon AVR-X or AVC series receiver that exposes the standard /ajax/ web control endpoints (most 2018+ models). Now Playing sensors require the receiver to support the `SSINFAISSIG`, `SSINFAISFSV`, `SSINFSIGRES`, and `SYSDA` telnet commands (X-series 2018+ receivers).

If your model works (or does not), please open an issue with the model name and firmware version.

### Example Control Card

Want a Denon-style control card in Home Assistant? A ready-to-use Lovelace YAML card is included in `examples/denon_control_panel.yaml`.

The card layout mirrors the Denon Web Control page structure:

- **Zones** -- power toggles for Main Zone / Zone 2 / Zone 3 / Zone 4
- **Speaker Preset** -- Preset 1 / Preset 2
- **Audyssey** -- MultEQ XT32, Dynamic EQ, Dynamic Volume, Reference Level Offset, LFC, Containment Amount
- **Volume** -- Scale, Limit, Power On Level, Mute Level
- **Audio** -- Restorer, Subwoofer 1 and 2 levels, Auto Lip Sync, Audio Delay
- **General & ECO** -- ECO Mode, Power On Default, On Screen Display, Auto Standby
- **Network** -- Network Control, AirPlay

#### Now Playing Quality card *(new in v0.3.0)*

Drop this Markdown card next to your existing dashboard to see live playback quality:

```yaml
type: markdown
title: Now Playing Quality
content: >
  **Audio:** {{ states('sensor.denon_audio_format') }}
  ({{ states('sensor.denon_audio_sample_rate') }})


  **Video:** {{ states('sensor.denon_video_input_resolution') }}
   -> {{ states('sensor.denon_video_output_resolution') }}
  ({{ states('sensor.denon_video_scaling') }})
```

Or an entities card:

```yaml
type: entities
title: Now Playing Quality
entities:
  - entity: sensor.denon_audio_format
    name: Audio format
  - entity: sensor.denon_audio_sample_rate
    name: Sample rate
  - entity: sensor.denon_video_input_resolution
    name: Video input
  - entity: sensor.denon_video_output_resolution
    name: Video output
  - entity: sensor.denon_video_scaling
    name: Scaling
```

#### How to use

- In Home Assistant, go to your **Overview** dashboard
- Click the three-dot menu -> **Edit dashboard**
- Click **+ Add card** -> scroll to the bottom -> **Manual**
- Paste the YAML from `examples/denon_control_panel.yaml`
- Save

The card uses entity IDs with the `denon_*` prefix (e.g. `switch.denon_main_zone_power`). If your entities have different IDs, update the YAML accordingly -- you can find your entities at **Settings -> Devices & services -> Denon Advanced Audio -> Entities**.

### How it works

The integration is primarily **HTTP** -- it uses the Denon web control API, the same endpoints the AVR's built-in web UI uses. As of v0.3.0 a small optional telnet query is added purely to read live audio/video format information (which the /ajax/ API does not expose).

Benefits:

- HTTP calls work over reverse proxies with HTTPS
- Reuses the Home Assistant shared HTTP client session (HTTP Keep-Alive) to minimize connection handshakes
- Automatic safety checks: skips setting changes when all zones are off, preventing receiver API lock-ups
- Telnet is used **read-only**, single-shot, ~1 second per poll (no persistent connection)
- If telnet is unavailable, the Now Playing sensors simply report unknown while everything else keeps working

#### Denon endpoints used

| Feature | Endpoint | Payload |
|---|---|---|
| Speaker Preset | /ajax/speakers/get_config?type=11 / set_config?type=11 | `<SpeakerPreset>X</SpeakerPreset>` |
| Restorer | /ajax/audio/get_config?type=5 / set_config?type=5 | `<Restorer>X</Restorer>` |
| Audio Delay | /ajax/audio/get_config?type=6 / set_config?type=6 | `<AutoLipSync>`, `<Adjust>` |
| Volume settings | /ajax/audio/get_config?type=7 / set_config?type=7 | `<Scale>`, `<Limit>`, `<PowerOnLevel>`, `<MuteLevel>` |
| Subwoofer Levels | /ajax/audio/get_config?type=3 / set_config?type=3 | `<SubwooferLevel1>`, `<SubwooferLevel2>` |
| Audyssey (all) | /ajax/audio/get_config?type=9 / set_config?type=9 | `<MultEQ>`, `<DynamicEQ>`, `<ReferenceLevelOffset>`, `<DynamicVolume>`, `<AudysseyLFC>`, `<Containmentamount>` |
| Zone Power | /ajax/globals/get_config?type=4 / set_config?type=4 | `<MainZone><Power>X</Power></MainZone>`, `<Zone2><Power>X</Power></Zone2>` |
| Zone Names | /ajax/globals/get_config?type=6 | `<MainZone>`, `<Zone2>` friendly names |
| ECO / General | /ajax/general/get_config?type=3 / set_config?type=3 | `<Mode>`, `<PowerOnDefault>`, `<OnScreenDisplay>`, `<AutoStandby>` |
| Front Display | /ajax/general/get_config?type=10 / set_config?type=10 | `<Dimmer>X</Dimmer>` |
| Network Control | /ajax/network/get_config?type=5 / set_config?type=5 | `<Control>X</Control>` |
| Network Information | /ajax/network/get_config?type=2 | IP, MAC (Ethernet/Wi-Fi), Connection, DHCP |
| Network Diagnostics | /ajax/network/get_config?type=7 | Physical Connection, Router Access, Internet Access |
| Device Info | /ajax/network/get_config?type=6 | `<DefaultName>`, `<CurrentName>` |
| AirPlay | /ajax/network/get_config?type=9 / set_config?type=9 | `<AirPlay><Value>X</Value></AirPlay>` |
| Now Playing (telnet :23) | ASCII commands terminated with `\r` | `SSINFAISSIG ?`, `SSINFAISFSV ?`, `SSINFSIGRES ?`, `SYSDA ?` |

#### Value encodings

- **Volume Limit / Power On Level** -- dB + 80 (e.g. -52 dB = 28, 0 dB = 80, +18 dB = 98)
- **Subwoofer Level 1 / 2** -- dB x 10 (e.g. -1.5 dB = -15, +3.0 dB = 30)
- **Zone Power** -- 1 = On, 3 = Off (the same values the Denon UI shows as green/red icons)
- **Boolean settings** -- Denon convention: 1 = On, 2 = Off
- **Audio Signal Category (`SSINFAISSIG`)** -- 2-char hex code (01 = Analog, 02 = PCM, 03 = Dolby, 04 = DTS, 05 = MPEG, 06 = AAC, 07 = Multi-ch PCM, 08 = Auro-3D, 09 = HEOS)
- **Video Resolution (`SSINFSIGRES`)** -- compact tokens like `4K50`, `1080p60`, `---` (no signal)

### Troubleshooting

#### "Cannot connect"
- Verify the Base URL is reachable from a browser on the Home Assistant host
- If using HTTPS with a self-signed certificate, uncheck **Verify SSL certificate**
- Check that the AVR is powered on (the Denon web UI is unavailable in some standby modes)

#### "Connected, but Denon did not return a valid Speaker Preset response"
- Confirm you can open `/ajax/speakers/get_config?type=11` in a browser and get an XML response like `<SpeakerPreset>1</SpeakerPreset>`
- Some very old Denon models may not support this endpoint

#### Some entities show unknown
- The AVR may return empty XML in certain standby modes -- power the AVR on and wait one poll cycle (30 s)
- Check Home Assistant logs for `denon_advanced_audio` warnings

#### Now Playing sensors show unknown
- Confirm TCP port 23 is reachable from Home Assistant: `nc -vz <avr-ip> 23`
- If the built-in `denonavr` HA integration is also enabled with telnet, temporarily disable it to test whether it is holding the socket
- Standby mode disables most telnet responses -- power the AVR on

#### Containment Amount is not adjustable
That is by design. **Containment Amount is only adjustable when Audyssey LFC is On.** Turn on the LFC switch first -- the Containment Amount entity will then become available. When LFC is off, the AVR itself greys the field out.

#### Zone 3 or Zone 4 power switch shows as unavailable
That's expected if your AVR model doesn't support those zones (like the AVR-X3700H, which only has Main Zone and Zone 2). The switches will automatically become available on models that expose Zone 3 / Zone 4.

#### Diagnostic sensors are hidden
The network and Now Playing sensors use HA's Diagnostic category -- they appear in a collapsed **Diagnostic** section at the bottom of the device page. Click to expand.

#### Model or device name is wrong
- Model comes from **Network -> Friendly Name -> Default Name** on the AVR
- Device name comes from **Network -> Friendly Name -> Current Name** (the one you can rename in the AVR web UI or Denon app)

### Branding

Icons for this integration are available in the `brands/` folder:

| File | Size | Purpose |
|---|---|---|
| brands/icon.png | 256 x 256 | Integration icon |
| brands/icon@2x.png | 512 x 512 | High-resolution icon |
| brands/logo.png | 1024 x 256 | Integration logo (banner) |
| brands/logo@2x.png | 2048 x 512 | High-resolution logo |

These icons have been prepared for submission to the https://github.com/home-assistant/brands repository so Home Assistant and HACS can display them automatically once merged.

### Version history

- **v0.3.2** -- Added three more Now Playing sensors: **Sound Mode** (what the AVR is doing with audio -- STEREO, MOVIE, PURE DIRECT, DOLBY ATMOS, etc. via telnet `MS?`), **Input Signal Type** (physical audio path -- eARC / HDMI / Analog / Optical via telnet `SD?`), and **Output Channels** (derived channel layout like 2.1, 5.1, 7.1.4). Completes the input -> processing -> output signal chain picture.
- **v0.3.1** -- Fix Audio Category so it always matches Audio Format (derived from SYSDA instead of the sometimes-stale SSINFAISSIG code). Video sensors now display "No signal" and "TV Audio (ARC)" instead of "Unknown" when no HDMI input is present.
- **v0.3.0** -- Added **Now Playing Quality** sensors: Audio Format, Audio Category, Audio Sample Rate, Video Input Resolution, Video Output Resolution, and Video Scaling. Uses a brief one-shot telnet query per poll cycle to read information that the /ajax/ API does not expose. Backwards-compatible; all previous entities unchanged.
- **v0.2.1** -- Reuses the shared HTTP client session (HTTP Keep-Alive) for faster response times and lower resource usage, and checks zone power before setting changes to prevent receiver API lockups.
- **v0.1.5** -- Front Display brightness control (Bright/Dim/Dark/Off), Network Information sensors (IP, MAC, DHCP, Connection), Network Diagnostics sensors (Physical/Router/Internet), MAC address added to device registry
- **v0.1.4** -- Integration branding added (icon and logo)
- **v0.1.3** -- Zone Power switches (Main + Zone 2/3/4 with custom names), ECO / General settings (ECO Mode, Power On Default, OSD, Auto Standby), icon fixes for subwoofer and AirPlay, integration branding added, removed redundant Speaker Preset State sensor
- **v0.1.2** -- Fix AirPlay state parsing (nested XML)
- **v0.1.1** -- Fix inverted On/Off states for Dynamic EQ, Auto Lip Sync, Network Control
- **v0.1.0** -- 100% HTTP: removed telnet, moved Audyssey to a single web endpoint, added Containment Amount
- **v0.0.9** -- Added Auto Lip Sync switch and Audio Delay number
- **v0.0.8** -- Added MultEQ XT32 select and Subwoofer Level 1 / 2 numbers
- **v0.0.7** -- Added AirPlay switch
- **v0.0.6** -- Added Network Control select
- **v0.0.5** -- Added Volume Scale / Limit / Power On Level / Mute Level; automatic device info
- **v0.0.4** -- Added Restorer select
- **v0.0.1 - v0.0.3** -- Initial Speaker Preset control and Audyssey via telnet

### License

MIT -- see LICENSE

### Credits

- Inspired by the https://github.com/ol-iver/denonavr Python library
- Reverse-engineered from the Denon AVR-X3700H web control interface


