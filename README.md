# Denon Advanced Audio

Home Assistant custom integration for advanced Denon AVR audio controls.

## Features

- Speaker Preset 1 / 2
- Dynamic Volume
- Dynamic EQ
- Reference Level Offset
- LFC
- UI setup using Config Flow
- Configurable Denon base URL
- Optional SSL certificate verification bypass

## Entities

- `select.speaker_preset`
- `select.dynamic_volume`
- `select.reference_level_offset`
- `switch.dynamic_eq`
- `switch.lfc`
- `sensor.speaker_preset_state`

## Notes

Speaker Preset is read using the Denon web endpoint:

- `/ajax/speakers/get_config?type=11`

Speaker Preset is changed using:

- `/ajax/speakers/set_config?type=11&data=<SpeakerPreset>X</SpeakerPreset>`

Audyssey values are queried using Denon telnet commands.
