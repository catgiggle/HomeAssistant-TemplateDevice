import re

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.util import slugify

from .constants import *


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        formData = user_input or {}
        formFields = {}
        formErrors = {}

        formFields[CONFIG_DISPLAY_NAME] = formData.get(CONFIG_DISPLAY_NAME, '').strip()
        formFields[CONFIG_INTERNAL_NAME] = formData.get(CONFIG_INTERNAL_NAME, '').strip()

        normalizedName = None

        if user_input is not None:
            if not re.search(r'[a-zA-Z]', formFields[CONFIG_DISPLAY_NAME]):
                formErrors[CONFIG_DISPLAY_NAME] = 'invalid_display_name'

            if formFields[CONFIG_INTERNAL_NAME]:
                if formFields[CONFIG_INTERNAL_NAME] == slugify(formFields[CONFIG_INTERNAL_NAME]):
                    normalizedName = formFields[CONFIG_INTERNAL_NAME]
                else:
                    formErrors[CONFIG_INTERNAL_NAME] = 'invalid_internal_name'
            else:
                normalizedName = slugify(formFields[CONFIG_DISPLAY_NAME])

            if not formErrors:
                await self.async_set_unique_id(normalizedName)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=formFields[CONFIG_DISPLAY_NAME], data={
                    CONFIG_DISPLAY_NAME: formFields[CONFIG_DISPLAY_NAME],
                    CONFIG_INTERNAL_NAME: normalizedName,
                })

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONFIG_DISPLAY_NAME, default=formFields[CONFIG_DISPLAY_NAME]): cv.string,
                vol.Optional(CONFIG_INTERNAL_NAME, default=formFields[CONFIG_INTERNAL_NAME]): cv.string,
            }),
            errors=formErrors
        )
