from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
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
            DenonDynamicEqSwitch(
                coordinator,
                entry.entry_id,
            ),
            DenonLfcSwitch(
                coordinator,
                entry.entry_id,
            ),
        ]
    )


class DenonDynamicEqSwitch(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SwitchEntity,
):
    """Denon Dynamic EQ switch."""

    _attr_name = "Dynamic EQ"
    _attr_icon = "mdi:equalizer"

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_dynamic_eq"

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get("dynamic_eq")

        if value == "ON":
            return True

        if value == "OFF":
            return False

        return None

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.api.async_set_dynamic_eq(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.async_set_dynamic_eq(False)
        await self.coordinator.async_request_refresh()


class DenonLfcSwitch(
    CoordinatorEntity[DenonAdvancedAudioCoordinator],
    SwitchEntity,
):
    """Denon LFC switch."""

    _attr_name = "LFC"
    _attr_icon = "mdi:sine-wave"

    def __init__(
        self,
        coordinator: DenonAdvancedAudioCoordinator,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_lfc"

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get("lfc")

        if value == "ON":
            return True

        if value == "OFF":
            return False

        return None

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.api.async_set_lfc(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.async_set_lfc(False)
        await self.coordinator.async_request_refresh()
