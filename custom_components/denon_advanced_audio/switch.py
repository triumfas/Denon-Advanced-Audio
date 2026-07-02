from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import DenonBaseEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        DenonDynamicEqSwitch(coord, entry.entry_id),
        DenonLfcSwitch(coord, entry.entry_id),
        DenonAirplaySwitch(coord, entry.entry_id),
        DenonAutoLipSyncSwitch(coord, entry.entry_id),
        DenonMainZonePowerSwitch(coord, entry.entry_id),
        DenonZone2PowerSwitch(coord, entry.entry_id),
        DenonZone3PowerSwitch(coord, entry.entry_id),
        DenonZone4PowerSwitch(coord, entry.entry_id),
    ])


class DenonDynamicEqSwitch(DenonBaseEntity, SwitchEntity):
    _attr_name = "Dynamic EQ"
    _attr_icon = "mdi:equalizer"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_dynamic_eq"

    @property
    def is_on(self):
        v = self.coordinator.data.get("dynamic_eq")
        return True if v == "1" else False if v == "2" else None

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.async_set_dynamic_eq(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_dynamic_eq(False)
        await self.coordinator.async_request_refresh()


class DenonLfcSwitch(DenonBaseEntity, SwitchEntity):
    _attr_name = "LFC"
    _attr_icon = "mdi:sine-wave"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_lfc"

    @property
    def is_on(self):
        v = self.coordinator.data.get("lfc")
        return True if v == "1" else False if v == "2" else None

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.async_set_lfc(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_lfc(False)
        await self.coordinator.async_request_refresh()


class DenonAirplaySwitch(DenonBaseEntity, SwitchEntity):
    _attr_name = "AirPlay"
    _attr_icon = "mdi:cast-audio"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_airplay"

    @property
    def is_on(self):
        v = self.coordinator.data.get("airplay")
        return True if v == "1" else False if v == "2" else None

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.async_set_airplay("1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_airplay("2")
        await self.coordinator.async_request_refresh()


class DenonAutoLipSyncSwitch(DenonBaseEntity, SwitchEntity):
    _attr_name = "Auto Lip Sync"
    _attr_icon = "mdi:sync"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_auto_lip_sync"

    @property
    def is_on(self):
        v = self.coordinator.data.get("auto_lip_sync")
        return True if v == "1" else False if v == "2" else None

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.async_set_auto_lip_sync("1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_auto_lip_sync("2")
        await self.coordinator.async_request_refresh()


class DenonZonePowerSwitch(DenonBaseEntity, SwitchEntity):
    _attr_icon = "mdi:power"

    _zone_key: str = ""
    _data_key: str = ""
    _default_name: str = ""
    _name_key: str = ""

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_zone_power_{self._name_key}"

    @property
    def name(self):
        zone_names = self.coordinator.data.get("zone_names") or {}
        custom_name = zone_names.get(self._name_key)
        if custom_name and custom_name.strip():
            return f"{custom_name.strip()} Power"
        return self._default_name

    @property
    def is_on(self):
        v = self.coordinator.data.get(self._data_key)
        return True if v == "1" else False if v in ("2", "3") else None

    @property
    def available(self) -> bool:
        base_available = super().available if hasattr(super(), "available") else True
        v = self.coordinator.data.get(self._data_key)
        return bool(base_available) and v is not None

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.async_set_zone_power(self._zone_key, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.async_set_zone_power(self._zone_key, False)
        await self.coordinator.async_request_refresh()


class DenonMainZonePowerSwitch(DenonZonePowerSwitch):
    _zone_key = "MainZone"
    _data_key = "zone_power_main"
    _default_name = "Main Zone Power"
    _name_key = "main"


class DenonZone2PowerSwitch(DenonZonePowerSwitch):
    _zone_key = "Zone2"
    _data_key = "zone_power_zone2"
    _default_name = "Zone 2 Power"
    _name_key = "zone2"


class DenonZone3PowerSwitch(DenonZonePowerSwitch):
    _zone_key = "Zone3"
    _data_key = "zone_power_zone3"
    _default_name = "Zone 3 Power"
    _name_key = "zone3"


class DenonZone4PowerSwitch(DenonZonePowerSwitch):
    _zone_key = "Zone4"
    _data_key = "zone_power_zone4"
    _default_name = "Zone 4 Power"
    _name_key = "zone4"
