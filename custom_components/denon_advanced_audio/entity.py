from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import DenonAdvancedAudioCoordinator


class DenonBaseEntity(CoordinatorEntity[DenonAdvancedAudioCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: DenonAdvancedAudioCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id

    @property
    def device_info(self) -> DeviceInfo:
        d = self.coordinator.device_info_data or {}
        info = DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            manufacturer=MANUFACTURER,
            model=d.get("model") or "AVR",
            name=d.get("name") or "Denon Advanced Audio",
        )
        if d.get("sw_version"):
            info["sw_version"] = d["sw_version"]
        if d.get("mac"):
            info["connections"] = {("mac", d["mac"])}
        return info
