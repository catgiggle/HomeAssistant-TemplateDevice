import logging
from functools import partial

from .Constants import *
from .Model.AssignManager import AssignManager
from .Model.StorageBuilder import StorageBuilder
from .Service.AssignService import AssignService
from .Service.StatusService import StatusService
from .Service.UnassignService import UnassignService

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, _config):
    config = _createRootConfig(hass)

    StorageBuilder(config[CONFIG_STORAGE_PATH]).build()
    AssignService(hass).register()
    UnassignService(hass).register()
    StatusService(hass).register()

    hass.bus.async_listen_once('homeassistant_start', partial(_onAfterLoad, config=config))

    return True


async def async_setup_entry(hass, entry):
    _createEntryConfig(hass, entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    _removeEntryConfig(hass, entry)

    return True


def _createRootConfig(hass):
    config = {
        CONFIG_STORAGE_PATH: hass.config.path(f".storage/{DOMAIN}/storage.db"),
    }
    config[CONFIG_ASSIGN_MANAGER] = AssignManager(hass, config[CONFIG_STORAGE_PATH])
    hass.data.setdefault(DOMAIN, config)

    return config


def _createEntryConfig(hass, entry):
    config = {
        CONFIG_DISPLAY_NAME: entry.data.get(CONFIG_DISPLAY_NAME),
        CONFIG_INTERNAL_NAME: entry.data.get(CONFIG_INTERNAL_NAME),
    }
    hass.data[DOMAIN][entry.entry_id] = config

    return config


def _removeEntryConfig(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id)


async def _onAfterLoad(_event, config):
    config[CONFIG_ASSIGN_MANAGER].reload()
