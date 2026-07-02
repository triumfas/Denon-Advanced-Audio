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
        super().__init__(
            hass, _LOGGER, name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        try:
            return await self.api.async_get_all()
        except Exception as err:
            raise UpdateFailed(f"Failed to update: {err}") from err
