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

    async def _async_validate(
        self, base_url: str, verify_ssl: bool
    ) -> str | None:
        """Probe the AVR. Return an error key, or None if the receiver is valid."""
        from homeassistant.helpers.aiohttp_client import async_get_clientsession

        session = async_get_clientsession(self.hass, verify_ssl=verify_ssl)
        api = DenonAdvancedAudioApi(
            base_url=base_url,
            verify_ssl=verify_ssl,
            session=session,
        )

        try:
            preset = await api.async_get_speaker_preset()
        except Exception as err:
            _LOGGER.exception(
                "Failed to connect to Denon AVR at %s: %s",
                base_url,
                err,
            )
            return "cannot_connect"

        if preset not in ("1", "2"):
            return "invalid_response"
        return None

    @staticmethod
    def _schema(base_url: str, verify_ssl: bool) -> vol.Schema:
        return vol.Schema(
            {
                vol.Required(CONF_BASE_URL, default=base_url): str,
                vol.Required(CONF_VERIFY_SSL, default=verify_ssl): bool,
            }
        )

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ):
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            verify_ssl = user_input[CONF_VERIFY_SSL]

            error = await self._async_validate(base_url, verify_ssl)
            if error:
                errors["base"] = error
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

        return self.async_show_form(
            step_id="user",
            data_schema=self._schema("https://192.168.1.100:10443", DEFAULT_VERIFY_SSL),
            errors=errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict | None = None,
    ):
        """Change the receiver address (e.g. after an IP change), keeping entities."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            verify_ssl = user_input[CONF_VERIFY_SSL]

            if any(
                other.entry_id != entry.entry_id and other.unique_id == base_url
                for other in self._async_current_entries()
            ):
                return self.async_abort(reason="already_configured")

            error = await self._async_validate(base_url, verify_ssl)
            if error:
                errors["base"] = error
            else:
                return self.async_update_reload_and_abort(
                    entry,
                    unique_id=base_url,
                    data_updates={
                        CONF_BASE_URL: base_url,
                        CONF_VERIFY_SSL: verify_ssl,
                    },
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self._schema(
                entry.data[CONF_BASE_URL],
                entry.data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
            ),
            errors=errors,
        )
