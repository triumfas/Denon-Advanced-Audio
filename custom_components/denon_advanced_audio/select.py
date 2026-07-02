from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import DenonBaseEntity

SPEAKER_PRESET_OPTIONS = ["Preset 1", "Preset 2"]

RESTORER_OPTIONS = ["Off", "Low", "Medium", "High"]
RESTORER_TO = {"Off": "1", "Low": "2", "Medium": "3", "High": "4"}
RESTORER_FROM = {v: k for k, v in RESTORER_TO.items()}

DYNVOL_OPTIONS = ["Off", "Light", "Medium", "Heavy"]
DYNVOL_TO = {"Off": "4", "Light": "3", "Medium": "2", "Heavy": "1"}
DYNVOL_FROM = {v: k for k, v in DYNVOL_TO.items()}

REFLEV_OPTIONS = ["0 dB", "5 dB", "10 dB", "15 dB"]
REFLEV_TO = {"0 dB": "0", "5 dB": "5", "10 dB": "10", "15 dB": "15"}
REFLEV_FROM = {v: k for k, v in REFLEV_TO.items()}

VOLUME_SCALE_OPTIONS = ["0-98", "-79.5dB - 18.0dB"]
VOLUME_SCALE_TO = {"0-98": "1", "-79.5dB - 18.0dB": "2"}
VOLUME_SCALE_FROM = {v: k for k, v in VOLUME_SCALE_TO.items()}

VOLUME_LIMIT_OPTIONS = ["Off"] + [f"-{i}dB" for i in range(20, 0, -1)] + ["0dB"]
MUTE_LEVEL_OPTIONS = ["Full", "-40dB", "-20dB"]
MUTE_LEVEL_TO = {"Full": "1", "-40dB": "2", "-20dB": "3"}
MUTE_LEVEL_FROM = {v: k for k, v in MUTE_LEVEL_TO.items()}

NETWORK_CONTROL_OPTIONS = ["Off", "Always On"]
NETWORK_CONTROL_TO = {"Off": "2", "Always On": "1"}
NETWORK_CONTROL_FROM = {v: k for k, v in NETWORK_CONTROL_TO.items()}

MULTEQ_OPTIONS = ["Reference", "L/R Bypass", "Flat", "Off"]
MULTEQ_TO = {"Reference": "1", "L/R Bypass": "2", "Flat": "3", "Off": "4"}
MULTEQ_FROM = {v: k for k, v in MULTEQ_TO.items()}

ECO_MODE_OPTIONS = ["On", "Auto", "Off"]
ECO_MODE_TO = {"On": "1", "Auto": "2", "Off": "3"}
ECO_MODE_FROM = {v: k for k, v in ECO_MODE_TO.items()}

POWER_ON_DEFAULT_OPTIONS = ["Last", "On", "Auto", "Off"]
POWER_ON_DEFAULT_TO = {"Last": "1", "On": "3", "Auto": "2", "Off": "4"}
POWER_ON_DEFAULT_FROM = {v: k for k, v in POWER_ON_DEFAULT_TO.items()}

OSD_OPTIONS = ["Always On", "Auto", "Off"]
OSD_TO = {"Always On": "1", "Auto": "2", "Off": "3"}
OSD_FROM = {v: k for k, v in OSD_TO.items()}

AS_MAIN_OPTIONS = ["60 min", "30 min", "15 min", "Off"]
AS_MAIN_TO = {"60 min": "1", "30 min": "2", "15 min": "3", "Off": "4"}
AS_MAIN_FROM = {v: k for k, v in AS_MAIN_TO.items()}

AS_Z2_OPTIONS = ["8 hours", "4 hours", "2 hours", "Off"]
AS_Z2_TO = {"8 hours": "1", "4 hours": "2", "2 hours": "3", "Off": "4"}
AS_Z2_FROM = {v: k for k, v in AS_Z2_TO.items()}

PON_OPTIONS = [f"-{i}dB" for i in range(80, 0, -1)] + ["0dB"] + [f"+{i}dB" for i in range(1, 19)]


def _db_option_to_value(option: str):
    if option == "Off":
        return "0"
    if option == "0dB":
        return "80"
    if option.startswith("+"):
        return str(80 + int(option[1:-2]))
    if option.startswith("-"):
        return str(80 - int(option[1:-2]))
    return None


def _value_to_db_option(value, include_off: bool):
    if value is None:
        return None
    try:
        n = int(value)
    except (ValueError, TypeError):
        return None
    if n == 0 and include_off:
        return "Off"
    db = n - 80
    if db == 0:
        return "0dB"
    return f"+{db}dB" if db > 0 else f"{db}dB"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        DenonSpeakerPresetSelect(coord, entry.entry_id),
        DenonRestorerSelect(coord, entry.entry_id),
        DenonDynamicVolumeSelect(coord, entry.entry_id),
        DenonReferenceLevelOffsetSelect(coord, entry.entry_id),
        DenonVolumeScaleSelect(coord, entry.entry_id),
        DenonVolumeLimitSelect(coord, entry.entry_id),
        DenonPowerOnLevelSelect(coord, entry.entry_id),
        DenonMuteLevelSelect(coord, entry.entry_id),
        DenonNetworkControlSelect(coord, entry.entry_id),
        DenonMultEQSelect(coord, entry.entry_id),
        DenonEcoModeSelect(coord, entry.entry_id),
        DenonPowerOnDefaultSelect(coord, entry.entry_id),
        DenonOnScreenDisplaySelect(coord, entry.entry_id),
        DenonAutoStandbyMainSelect(coord, entry.entry_id),
        DenonAutoStandbyZone2Select(coord, entry.entry_id),
    ])


class DenonSpeakerPresetSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Speaker Preset"
    _attr_icon = "mdi:surround-sound"
    _attr_options = SPEAKER_PRESET_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_speaker_preset"

    @property
    def current_option(self):
        p = self.coordinator.data.get("speaker_preset")
        return {"1": "Preset 1", "2": "Preset 2"}.get(p)

    async def async_select_option(self, option):
        await self.coordinator.api.async_set_speaker_preset("1" if option == "Preset 1" else "2")
        await self.coordinator.async_request_refresh()


class DenonRestorerSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Restorer"
    _attr_icon = "mdi:music-circle-outline"
    _attr_options = RESTORER_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_restorer"

    @property
    def current_option(self):
        return RESTORER_FROM.get(self.coordinator.data.get("restorer") or "")

    async def async_select_option(self, option):
        v = RESTORER_TO.get(option)
        if v:
            await self.coordinator.api.async_set_restorer(v)
            await self.coordinator.async_request_refresh()


class DenonDynamicVolumeSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Dynamic Volume"
    _attr_icon = "mdi:volume-high"
    _attr_options = DYNVOL_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_dynamic_volume"

    @property
    def current_option(self):
        return DYNVOL_FROM.get(self.coordinator.data.get("dynamic_volume") or "")

    async def async_select_option(self, option):
        v = DYNVOL_TO.get(option)
        if v:
            await self.coordinator.api.async_set_dynamic_volume(v)
            await self.coordinator.async_request_refresh()


class DenonReferenceLevelOffsetSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Reference Level Offset"
    _attr_icon = "mdi:volume-equal"
    _attr_options = REFLEV_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_reference_level_offset"

    @property
    def current_option(self):
        v = self.coordinator.data.get("reference_level_offset")
        return REFLEV_FROM.get(v or "")

    async def async_select_option(self, option):
        v = REFLEV_TO.get(option)
        if v is not None:
            await self.coordinator.api.async_set_reference_level_offset(v)
            await self.coordinator.async_request_refresh()


class DenonVolumeScaleSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Volume Scale"
    _attr_icon = "mdi:tune-vertical"
    _attr_options = VOLUME_SCALE_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_volume_scale"

    @property
    def current_option(self):
        return VOLUME_SCALE_FROM.get(self.coordinator.data.get("volume_scale") or "")

    async def async_select_option(self, option):
        v = VOLUME_SCALE_TO.get(option)
        if v:
            await self.coordinator.api.async_set_volume_scale(v)
            await self.coordinator.async_request_refresh()


class DenonVolumeLimitSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Volume Limit"
    _attr_icon = "mdi:volume-minus"
    _attr_options = VOLUME_LIMIT_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_volume_limit"

    @property
    def current_option(self):
        return _value_to_db_option(self.coordinator.data.get("volume_limit"), include_off=True)

    async def async_select_option(self, option):
        v = _db_option_to_value(option)
        if v is not None:
            await self.coordinator.api.async_set_volume_limit(v)
            await self.coordinator.async_request_refresh()


class DenonPowerOnLevelSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Power On Level"
    _attr_icon = "mdi:power-standby"
    _attr_options = PON_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_power_on_level"

    @property
    def current_option(self):
        return _value_to_db_option(self.coordinator.data.get("volume_power_on_level"), include_off=False)

    async def async_select_option(self, option):
        v = _db_option_to_value(option)
        if v is not None:
            await self.coordinator.api.async_set_volume_power_on_level(v)
            await self.coordinator.async_request_refresh()


class DenonMuteLevelSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Mute Level"
    _attr_icon = "mdi:volume-mute"
    _attr_options = MUTE_LEVEL_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_mute_level"

    @property
    def current_option(self):
        return MUTE_LEVEL_FROM.get(self.coordinator.data.get("volume_mute_level") or "")

    async def async_select_option(self, option):
        v = MUTE_LEVEL_TO.get(option)
        if v:
            await self.coordinator.api.async_set_volume_mute_level(v)
            await self.coordinator.async_request_refresh()


class DenonNetworkControlSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Network Control"
    _attr_icon = "mdi:lan"
    _attr_options = NETWORK_CONTROL_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_network_control"

    @property
    def current_option(self):
        return NETWORK_CONTROL_FROM.get(self.coordinator.data.get("network_control") or "")

    async def async_select_option(self, option):
        v = NETWORK_CONTROL_TO.get(option)
        if v:
            await self.coordinator.api.async_set_network_control(v)
            await self.coordinator.async_request_refresh()


class DenonMultEQSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "MultEQ XT32"
    _attr_icon = "mdi:tune"
    _attr_options = MULTEQ_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_multeq"

    @property
    def current_option(self):
        return MULTEQ_FROM.get(self.coordinator.data.get("multeq") or "")

    async def async_select_option(self, option):
        v = MULTEQ_TO.get(option)
        if v:
            await self.coordinator.api.async_set_multeq(v)
            await self.coordinator.async_request_refresh()


class DenonEcoModeSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "ECO Mode"
    _attr_icon = "mdi:leaf"
    _attr_options = ECO_MODE_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_eco_mode"

    @property
    def current_option(self):
        return ECO_MODE_FROM.get(self.coordinator.data.get("eco_mode") or "")

    async def async_select_option(self, option):
        v = ECO_MODE_TO.get(option)
        if v:
            await self.coordinator.api.async_set_eco_mode(v)
            await self.coordinator.async_request_refresh()


class DenonPowerOnDefaultSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Power On Default"
    _attr_icon = "mdi:power-standby"
    _attr_options = POWER_ON_DEFAULT_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_power_on_default"

    @property
    def current_option(self):
        return POWER_ON_DEFAULT_FROM.get(self.coordinator.data.get("eco_power_on_default") or "")

    async def async_select_option(self, option):
        v = POWER_ON_DEFAULT_TO.get(option)
        if v:
            await self.coordinator.api.async_set_power_on_default(v)
            await self.coordinator.async_request_refresh()


class DenonOnScreenDisplaySelect(DenonBaseEntity, SelectEntity):
    _attr_name = "On Screen Display"
    _attr_icon = "mdi:monitor"
    _attr_options = OSD_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_on_screen_display"

    @property
    def current_option(self):
        return OSD_FROM.get(self.coordinator.data.get("eco_on_screen_display") or "")

    async def async_select_option(self, option):
        v = OSD_TO.get(option)
        if v:
            await self.coordinator.api.async_set_on_screen_display(v)
            await self.coordinator.async_request_refresh()


class DenonAutoStandbyMainSelect(DenonBaseEntity, SelectEntity):
    _attr_name = "Auto Standby Main Zone"
    _attr_icon = "mdi:sleep"
    _attr_options = AS_MAIN_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_auto_standby_main"

    @property
    def current_option(self):
        return AS_MAIN_FROM.get(self.coordinator.data.get("eco_auto_standby_main") or "")

    async def async_select_option(self, option):
        v = AS_MAIN_TO.get(option)
        if v:
            await self.coordinator.api.async_set_auto_standby_main(v)
            await self.coordinator.async_request_refresh()


class DenonAutoStandbyZone2Select(DenonBaseEntity, SelectEntity):
    _attr_name = "Auto Standby Zone 2"
    _attr_icon = "mdi:sleep"
    _attr_options = AS_Z2_OPTIONS

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_auto_standby_zone2"

    @property
    def current_option(self):
        return AS_Z2_FROM.get(self.coordinator.data.get("eco_auto_standby_zone2") or "")

    async def async_select_option(self, option):
        v = AS_Z2_TO.get(option)
        if v:
            await self.coordinator.api.async_set_auto_standby_zone2(v)
            await self.coordinator.async_request_refresh()
