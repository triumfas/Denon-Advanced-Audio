from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import DenonBaseEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([DenonSpeakerPresetSensor(coord, entry.entry_id)])


class DenonSpeakerPresetSensor(DenonBaseEntity, SensorEntity):
    _attr_name = "Speaker Preset State"
    _attr_icon = "mdi:surround-sound"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_speaker_preset_state"

    @property
    def native_value(self):
        return {"1": "Preset 1", "2": "Preset 2"}.get(self.coordinator.data.get("speaker_preset"), "Unknown")
