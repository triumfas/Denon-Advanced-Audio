# Denon Advanced Audio — Home Assistant Integration

Home Assistant custom integration exposing **advanced Denon AVR settings** that are not available in the built-in Denon integration — Speaker Presets, MultEQ XT32, full Audyssey control, Zone Power, ECO / power-saving settings, Subwoofer Levels, Volume settings, Audio Delay, Restorer, Network Control, AirPlay, and more.

Developed and tested against **Denon AVR-X3700H**, but should work with any Denon AVR-X or AVC series receiver that exposes the standard `/ajax/` web control endpoints.

**As of v0.1.0, the integration is 100% HTTP.** No telnet, no port 23, no conflicts with the built-in `denonavr` integration.

---

## Features

### Speaker & Audyssey

- **Speaker Preset** — switch between Preset 1 / Preset 2
- **MultEQ XT32** — Reference / L/R Bypass / Flat / Off
- **Dynamic EQ** — on / off switch
- **Dynamic Volume** — Off / Light / Medium / Heavy
- **Reference Level Offset** — 0 / 5 / 10 / 15 dB
- **Audyssey LFC** — on / off switch
- **Containment Amount** — 1 – 7 (only available when LFC is On)

### Volume

- **Volume Scale** — 0-98 / -79.5 dB … 18.0 dB
- **Volume Limit** — Off, -20 dB … 0 dB
- **Power On Level** — -80 dB … +18 dB
- **Mute Level** — Full / -40 dB / -20 dB

### Audio

- **Restorer** — Off / Low / Medium / High
- **Subwoofer Level 1** — -12.0 dB … +12.0 dB in 0.5 dB steps
- **Subwoofer Level 2** — -12.0 dB … +12.0 dB in 0.5 dB steps
- **Auto Lip Sync** — on / off
- **Audio Delay** — 0 – 999 ms

### Zone Power *(new in v0.1.3)*

- **Main Zone Power** — on / off
- **Zone 2 Power** — on / off
- **Zone 3 Power** — auto-hidden if not supported by your AVR
- **Zone 4 Power** — auto-hidden if not supported by your AVR

Each switch uses the **custom zone name** configured on the AVR (e.g. if Zone 2 is renamed to "Kitchen", the entity appears as "Kitchen Power").

### ECO / General *(new in v0.1.3)*

- **ECO Mode** — On / Auto / Off
- **Power On Default** — Last / On / Auto / Off
- **On Screen Display** — Always On / Auto / Off
- **Auto Standby Main Zone** — 60 min / 30 min / 15 min / Off
- **Auto Standby Zone 2** — 8 hours / 4 hours / 2 hours / Off

### Network

- **Network Control** — Off / Always On
- **AirPlay** — on / off

### Device info

- Model and friendly name are read directly from the AVR at setup
- All entities are grouped under a single Home Assistant device

---

## Entities

| Entity | Platform | Notes |
|---|---|---|
| Speaker Preset | select | Preset 1 / Preset 2 |
| MultEQ XT32 | select | Reference / L/R Bypass / Flat / Off |
| Dynamic EQ | switch | on / off |
| Dynamic Volume | select | Off / Light / Medium / Heavy |
| Reference Level Offset | select | 0 – 15 dB |
| Audyssey LFC | switch | on / off |
| Containment Amount | number | 1 – 7, only available when LFC is On |
| Volume Scale | select | 0-98 / -79.5 dB … 18.0 dB |
| Volume Limit | select | Off, -20 dB … 0 dB |
| Power On Level | select | -80 dB … +18 dB |
| Mute Level | select | Full / -40 dB / -20 dB |
| Restorer | select | Off / Low / Medium / High |
| Subwoofer Level 1 | number | -12.0 … +12.0 dB, step 0.5 |
| Subwoofer Level 2 | number | -12.0 … +12.0 dB, step 0.5 |
| Auto Lip Sync | switch | on / off |
| Audio Delay | number | 0 – 999 ms |
| Main Zone Power | switch | Uses custom zone name |
| Zone 2 Power | switch | Uses custom zone name |
| Zone 3 Power | switch | Hidden if not supported |
| Zone 4 Power | switch | Hidden if not supported |
| ECO Mode | select | On / Auto / Off |
| Power On Default | select | Last / On / Auto / Off |
| On Screen Display | select | Always On / Auto / Off |
| Auto Standby Main Zone | select | 60 / 30 / 15 min / Off |
| Auto Standby Zone 2 | select | 8 / 4 / 2 hours / Off |
| Network Control | select | Off / Always On |
| AirPlay | switch | on / off |

All entities poll the AVR every 30 seconds by default.

---

## Installation

### Option 1 — HACS (recommended)

This integration is a **custom repository**. Add it via HACS as follows:

1. In Home Assistant, go to **HACS**
2. Open **Integrations**
3. Click the three-dot menu in the top right → **Custom repositories**
4. Enter:
   - **Repository**: `https://github.com/triumfas/Denon-Advanced-Audio`
   - **Category**: `Integration`
5. Click **ADD**
6. Close the dialog, search for **Denon Advanced Audio** in the HACS integration list
7. Click **Download** on the integration
8. Restart Home Assistant

### Option 2 — Manual

1. Download this repository as a ZIP
2. Copy the folder `custom_components/denon_advanced_audio` into your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

Final folder structure:

```
config/
└── custom_components/
    └── denon_advanced_audio/
        ├── __init__.py
        ├── api.py
        ├── const.py
        ├── coordinator.py
        ├── config_flow.py
        ├── entity.py
        ├── manifest.json
        ├── number.py
        ├── select.py
        ├── sensor.py
        └── switch.py
```

---

## Configuration

1. Go to **Settings → Devices & services → Add integration**
2. Search for **Denon Advanced Audio**
3. Enter:

| Field | Example | Notes |
|---|---|---|
| **Base URL** | `https://192.168.1.100:10443` | Denon web control URL (see below) |
| **Verify SSL certificate** | off | Denon uses a self-signed certificate; leave unchecked unless you use a reverse proxy with a valid certificate |

The device name and model are read automatically from the AVR — no need to enter them manually.

### Finding your Denon Base URL

Denon AVRs expose a web control interface on ports **8080 (HTTP)** and **10443 (HTTPS)**. Recommended URL formats:

| Setup | Base URL |
|---|---|
| Direct local access (HTTPS) | `https://192.168.X.X:10443` |
| Direct local access (HTTP) | `http://192.168.X.X:8080` |
| Behind reverse proxy | `https://avr.example.com` |

You can test by opening the URL in a browser — you should see the Denon web control page.

---

## Tested devices

| Model | Status |
|---|---|
| Denon AVR-X3700H | Fully tested |

Should also work on any Denon AVR-X or AVC series receiver that exposes the standard `/ajax/` web control endpoints (most 2018+ models).

If your model works (or does not), please open an issue with the model name and firmware version.

---

## How it works

As of v0.1.0, the integration is **100% HTTP** — it uses only the Denon web control API, the same endpoints the AVR's built-in web UI uses.

Benefits:

- No TCP port 23 (telnet) required
- Works cleanly alongside the built-in `denonavr` integration (no telnet conflict)
- Works over reverse proxies with HTTPS
- Faster and more reliable

### Denon endpoints used

| Feature | Endpoint | Payload |
|---|---|---|
| Speaker Preset | `/ajax/speakers/get_config?type=11` / `set_config?type=11` | `<SpeakerPreset>X</SpeakerPreset>` |
| Restorer | `/ajax/audio/get_config?type=5` / `set_config?type=5` | `<Restorer>X</Restorer>` |
| Audio Delay | `/ajax/audio/get_config?type=6` / `set_config?type=6` | `<AutoLipSync>`, `<Adjust>` |
| Volume settings | `/ajax/audio/get_config?type=7` / `set_config?type=7` | `<Scale>`, `<Limit>`, `<PowerOnLevel>`, `<MuteLevel>` |
| Subwoofer Levels | `/ajax/audio/get_config?type=3` / `set_config?type=3` | `<SubwooferLevel1>`, `<SubwooferLevel2>` |
| Audyssey (all) | `/ajax/audio/get_config?type=9` / `set_config?type=9` | `<MultEQ>`, `<DynamicEQ>`, `<ReferenceLevelOffset>`, `<DynamicVolume>`, `<AudysseyLFC>`, `<Containmentamount>` |
| Zone Power | `/ajax/globals/get_config?type=4` / `set_config?type=4` | `<MainZone><Power>X</Power></MainZone>`, `<Zone2><Power>X</Power></Zone2>` |
| Zone Names | `/ajax/globals/get_config?type=6` | `<MainZone>`, `<Zone2>` friendly names |
| ECO / General | `/ajax/general/get_config?type=3` / `set_config?type=3` | `<Mode>`, `<PowerOnDefault>`, `<OnScreenDisplay>`, `<AutoStandby>` |
| Network Control | `/ajax/network/get_config?type=5` / `set_config?type=5` | `<Control>X</Control>` |
| Device Info | `/ajax/network/get_config?type=6` | `<DefaultName>`, `<CurrentName>` |
| AirPlay | `/ajax/network/get_config?type=9` / `set_config?type=9` | `<AirPlay><Value>X</Value></AirPlay>` |

### Value encodings

- **Volume Limit / Power On Level** → `dB + 80` (e.g. `-52 dB` = `28`, `0 dB` = `80`, `+18 dB` = `98`)
- **Subwoofer Level 1 / 2** → `dB × 10` (e.g. `-1.5 dB` = `-15`, `+3.0 dB` = `30`)
- **Zone Power** → `1` = On, `3` = Off (the same values the Denon UI shows as green/red icons)
- **Boolean settings** — Denon convention: `1` = On, `2` = Off

---

## Troubleshooting

### "Cannot connect"

- Verify the Base URL is reachable from a browser on the Home Assistant host
- If using HTTPS with a self-signed certificate, uncheck **Verify SSL certificate**
- Check that the AVR is powered on (the Denon web UI is unavailable in some standby modes)

### "Connected, but Denon did not return a valid Speaker Preset response"

- Confirm you can open `/ajax/speakers/get_config?type=11` in a browser and get an XML response like `<SpeakerPreset>1</SpeakerPreset>`
- Some very old Denon models may not support this endpoint

### Some entities show `unknown`

- The AVR may return empty XML in certain standby modes — power the AVR on and wait one poll cycle (30 s)
- Check Home Assistant logs for `denon_advanced_audio` warnings

### Containment Amount is not adjustable

That is by design. **Containment Amount is only adjustable when Audyssey LFC is On.** Turn on the LFC switch first — the Containment Amount entity will then become available. When LFC is off, the AVR itself greys the field out.

### Zone 3 or Zone 4 power switch shows as unavailable

That's expected if your AVR model doesn't support those zones (like the AVR-X3700H, which only has Main Zone and Zone 2). The switches will automatically become available on models that expose Zone 3 / Zone 4.

### Model or device name is wrong

- Model comes from **Network → Friendly Name → Default Name** on the AVR
- Device name comes from **Network → Friendly Name → Current Name** (the one you can rename in the AVR web UI or Denon app)

---

## Version history

- **v0.1.4** -- Integration branding added (icon and logo submitted to home-assistant/brands)
- **v0.1.3** — Zone Power switches (Main + Zone 2/3/4 with custom names), ECO / General settings (ECO Mode, Power On Default, OSD, Auto Standby), icon fixes for subwoofer and AirPlay
- **v0.1.2** — Fix AirPlay state parsing (nested XML)
- **v0.1.1** — Fix inverted On/Off states for Dynamic EQ, Auto Lip Sync, Network Control
- **v0.1.0** — 100% HTTP: removed telnet, moved Audyssey to a single web endpoint, added Containment Amount
- **v0.0.9** — Added Auto Lip Sync switch and Audio Delay number
- **v0.0.8** — Added MultEQ XT32 select and Subwoofer Level 1 / 2 numbers
- **v0.0.7** — Added AirPlay switch
- **v0.0.6** — Added Network Control select
- **v0.0.5** — Added Volume Scale / Limit / Power On Level / Mute Level; automatic device info
- **v0.0.4** — Added Restorer select
- **v0.0.1 – v0.0.3** — Initial Speaker Preset control and Audyssey via telnet

---

## License

MIT — see [LICENSE](LICENSE)

## Credits

- Inspired by the [denonavr](https://github.com/ol-iver/denonavr) Python library
- Reverse-engineered from the Denon AVR-X3700H web control interface




