from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries

from .api import DenonAdvancedAudioApi
from .const import (
    CONF_BASE_URL,
    CONF_VERIFY_SSL,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class DenonAdvancedAudioConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for Denon Advanced Audio."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ):
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            verify_ssl = user_input[CONF_VERIFY_SSL]

            api = DenonAdvancedAudioApi(
                base_url=base_url,
                verify_ssl=verify_ssl,
            )

            try:
                preset = await api.async_get_speaker_preset()

            except Exception as err:
                _LOGGER.exception(
                    "Failed to connect to Denon AVR at %s: %s",
                    base_url,
                    err,
                )
                errors["base"] = "cannot_connect"

            else:
                if preset not in ("1", "2"):
                    errors["base"] = "invalid_response"

                else:
                    await self.async_set_unique_id(base_url)
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title="Denon Advanced Audio",
                        data={
                            CONF_BASE_URL: base_url,
                            CONF_VERIFY_SSL: verify_ssl,
                        },
                    )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_BASE_URL,
                    default="https://192.168.1.100:10443",
                ): str,
                vol.Required(
                    CONF_VERIFY_SSL,
                    default=DEFAULT_VERIFY_SSL,
                ): bool,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
