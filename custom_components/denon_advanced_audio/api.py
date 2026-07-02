from __future__ import annotations

import asyncio
import re
from urllib.parse import quote, urlparse

import aiohttp

from .const import DEFAULT_TELNET_PORT


class DenonAdvancedAudioApi:
    """API client for Denon Advanced Audio."""

    def __init__(
        self,
        base_url: str,
        verify_ssl: bool,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl

        parsed = urlparse(self.base_url)
        self.telnet_host = parsed.hostname
        self.telnet_port = DEFAULT_TELNET_PORT

    def _ssl_context(self) -> bool:
        if self.verify_ssl:
            return True

        return False

    async def async_get_speaker_preset(self) -> str | None:
        """Get active speaker preset."""
        url = f"{self.base_url}/ajax/speakers/get_config?type=11"

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                url,
                ssl=self._ssl_context(),
            ) as response:
                response.raise_for_status()
                text = await response.text()

        match = re.search(
            r"<SpeakerPreset>(\d+)</SpeakerPreset>",
            text,
        )

        if not match:
            return None

        return match.group(1)

    async def async_set_speaker_preset(
        self,
        preset: str,
    ) -> None:
        """Set active speaker preset."""
        if preset not in ("1", "2"):
            raise ValueError(f"Unsupported speaker preset: {preset}")

        xml_payload = quote(
            f"<SpeakerPreset>{preset}</SpeakerPreset>",
            safe="",
        )

        url = (
            f"{self.base_url}"
            f"/ajax/speakers/set_config"
            f"?type=11&data={xml_payload}"
        )

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                url,
                ssl=self._ssl_context(),
            ) as response:
                response.raise_for_status()

        await asyncio.sleep(0.5)

    async def async_telnet_query(
        self,
        command: str,
        expected_prefix: str,
    ) -> str | None:
        """Query Denon telnet command and return matching response value."""
        if not self.telnet_host:
            return None

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(
                    self.telnet_host,
                    self.telnet_port,
                ),
                timeout=3,
            )

            writer.write(f"{command}\r".encode("ascii"))
            await writer.drain()

            buffer = ""
            end_time = asyncio.get_running_loop().time() + 3

            while asyncio.get_running_loop().time() < end_time:
                try:
                    chunk = await asyncio.wait_for(
                        reader.read(1024),
                        timeout=0.5,
                    )
                except asyncio.TimeoutError:
                    continue

                if not chunk:
                    break

                buffer += chunk.decode(
                    "ascii",
                    errors="ignore",
                )

                lines = re.split(r"[\r\n]+", buffer)

                for line in lines:
                    line = line.strip()

                    if line.startswith(expected_prefix):
                        parts = line.split(maxsplit=1)

                        if len(parts) == 2:
                            return parts[1].strip()

                        return ""

            return None

        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def async_telnet_send(
        self,
        command: str,
    ) -> None:
        """Send Denon telnet command without expecting response."""
        if not self.telnet_host:
            return

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                self.telnet_host,
                self.telnet_port,
            ),
            timeout=3,
        )

        try:
            writer.write(f"{command}\r".encode("ascii"))
            await writer.drain()
            await asyncio.sleep(0.3)

        finally:
            writer.close()
            await writer.wait_closed()

    async def async_get_dynamic_volume(self) -> str | None:
        return await self.async_telnet_query(
            "PSDYNVOL ?",
            "PSDYNVOL",
        )

    async def async_set_dynamic_volume(
        self,
        value: str,
    ) -> None:
        await self.async_telnet_send(f"PSDYNVOL {value}")

    async def async_get_dynamic_eq(self) -> str | None:
        return await self.async_telnet_query(
            "PSDYNEQ ?",
            "PSDYNEQ",
        )

    async def async_set_dynamic_eq(
        self,
        enabled: bool,
    ) -> None:
        await self.async_telnet_send(
            f"PSDYNEQ {'ON' if enabled else 'OFF'}"
        )

    async def async_get_reference_level_offset(self) -> str | None:
        return await self.async_telnet_query(
            "PSREFLEV ?",
            "PSREFLEV",
        )

    async def async_set_reference_level_offset(
        self,
        value: str,
    ) -> None:
        await self.async_telnet_send(f"PSREFLEV {value}")

    async def async_get_lfc(self) -> str | None:
        return await self.async_telnet_query(
            "PSLFC ?",
            "PSLFC",
        )

    async def async_set_lfc(
        self,
        enabled: bool,
    ) -> None:
        await self.async_telnet_send(
            f"PSLFC {'ON' if enabled else 'OFF'}"
        )

    async def async_get_all(self) -> dict:
        """Fetch all supported values."""
        data = {
            "speaker_preset": None,
            "dynamic_volume": None,
            "dynamic_eq": None,
            "reference_level_offset": None,
            "lfc": None,
        }

        data["speaker_preset"] = await self.async_get_speaker_preset()

        for key, method in (
            ("dynamic_volume", self.async_get_dynamic_volume),
            ("dynamic_eq", self.async_get_dynamic_eq),
            ("reference_level_offset", self.async_get_reference_level_offset),
            ("lfc", self.async_get_lfc),
        ):
            try:
                data[key] = await method()
            except Exception:
                data[key] = None

        return data
