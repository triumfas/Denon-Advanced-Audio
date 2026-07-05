"""Telnet client for Denon AVR now-playing info (port 23)."""
from __future__ import annotations

import asyncio
import logging
from urllib.parse import urlparse

_LOGGER = logging.getLogger(__name__)

AUDIO_CATEGORY = {
    "01": "Analog",
    "02": "PCM",
    "03": "Dolby",
    "04": "DTS",
    "05": "MPEG",
    "06": "AAC",
    "07": "Multi-ch PCM",
    "08": "Auro-3D",
    "09": "HEOS/Streaming",
    "0A": "Multichannel PCM",
    "0B": "MP3",
    "0C": "WMA",
    "0D": "FLAC",
    "0E": "ALAC",
    "0F": "DSD",
}

VIDEO_RES_NORMALIZED = {
    "---": None,
    "480p60": "480p60", "576p50": "576p50",
    "720p50": "720p50", "720p60": "720p60",
    "1080p24": "1080p24", "1080p50": "1080p50", "1080p60": "1080p60",
    "4K24": "2160p24", "4K25": "2160p25", "4K30": "2160p30",
    "4K50": "2160p50", "4K60": "2160p60",
    "8K30": "4320p30", "8K50": "4320p50", "8K60": "4320p60",
}

SD_MAP = {
    "AUTO":     "Auto",
    "HDMI":     "HDMI",
    "DIGITAL":  "Digital (Coax/Opt)",
    "ANALOG":   "Analog",
    "EXT.IN":   "7.1 External",
    "NO":       "No signal",
    "ARC":      "ARC",
    "EARC":     "eARC",
    "7.1IN":    "7.1 Discrete",
}


def extract_host(base_url: str) -> str:
    parsed = urlparse(base_url if "://" in base_url else f"http://{base_url}")
    return parsed.hostname or base_url


def _normalize_rate(raw: str) -> str | None:
    raw = raw.strip().upper()
    if raw in ("", "NONE", "---"):
        return None
    if raw.endswith("K"):
        return f"{raw[:-1]} kHz"
    return raw


def _normalize_sd(raw: str) -> str | None:
    raw = raw.strip().upper()
    if not raw:
        return None
    return SD_MAP.get(raw, raw.title())


class DenonTelnetClient:
    def __init__(self, host: str, port: int = 23, timeout: float = 2.5) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

    async def async_query_now_playing(self) -> dict:
        result = {
            "audio_format_raw": None,
            "audio_signal_code": None,
            "audio_category": None,
            "audio_sample_rate": None,
            "video_input_res": None,
            "video_output_res": None,
            "sound_mode": None,
            "input_signal_type": None,
        }

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout,
            )
        except (asyncio.TimeoutError, OSError) as err:
            _LOGGER.debug("Telnet connect to %s:%s failed: %s",
                          self.host, self.port, err)
            return result

        try:
            cmds = ("MS?\rSSINFAISSIG ?\rSSINFAISFSV ?\r"
                    "SSINFSIGRES ?\rSYSDA ?\rSD?\r")
            writer.write(cmds.encode("ascii"))
            await writer.drain()

            buf = bytearray()
            loop = asyncio.get_event_loop()
            hard_deadline = loop.time() + self.timeout
            while loop.time() < hard_deadline:
                try:
                    chunk = await asyncio.wait_for(reader.read(1024), timeout=0.4)
                    if not chunk:
                        break
                    buf.extend(chunk)
                except asyncio.TimeoutError:
                    if buf:
                        break
                    continue
        except Exception as err:
            _LOGGER.debug("Telnet read error: %s", err)
        finally:
            try:
                writer.close()
                await asyncio.wait_for(writer.wait_closed(), timeout=1.0)
            except Exception:
                pass

        text = buf.decode("ascii", errors="ignore")
        for line in text.split("\r"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("SSINFAISSIG "):
                code = line[len("SSINFAISSIG "):].strip()
                result["audio_signal_code"] = code
                result["audio_category"] = AUDIO_CATEGORY.get(
                    code, f"Unknown ({code})"
                )
            elif line.startswith("SSINFAISFSV "):
                result["audio_sample_rate"] = _normalize_rate(
                    line[len("SSINFAISFSV "):]
                )
            elif line.startswith("SSINFSIGRES "):
                payload = line[len("SSINFSIGRES "):].strip()
                if payload and payload[0] in ("I", "O"):
                    side = payload[0]
                    res = payload[1:].strip()
                    if res == "---" or not res:
                        norm = None
                    else:
                        norm = VIDEO_RES_NORMALIZED.get(res, res)
                    if side == "I":
                        result["video_input_res"] = norm
                    else:
                        result["video_output_res"] = norm
            elif line.startswith("SYSDA "):
                result["audio_format_raw"] = line[len("SYSDA "):].strip()
            elif (line.startswith("MS") and len(line) > 2
                    and not line.startswith(("MSQUICK", "MSSMART"))):
                result["sound_mode"] = line[2:].strip()
            elif line.startswith("SD") and len(line) > 2:
                payload = line[2:].strip()
                if payload and not payload.startswith(("INF", "?")):
                    result["input_signal_type"] = _normalize_sd(payload)

        return result
