from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import DenonBaseEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        DenonSubwooferLevel1(coord, entry.entry_id),
        DenonSubwooferLevel2(coord, entry.entry_id),
        DenonAudioDelayAdjust(coord, entry.entry_id),
        DenonContainmentAmount(coord, entry.entry_id),
    ])


class _DenonSubwooferBase(DenonBaseEntity, NumberEntity):
    _attr_icon = "mdi:speaker"
    _attr_native_min_value = -12.0
    _attr_native_max_value = 12.0
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = "dB"
    _attr_mode = NumberMode.SLIDER

    _data_key: str = ""

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self._data_key)
        if raw is None:
            return None
        try:
            return int(raw) / 10.0
        except (ValueError, TypeError):
            return None


class DenonSubwooferLevel1(_DenonSubwooferBase):
    _attr_name = "Subwoofer Level 1"
    _data_key = "subwoofer_level_1"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_subwoofer_level_1"

    async def async_set_native_value(self, value: float) -> None:
        v = str(int(round(value * 10)))
        await self.coordinator.api.async_set_subwoofer_level_1(v)
        await self.coordinator.async_request_refresh()


class DenonSubwooferLevel2(_DenonSubwooferBase):
    _attr_name = "Subwoofer Level 2"
    _data_key = "subwoofer_level_2"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_subwoofer_level_2"

    async def async_set_native_value(self, value: float) -> None:
        v = str(int(round(value * 10)))
        await self.coordinator.api.async_set_subwoofer_level_2(v)
        await self.coordinator.async_request_refresh()


class DenonAudioDelayAdjust(DenonBaseEntity, NumberEntity):
    _attr_name = "Audio Delay"
    _attr_icon = "mdi:sync-circle"
    _attr_native_min_value = 0
    _attr_native_max_value = 999
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "ms"
    _attr_mode = NumberMode.BOX

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_audio_delay_adjust"

    @property
    def native_value(self):
        raw = self.coordinator.data.get("audio_delay_adjust")
        if raw is None:
            return None
        try:
            return int(raw)
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        v = str(int(round(value)))
        await self.coordinator.api.async_set_audio_delay_adjust(v)
        await self.coordinator.async_request_refresh()


class DenonContainmentAmount(DenonBaseEntity, NumberEntity):
    _attr_name = "Containment Amount"
    _attr_icon = "mdi:waveform"
    _attr_native_min_value = 1
    _attr_native_max_value = 7
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_containment_amount"

    @property
    def available(self) -> bool:
        base_available = super().available if hasattr(super(), "available") else True
        return bool(base_available) and bool(self.coordinator.data.get("containment_amount_enabled"))

    @property
    def native_value(self):
        raw = self.coordinator.data.get("containment_amount")
        if raw is None:
            return None
        try:
            return int(raw)
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        v = str(int(round(value)))
        await self.coordinator.api.async_set_containment_amount(v)
        await self.coordinator.async_request_refresh()
