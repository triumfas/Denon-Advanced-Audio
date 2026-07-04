from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import DenonBaseEntity


CONNECTION_MAP = {"1": "Wi-Fi", "2": "Not connected", "3": "Wired (Ethernet)"}
DHCP_MAP = {"1": "On", "2": "Off"}
DIAG_MAP = {"1": "OK", "2": "Failed", "3": "OK"}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coord = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        DenonIpAddressSensor(coord, entry.entry_id),
        DenonMacEthernetSensor(coord, entry.entry_id),
        DenonMacWifiSensor(coord, entry.entry_id),
        DenonConnectionSensor(coord, entry.entry_id),
        DenonDhcpSensor(coord, entry.entry_id),
        DenonPhysicalConnectionSensor(coord, entry.entry_id),
        DenonRouterAccessSensor(coord, entry.entry_id),
        DenonInternetAccessSensor(coord, entry.entry_id),
    ])


class _DenonDiagSensorBase(DenonBaseEntity, SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC


class DenonIpAddressSensor(_DenonDiagSensorBase):
    _attr_name = "IP Address"
    _attr_icon = "mdi:ip-network"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_ip_address"

    @property
    def native_value(self):
        return self.coordinator.data.get("network_ip")


class DenonMacEthernetSensor(_DenonDiagSensorBase):
    _attr_name = "MAC Address (Ethernet)"
    _attr_icon = "mdi:ethernet"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_mac_ethernet"

    @property
    def native_value(self):
        mac = self.coordinator.data.get("network_mac_ethernet")
        if mac and len(mac) == 12:
            mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
        return mac


class DenonMacWifiSensor(_DenonDiagSensorBase):
    _attr_name = "MAC Address (Wi-Fi)"
    _attr_icon = "mdi:wifi"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_mac_wifi"

    @property
    def native_value(self):
        mac = self.coordinator.data.get("network_mac_wifi")
        if mac and len(mac) == 12:
            mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
        return mac


class DenonConnectionSensor(_DenonDiagSensorBase):
    _attr_name = "Connection Type"
    _attr_icon = "mdi:lan-connect"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_connection_type"

    @property
    def native_value(self):
        v = self.coordinator.data.get("network_connection")
        return CONNECTION_MAP.get(v, v)


class DenonDhcpSensor(_DenonDiagSensorBase):
    _attr_name = "DHCP"
    _attr_icon = "mdi:ip-network-outline"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_dhcp"

    @property
    def native_value(self):
        v = self.coordinator.data.get("network_dhcp")
        return DHCP_MAP.get(v, v)


class DenonPhysicalConnectionSensor(_DenonDiagSensorBase):
    _attr_name = "Physical Connection"
    _attr_icon = "mdi:ethernet-cable"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_physical_connection"

    @property
    def native_value(self):
        v = self.coordinator.data.get("diag_physical")
        return DIAG_MAP.get(v, v)


class DenonRouterAccessSensor(_DenonDiagSensorBase):
    _attr_name = "Router Access"
    _attr_icon = "mdi:router-wireless"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_router_access"

    @property
    def native_value(self):
        v = self.coordinator.data.get("diag_router")
        return DIAG_MAP.get(v, v)


class DenonInternetAccessSensor(_DenonDiagSensorBase):
    _attr_name = "Internet Access"
    _attr_icon = "mdi:web"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_internet_access"

    @property
    def native_value(self):
        v = self.coordinator.data.get("diag_internet")
        return DIAG_MAP.get(v, v)
