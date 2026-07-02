from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import DenonAdvancedAudioApi
from .const import CONF_BASE_URL, CONF_VERIFY_SSL, DOMAIN
from .coordinator import DenonAdvancedAudioCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["select", "switch", "number", "sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = DenonAdvancedAudioApi(
        base_url=entry.data[CONF_BASE_URL],
        verify_ssl=entry.data[CONF_VERIFY_SSL],
    )
    coordinator = DenonAdvancedAudioCoordinator(hass=hass, api=api)
    await coordinator.async_config_entry_first_refresh()

    try:
        coordinator.device_info_data = await api.async_get_device_info()
    except Exception as err:
        _LOGGER.warning("Could not retrieve Denon device info: %s", err)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"api": api, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return ok
