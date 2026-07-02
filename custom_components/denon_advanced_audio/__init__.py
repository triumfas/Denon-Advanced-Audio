from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import DenonAdvancedAudioApi
from .const import (
    CONF_BASE_URL,
    CONF_VERIFY_SSL,
    DOMAIN,
)
from .coordinator import DenonAdvancedAudioCoordinator

PLATFORMS: list[str] = [
    "sensor",
    "select",
    "switch",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Denon Advanced Audio from a config entry."""
    api = DenonAdvancedAudioApi(
        base_url=entry.data[CONF_BASE_URL],
        verify_ssl=entry.data[CONF_VERIFY_SSL],
    )

    coordinator = DenonAdvancedAudioCoordinator(
        hass=hass,
        api=api,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Denon Advanced Audio config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
