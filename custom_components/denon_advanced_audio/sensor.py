from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DenonAdvancedAudioCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities(
        [
            DenonSpeakerPresetSensor(
                coordinator,
                entry.entry_id,
            ),
        ]
    )


class DenonSpeakerPresetSensor(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SensorEntity,
):
    """Denon Speaker Preset state sensor."""

    _attr_name = "Speaker Preset State"
    _attr_icon = "mdi:surround-sound"

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_speaker_preset_state"

    @property
    def native_value(self) -> str:
        preset = self.coordinator.data.get("speaker_preset")

        if preset == "1":
            return "Preset 1"

        if preset == "2":
            return "Preset 2"

        return "Unknown"
