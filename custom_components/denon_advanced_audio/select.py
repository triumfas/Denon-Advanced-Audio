from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DenonAdvancedAudioCoordinator


SPEAKER_PRESET_OPTIONS = [
    "Preset 1",
    "Preset 2",
]

DYNAMIC_VOLUME_OPTIONS = [
    "Off",
    "Light",
    "Medium",
    "Heavy",
]

DYNAMIC_VOLUME_TO_DENON = {
    "Off": "OFF",
    "Light": "LIT",
    "Medium": "MED",
    "Heavy": "HEV",
}

DYNAMIC_VOLUME_FROM_DENON = {
    "OFF": "Off",
    "LIT": "Light",
    "MED": "Medium",
    "HEV": "Heavy",
}

REFERENCE_LEVEL_OPTIONS = [
    "0 dB",
    "5 dB",
    "10 dB",
    "15 dB",
]

REFERENCE_LEVEL_TO_DENON = {
    "0 dB": "0",
    "5 dB": "5",
    "10 dB": "10",
    "15 dB": "15",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities(
        [
            DenonSpeakerPresetSelect(
                coordinator,
                entry.entry_id,
            ),
            DenonDynamicVolumeSelect(
                coordinator,
                entry.entry_id,
            ),
            DenonReferenceLevelOffsetSelect(
                coordinator,
                entry.entry_id,
            ),
        ]
    )


class DenonSpeakerPresetSelect(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SelectEntity,
):
    """Denon Speaker Preset selector."""

    _attr_name = "Speaker Preset"
    _attr_icon = "mdi:surround-sound"
    _attr_options = SPEAKER_PRESET_OPTIONS

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_speaker_preset"

    @property
    def current_option(self) -> str | None:
        preset = self.coordinator.data.get("speaker_preset")

        if preset == "1":
            return "Preset 1"

        if preset == "2":
            return "Preset 2"

        return None

    async def async_select_option(
        self,
        option: str,
    ) -> None:
        if option == "Preset 1":
            await self.coordinator.api.async_set_speaker_preset("1")

        elif option == "Preset 2":
            await self.coordinator.api.async_set_speaker_preset("2")

        await self.coordinator.async_request_refresh()


class DenonDynamicVolumeSelect(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SelectEntity,
):
    """Denon Dynamic Volume selector."""

    _attr_name = "Dynamic Volume"
    _attr_icon = "mdi:volume-high"
    _attr_options = DYNAMIC_VOLUME_OPTIONS

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_dynamic_volume"

    @property
    def current_option(self) -> str | None:
        value = self.coordinator.data.get("dynamic_volume")

        if value is None:
            return None

        return DYNAMIC_VOLUME_FROM_DENON.get(value)

    async def async_select_option(
        self,
        option: str,
    ) -> None:
        denon_value = DYNAMIC_VOLUME_TO_DENON.get(option)

        if denon_value is None:
            return

        await self.coordinator.api.async_set_dynamic_volume(
            denon_value,
        )

        await self.coordinator.async_request_refresh()


class DenonReferenceLevelOffsetSelect(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SelectEntity,
):
    """Denon Reference Level Offset selector."""

    _attr_name = "Reference Level Offset"
    _attr_icon = "mdi:volume-equal"
    _attr_options = REFERENCE_LEVEL_OPTIONS

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_reference_level_offset"

    @property
    def current_option(self) -> str | None:
        value = self.coordinator.data.get("reference_level_offset")

        if value is None:
            return None

        return f"{value} dB"

    async def async_select_option(
        self,
        option: str,
    ) -> None:
        denon_value = REFERENCE_LEVEL_TO_DENON.get(option)

        if denon_value is None:
            return

        await self.coordinator.api.async_set_reference_level_offset(
            denon_value,
        )

        await self.coordinator.async_request_refresh()
