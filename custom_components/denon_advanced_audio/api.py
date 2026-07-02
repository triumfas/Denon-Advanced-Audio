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
        m = re.search(r"<AirPlay[^>]*>.*?<Value[^>]*>([^<]+)</Value>.*?</AirPlay>", text, re.DOTALL)
        if m:
            return m.group(1)
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
        v = "1" if on else "2"
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

    async def async_get_zone_power(self) -> dict:
        result = {"main": None, "zone2": None, "zone3": None, "zone4": None}
        try:
            url = f"{self.base_url}/ajax/globals/get_config?type=4"
            text = await self._http_get_text(url)
            m = re.search(r"<MainZone[^>]*>\s*<Power[^>]*>([^<]+)</Power>", text)
            if m: result["main"] = m.group(1)
            m = re.search(r"<Zone2[^>]*>\s*<Power[^>]*>([^<]+)</Power>", text)
            if m: result["zone2"] = m.group(1)
            m = re.search(r"<Zone3[^>]*>\s*<Power[^>]*>([^<]+)</Power>", text)
            if m: result["zone3"] = m.group(1)
            m = re.search(r"<Zone4[^>]*>\s*<Power[^>]*>([^<]+)</Power>", text)
            if m: result["zone4"] = m.group(1)
        except Exception:
            pass
        return result

    async def async_get_zone_names(self) -> dict:
        result = {"main": None, "zone2": None, "zone3": None, "zone4": None}
        try:
            url = f"{self.base_url}/ajax/globals/get_config?type=6"
            text = await self._http_get_text(url)
            m = re.search(r"<MainZone[^>]*>([^<]*)</MainZone>", text)
            if m and m.group(1).strip(): result["main"] = m.group(1).strip()
            m = re.search(r"<Zone2[^>]*>([^<]*)</Zone2>", text)
            if m and m.group(1).strip(): result["zone2"] = m.group(1).strip()
            m = re.search(r"<Zone3[^>]*>([^<]*)</Zone3>", text)
            if m and m.group(1).strip(): result["zone3"] = m.group(1).strip()
            m = re.search(r"<Zone4[^>]*>([^<]*)</Zone4>", text)
            if m and m.group(1).strip(): result["zone4"] = m.group(1).strip()
        except Exception:
            pass
        return result

    async def async_set_zone_power(self, zone_key: str, on: bool):
        v = "1" if on else "3"
        payload = f"<{zone_key}><Power>{v}</Power></{zone_key}>"
        data = quote(payload, safe="")
        url = f"{self.base_url}/ajax/globals/set_config?type=4&data={data}"
        await self._http_get_text(url)
        await asyncio.sleep(0.3)

    async def async_get_eco_config(self) -> dict:
        result = {"mode": None, "power_on_default": None, "on_screen_display": None,
                  "auto_standby_main": None, "auto_standby_zone2": None}
        try:
            text = await self._ajax_get("general", 3)
            result["mode"] = self._extract(text, "Mode")
            result["power_on_default"] = self._extract(text, "PowerOnDefault")
            result["on_screen_display"] = self._extract(text, "OnScreenDisplay")
            m = re.search(r"<AutoStandby[^>]*>(.*?)</AutoStandby>", text, re.DOTALL)
            if m:
                inner = m.group(1)
                mm = re.search(r"<MainZone[^>]*>([^<]+)</MainZone>", inner)
                if mm: result["auto_standby_main"] = mm.group(1)
                mz = re.search(r"<Zone2[^>]*>([^<]+)</Zone2>", inner)
                if mz: result["auto_standby_zone2"] = mz.group(1)
        except Exception:
            pass
        return result

    async def async_set_eco_mode(self, value: str):
        await self._ajax_set("general", 3, f"<Mode>{value}</Mode>")

    async def async_set_power_on_default(self, value: str):
        await self._ajax_set("general", 3, f"<PowerOnDefault>{value}</PowerOnDefault>")

    async def async_set_on_screen_display(self, value: str):
        await self._ajax_set("general", 3, f"<OnScreenDisplay>{value}</OnScreenDisplay>")

    async def async_set_auto_standby_main(self, value: str):
        await self._ajax_set("general", 3, f"<AutoStandby><MainZone>{value}</MainZone></AutoStandby>")

    async def async_set_auto_standby_zone2(self, value: str):
        await self._ajax_set("general", 3, f"<AutoStandby><Zone2>{value}</Zone2></AutoStandby>")

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
            "zone_power_main": None, "zone_power_zone2": None,
            "zone_power_zone3": None, "zone_power_zone4": None,
            "zone_names": {"main": None, "zone2": None, "zone3": None, "zone4": None},
            "eco_mode": None, "eco_power_on_default": None, "eco_on_screen_display": None,
            "eco_auto_standby_main": None, "eco_auto_standby_zone2": None,
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
        try:
            zp = await self.async_get_zone_power()
            data["zone_power_main"] = zp.get("main")
            data["zone_power_zone2"] = zp.get("zone2")
            data["zone_power_zone3"] = zp.get("zone3")
            data["zone_power_zone4"] = zp.get("zone4")
        except Exception: pass
        try:
            data["zone_names"] = await self.async_get_zone_names()
        except Exception:
            data["zone_names"] = {"main": None, "zone2": None, "zone3": None, "zone4": None}
        try:
            eco = await self.async_get_eco_config()
            data["eco_mode"] = eco.get("mode")
            data["eco_power_on_default"] = eco.get("power_on_default")
            data["eco_on_screen_display"] = eco.get("on_screen_display")
            data["eco_auto_standby_main"] = eco.get("auto_standby_main")
            data["eco_auto_standby_zone2"] = eco.get("auto_standby_zone2")
        except Exception: pass
        return data
