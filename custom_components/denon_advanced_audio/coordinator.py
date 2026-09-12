from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DenonAdvancedAudioApi
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class DenonAdvancedAudioCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: DenonAdvancedAudioApi) -> None:
        self.api = api
        self.device_info_data: dict = {"model": None, "name": None, "mac": None, "sw_version": None}
        # Best-effort memory of which Sound Mode quick-select category (Movie/Music/Game/Pure)
        # is active. The receiver only reports the resolved concrete mode, which is ambiguous
        # for modes shared across categories -- see select.py's SOUND_MODE_* comments. Not
        # persisted across restarts, and self-heals whenever an unambiguous mode is observed.
        self.last_sound_mode_family: str | None = None
        # Best-effort memory of which Pure submode (Direct/Pure Direct/Auto) was last active.
        # Unlike Movie/Music/Game, Pure has no working "jump to category, keep last submode"
        # telnet command -- probing found MSPURE is simply a no-op, not a real category-select
        # -- so the Sound Mode (Quick) Pure button sends whichever submode is remembered here
        # instead. Not persisted across restarts.
        self.last_pure_submode: str | None = None
        super().__init__(
            hass, _LOGGER, name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        try:
            new_data = await self.api.async_get_all()
            if self.data:
                for key, val in new_data.items():
                    if val is None and self.data.get(key) is not None:
                        new_data[key] = self.data[key]
                    elif isinstance(val, dict) and isinstance(self.data.get(key), dict):
                        # Merge nested dictionaries like zone_names
                        for sub_key, sub_val in val.items():
                            if sub_val is None and self.data[key].get(sub_key) is not None:
                                val[sub_key] = self.data[key][sub_key]
            return new_data
        except Exception as err:
            raise UpdateFailed(f"Failed to update: {err}") from err
