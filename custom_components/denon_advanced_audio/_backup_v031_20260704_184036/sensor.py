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
        # Network / diagnostics (existing)
        DenonIpAddressSensor(coord, entry.entry_id),
        DenonMacEthernetSensor(coord, entry.entry_id),
        DenonMacWifiSensor(coord, entry.entry_id),
        DenonConnectionSensor(coord, entry.entry_id),
        DenonDhcpSensor(coord, entry.entry_id),
        DenonPhysicalConnectionSensor(coord, entry.entry_id),
        DenonRouterAccessSensor(coord, entry.entry_id),
        DenonInternetAccessSensor(coord, entry.entry_id),
        # Now-playing quality (new)
        DenonAudioFormatSensor(coord, entry.entry_id),
        DenonAudioCategorySensor(coord, entry.entry_id),
        DenonSampleRateSensor(coord, entry.entry_id),
        DenonVideoInputResSensor(coord, entry.entry_id),
        DenonVideoOutputResSensor(coord, entry.entry_id),
        DenonVideoScalingSensor(coord, entry.entry_id),
    ])


class _DenonDiagSensorBase(DenonBaseEntity, SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC


# ---------- Network / diagnostics (unchanged) -----------------------------

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


# ---------- Now-playing quality (new) -------------------------------------

class _DenonNowPlayingSensorBase(DenonBaseEntity, SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC


class DenonAudioFormatSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Audio Format"
    _attr_icon = "mdi:dolby"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_audio_format"
    @property
    def native_value(self):
        return self.coordinator.data.get("audio_format_raw")
    @property
    def extra_state_attributes(self):
        return {
            "signal_code": self.coordinator.data.get("audio_signal_code"),
            "signal_category": self.coordinator.data.get("audio_category"),
            "sample_rate": self.coordinator.data.get("audio_sample_rate"),
        }


class DenonAudioCategorySensor(_DenonNowPlayingSensorBase):
    _attr_name = "Audio Category"
    _attr_icon = "mdi:surround-sound"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_audio_category"
    @property
    def native_value(self):
        return self.coordinator.data.get("audio_category")


class DenonSampleRateSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Audio Sample Rate"
    _attr_icon = "mdi:sine-wave"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_audio_sample_rate"
    @property
    def native_value(self):
        return self.coordinator.data.get("audio_sample_rate")


class DenonVideoInputResSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Video Input Resolution"
    _attr_icon = "mdi:video-input-hdmi"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_video_input_res"
    @property
    def native_value(self):
        return self.coordinator.data.get("video_input_res")


class DenonVideoOutputResSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Video Output Resolution"
    _attr_icon = "mdi:television"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_video_output_res"
    @property
    def native_value(self):
        return self.coordinator.data.get("video_output_res")
    @property
    def extra_state_attributes(self):
        vi = self.coordinator.data.get("video_input_res")
        vo = self.coordinator.data.get("video_output_res")
        return {
            "input_res": vi,
            "output_res": vo,
            "passthrough": (vi is not None and vi == vo),
        }


class DenonVideoScalingSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Video Scaling"
    _attr_icon = "mdi:arrow-expand-vertical"
    _attr_options = ["Passthrough", "Upscaling", "Downscaling", "Different"]
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_video_scaling"

    @staticmethod
    def _rank(res: str | None) -> int:
        if not res:
            return 0
        if "480" in res: return 1
        if "576" in res: return 2
        if "720" in res: return 3
        if "1080" in res: return 4
        if "2160" in res or "4K" in res: return 5
        if "4320" in res or "8K" in res: return 6
        return 0

    @property
    def native_value(self):
        vi = self.coordinator.data.get("video_input_res")
        vo = self.coordinator.data.get("video_output_res")
        if vi is None or vo is None:
            return None
        if vi == vo:
            return "Passthrough"
        ri, ro = self._rank(vi), self._rank(vo)
        if ro > ri: return "Upscaling"
        if ro < ri: return "Downscaling"
        return "Different"
