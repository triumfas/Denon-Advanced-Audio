from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .entity import DenonBaseEntity
from .telnet import NO_SIGNAL

CONNECTION_MAP = {"1": "Wi-Fi", "2": "Not connected", "3": "Wired (Ethernet)"}
DHCP_MAP = {"1": "On", "2": "Off"}
DIAG_MAP = {"1": "OK", "2": "Failed", "3": "OK"}


def category_from_sysda(sysda):
    if not sysda:
        return None
    s = sysda.upper().strip()
    if not s:
        return None
    if ("ATMOS" in s or "DOLBY" in s or "TRUEHD" in s
            or s == "DD" or s.startswith("DD ") or s.startswith("DD+")):
        return "Dolby"
    if "DTS" in s:
        return "DTS"
    if "PCM" in s:
        if "MULTI" in s:
            return "Multi-ch PCM"
        return "PCM"
    if "ANALOG" in s:
        return "Analog"
    for token in ("MPEG", "AAC", "MP3", "FLAC", "ALAC", "WAV", "DSD", "WMA"):
        if token in s:
            return token
    return sysda.strip().title()


def channels_from_sysda(sysda):
    if not sysda:
        return None
    s = sysda.upper()
    if "ATMOS" in s or "DTS:X" in s or "TRUEHD" in s:
        return "7.1.4"
    if "DD+" in s or "DTS-HD" in s:
        return "5.1"
    if s.startswith("DD") or s == "DTS" or " DD" in s or " DTS" in s:
        return "5.1"
    if "MULTI" in s:
        return "7.1"
    if "PCM" in s:
        return "2.0"
    if "ANALOG" in s:
        return "2.0"
    return None


def compute_output_channels(sound_mode, input_channels, has_sub=True):
    if not sound_mode:
        return input_channels
    m = sound_mode.upper()
    sub = ".1" if has_sub else ".0"

    if m in ("STEREO", "PURE DIRECT"):
        return f"2{sub}"
    if "MCH STEREO" in m or "MULTI CH STEREO" in m:
        return f"7{sub}"
    if m == "DIRECT":
        return input_channels or f"2{sub}"
    if "ATMOS" in m or (input_channels and ".4" in input_channels):
        return f"7{sub}.4"
    if "DTS:X" in m or "NEURAL" in m:
        return f"7{sub}.4"
    if m in ("MOVIE", "MUSIC", "GAME", "AUTO"):
        return input_channels or f"5{sub}"
    return input_channels or f"2{sub}"


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
        DenonAudioFormatSensor(coord, entry.entry_id),
        DenonAudioCategorySensor(coord, entry.entry_id),
        DenonSampleRateSensor(coord, entry.entry_id),
        DenonVideoInputResSensor(coord, entry.entry_id),
        DenonVideoOutputResSensor(coord, entry.entry_id),
        DenonVideoScalingSensor(coord, entry.entry_id),
        DenonSoundModeSensor(coord, entry.entry_id),
        DenonInputSignalTypeSensor(coord, entry.entry_id),
        DenonOutputChannelsSensor(coord, entry.entry_id),
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
            "signal_category_raw": self.coordinator.data.get("audio_category"),
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
        sysda = self.coordinator.data.get("audio_format_raw")
        derived = category_from_sysda(sysda)
        if derived:
            return derived
        return self.coordinator.data.get("audio_category")
    @property
    def extra_state_attributes(self):
        return {
            "signal_code": self.coordinator.data.get("audio_signal_code"),
            "category_from_ssinfaissig": self.coordinator.data.get("audio_category"),
            "sysda_raw": self.coordinator.data.get("audio_format_raw"),
        }


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
        v = self.coordinator.data.get("video_input_res")
        return v if v else NO_SIGNAL


class DenonVideoOutputResSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Video Output Resolution"
    _attr_icon = "mdi:television"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_video_output_res"
    @property
    def native_value(self):
        v = self.coordinator.data.get("video_output_res")
        return v if v else NO_SIGNAL
    @property
    def extra_state_attributes(self):
        vi = self.coordinator.data.get("video_input_res")
        vo = self.coordinator.data.get("video_output_res")
        return {
            "input_res": vi,
            "output_res": vo,
            "passthrough": (vi is not None and vi != NO_SIGNAL and vi == vo),
        }


class DenonVideoScalingSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Video Scaling"
    _attr_icon = "mdi:arrow-expand-vertical"

    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_video_scaling"

    @staticmethod
    def _rank(res):
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
        vi_active = vi not in (None, NO_SIGNAL)
        vo_active = vo not in (None, NO_SIGNAL)
        if not vi_active and vo_active:
            return "TV Audio (ARC)"
        if not vi_active and not vo_active:
            return NO_SIGNAL
        if vi == vo:
            return "Passthrough"
        ri, ro = self._rank(vi), self._rank(vo)
        if ro > ri: return "Upscaling"
        if ro < ri: return "Downscaling"
        return "Different"


class DenonSoundModeSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Sound Mode"
    _attr_icon = "mdi:surround-sound-5-1"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_sound_mode"
    @property
    def native_value(self):
        v = self.coordinator.data.get("sound_mode")
        return v if v else None


class DenonInputSignalTypeSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Input Signal Type"
    _attr_icon = "mdi:cable-data"
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_input_signal_type"
    @property
    def native_value(self):
        v = self.coordinator.data.get("input_signal_type")
        return v if v else None


class DenonOutputChannelsSensor(_DenonNowPlayingSensorBase):
    _attr_name = "Output Channels (Estimated)"
    _attr_icon = "mdi:speaker-multiple"
    _attr_entity_registry_enabled_default = False
    def __init__(self, coord, entry_id):
        super().__init__(coord, entry_id)
        self._attr_unique_id = f"{entry_id}_output_channels"

    def _has_sub(self) -> bool:
        return (
            self.coordinator.data.get("subwoofer_level_1") is not None
            or self.coordinator.data.get("subwoofer_level_2") is not None
        )

    @property
    def native_value(self):
        sysda = self.coordinator.data.get("audio_format_raw")
        source_ch = channels_from_sysda(sysda)
        mode = self.coordinator.data.get("sound_mode")
        return compute_output_channels(mode, source_ch, has_sub=self._has_sub())
    @property
    def extra_state_attributes(self):
        sysda = self.coordinator.data.get("audio_format_raw")
        return {
            "source_channels": channels_from_sysda(sysda),
            "sound_mode": self.coordinator.data.get("sound_mode"),
            "subwoofer_detected": self._has_sub(),
            "is_derived": True,
            "note": "Estimated from format/mode heuristics; not reported by the receiver.",
        }
