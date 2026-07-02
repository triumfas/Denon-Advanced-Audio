from __future__ import annotations

import asyncio
import re
from urllib.parse import quote

import aiohttp


class DenonAdvancedAudioApi:
    def __init__(self, base_url: str, verify_ssl: bool) -> None:
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl

    def _ssl_context(self) -> bool:
        return True if self.verify_ssl else False

    async def _http_get_text(self, url: str) -> str:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.get(url, ssl=self._ssl_context()) as r:
                r.raise_for_status()
                return await r.text()

    async def _ajax_get(self, path: str, xml_type: int) -> str:
        url = f"{self.base_url}/ajax/{path}/get_config?type={xml_type}"
        return await self._http_get_text(url)

    async def _ajax_set(self, path: str, xml_type: int, xml_payload: str) -> None:
        data = quote(xml_payload, safe="")
        url = f"{self.base_url}/ajax/{path}/set_config?type={xml_type}&data={data}"
        await self._http_get_text(url)
        await asyncio.sleep(0.3)

    def _extract(self, text: str, tag: str):
        m = re.search(rf"<{tag}[^>]*>([^<]*)</{tag}>", text)
        return m.group(1) if m else None

    def _extract_display(self, text: str, tag: str):
        m = re.search(rf'<{tag}[^>]*display="(\d)"[^>]*>', text)
        return m.group(1) if m else None

    async def async_get_speaker_preset(self):
        text = await self._ajax_get("speakers", 11)
        return self._extract(text, "SpeakerPreset")

    async def async_set_speaker_preset(self, preset: str):
        await self._ajax_set("speakers", 11, f"<SpeakerPreset>{preset}</SpeakerPreset>")

    async def async_get_restorer(self):
        text = await self._ajax_get("audio", 5)
        return self._extract(text, "Restorer")

    async def async_set_restorer(self, value: str):
        await self._ajax_set("audio", 5, f"<Restorer>{value}</Restorer>")

    async def async_get_volume_config(self) -> dict:
        text = await self._ajax_get("audio", 7)
        return {
            "scale": self._extract(text, "Scale"),
            "limit": self._extract(text, "Limit"),
            "power_on_level": self._extract(text, "PowerOnLevel"),
            "mute_level": self._extract(text, "MuteLevel"),
        }

    async def async_set_volume_scale(self, value: str):
        await self._ajax_set("audio", 7, f"<Scale>{value}</Scale>")

    async def async_set_volume_limit(self, value: str):
        await self._ajax_set("audio", 7, f"<Limit>{value}</Limit>")

    async def async_set_volume_power_on_level(self, value: str):
        await self._ajax_set("audio", 7, f"<PowerOnLevel>{value}</PowerOnLevel>")

    async def async_set_volume_mute_level(self, value: str):
        await self._ajax_set("audio", 7, f"<MuteLevel>{value}</MuteLevel>")

    async def async_get_network_control(self):
        text = await self._ajax_get("network", 5)
        return self._extract(text, "Control")

    async def async_set_network_control(self, value: str):
        await self._ajax_set("network", 5, f"<Control>{value}</Control>")

    async def async_get_airplay(self):
        text = await self._ajax_get("network", 9)
        return self._extract(text, "AirPlay")

    async def async_set_airplay(self, value: str):
        await self._ajax_set("network", 9, f"<AirPlay>{value}</AirPlay>")

    async def async_get_subwoofer_config(self) -> dict:
        text = await self._ajax_get("audio", 3)
        return {
            "sub1": self._extract(text, "SubwooferLevel1"),
            "sub2": self._extract(text, "SubwooferLevel2"),
        }

    async def async_set_subwoofer_level_1(self, value: str):
        await self._ajax_set("audio", 3, f"<SubwooferLevel1>{value}</SubwooferLevel1>")

    async def async_set_subwoofer_level_2(self, value: str):
        await self._ajax_set("audio", 3, f"<SubwooferLevel2>{value}</SubwooferLevel2>")

    async def async_get_audyssey_config(self) -> dict:
        text = await self._ajax_get("audio", 9)
        containment_display = self._extract_display(text, "Containmentamount")
        return {
            "multeq": self._extract(text, "MultEQ"),
            "lrbypass": self._extract(text, "LRBypass"),
            "dynamic_eq": self._extract(text, "DynamicEQ"),
            "reference_level_offset": self._extract(text, "ReferenceLevelOffset"),
            "dynamic_volume": self._extract(text, "DynamicVolume"),
            "lfc": self._extract(text, "AudysseyLFC"),
            "containment_amount": self._extract(text, "Containmentamount"),
            "containment_amount_enabled": (
                containment_display is not None and containment_display != "2"
            ),
        }

    async def async_set_multeq(self, value: str):
        await self._ajax_set("audio", 9, f"<MultEQ>{value}</MultEQ>")

    async def async_set_dynamic_eq(self, on: bool):
        v = "2" if on else "1"
        await self._ajax_set("audio", 9, f"<DynamicEQ>{v}</DynamicEQ>")

    async def async_set_dynamic_volume(self, value: str):
        await self._ajax_set("audio", 9, f"<DynamicVolume>{value}</DynamicVolume>")

    async def async_set_reference_level_offset(self, value: str):
        await self._ajax_set("audio", 9, f"<ReferenceLevelOffset>{value}</ReferenceLevelOffset>")

    async def async_set_lfc(self, on: bool):
        v = "1" if on else "2"
        await self._ajax_set("audio", 9, f"<AudysseyLFC>{v}</AudysseyLFC>")

    async def async_set_containment_amount(self, value: str):
        await self._ajax_set("audio", 9, f"<Containmentamount>{value}</Containmentamount>")

    async def async_get_audio_delay_config(self) -> dict:
        text = await self._ajax_get("audio", 6)
        return {
            "auto_lip_sync": self._extract(text, "AutoLipSync"),
            "adjust": self._extract(text, "Adjust"),
        }

    async def async_set_auto_lip_sync(self, value: str):
        await self._ajax_set("audio", 6, f"<AutoLipSync>{value}</AutoLipSync>")

    async def async_set_audio_delay_adjust(self, value: str):
        await self._ajax_set("audio", 6, f"<Adjust>{value}</Adjust>")

    async def async_get_device_info(self) -> dict:
        result = {"model": None, "name": None, "mac": None, "sw_version": None}
        try:
            text = await self._ajax_get("network", 6)
            default_name = self._extract(text, "DefaultName")
            current_name = self._extract(text, "CurrentName")
            if default_name:
                model = default_name.strip()
                if model.lower().startswith("denon "):
                    model = model[6:].strip()
                result["model"] = model or default_name.strip()
            if current_name and current_name.strip():
                result["name"] = current_name.strip()
            elif default_name:
                result["name"] = default_name.strip()
        except Exception:
            pass
        return result

    async def async_get_all(self) -> dict:
        data = {
            "speaker_preset": None, "restorer": None,
            "network_control": None, "airplay": None,
            "volume_scale": None, "volume_limit": None,
            "volume_power_on_level": None, "volume_mute_level": None,
            "subwoofer_level_1": None, "subwoofer_level_2": None,
            "multeq": None, "lrbypass": None,
            "dynamic_eq": None, "dynamic_volume": None,
            "reference_level_offset": None, "lfc": None,
            "containment_amount": None, "containment_amount_enabled": False,
            "auto_lip_sync": None, "audio_delay_adjust": None,
        }
        try: data["speaker_preset"] = await self.async_get_speaker_preset()
        except Exception: pass
        try: data["restorer"] = await self.async_get_restorer()
        except Exception: pass
        try: data["network_control"] = await self.async_get_network_control()
        except Exception: pass
        try: data["airplay"] = await self.async_get_airplay()
        except Exception: pass
        try:
            vc = await self.async_get_volume_config()
            data["volume_scale"] = vc.get("scale")
            data["volume_limit"] = vc.get("limit")
            data["volume_power_on_level"] = vc.get("power_on_level")
            data["volume_mute_level"] = vc.get("mute_level")
        except Exception: pass
        try:
            sc = await self.async_get_subwoofer_config()
            data["subwoofer_level_1"] = sc.get("sub1")
            data["subwoofer_level_2"] = sc.get("sub2")
        except Exception: pass
        try:
            au = await self.async_get_audyssey_config()
            data["multeq"] = au.get("multeq")
            data["lrbypass"] = au.get("lrbypass")
            data["dynamic_eq"] = au.get("dynamic_eq")
            data["reference_level_offset"] = au.get("reference_level_offset")
            data["dynamic_volume"] = au.get("dynamic_volume")
            data["lfc"] = au.get("lfc")
            data["containment_amount"] = au.get("containment_amount")
            data["containment_amount_enabled"] = au.get("containment_amount_enabled")
        except Exception: pass
        try:
            ad = await self.async_get_audio_delay_config()
            data["auto_lip_sync"] = ad.get("auto_lip_sync")
            data["audio_delay_adjust"] = ad.get("adjust")
        except Exception: pass
        return data
