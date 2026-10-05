from homeassistant.helpers import config_validation as cv, device_registry

from .constants import *
from .model.AssignManager import AssignManager
from .model.StorageBuilder import StorageBuilder
from .service.AssignService import AssignService
from .service.StatusService import StatusService
from .service.UnassignService import UnassignService

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass, _config):
    config = await _createRootConfig(hass)

    await StorageBuilder(hass, config[CONFIG_STORAGE_PATH]).async_build()
    AssignService(hass).register()
    UnassignService(hass).register()
    StatusService(hass).register()

    return True


async def async_setup_entry(hass, entry):
    await _createEntryConfig(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await _setupDevice(hass, entry)

    return True


async def async_unload_entry(hass, entry):
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await _unloadDevice(hass, entry)
        await _removeEntryConfig(hass, entry)

        return True

    return False


async def async_remove_entry(hass, entry):
    await _cleanupDevice(hass, entry)


async def _createRootConfig(hass):
    path = hass.config.path(f".storage/{DOMAIN}/storage.db")
    config = {
        CONFIG_STORAGE_PATH: path,
        CONFIG_ASSIGN_MANAGER: AssignManager(hass, path),
    }
    hass.data.setdefault(DOMAIN, config)

    return config


async def _createEntryConfig(hass, entry):
    config = {
        CONFIG_DISPLAY_NAME: entry.data.get(CONFIG_DISPLAY_NAME),
        CONFIG_INTERNAL_NAME: entry.data.get(CONFIG_INTERNAL_NAME),
    }
    hass.data[DOMAIN][entry.entry_id] = config

    return config


async def _removeEntryConfig(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id, None)


async def _setupDevice(hass, entry):
    deviceRegistry = device_registry.async_get(hass)
    deviceEntry = deviceRegistry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})

    if deviceEntry:
        config = hass.data.get(DOMAIN)

        if config and CONFIG_ASSIGN_MANAGER in config:
            await config[CONFIG_ASSIGN_MANAGER].async_device_setup(deviceEntry.id)


async def _unloadDevice(hass, entry):
    deviceRegistry = device_registry.async_get(hass)
    deviceEntry = deviceRegistry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})

    if deviceEntry:
        config = hass.data.get(DOMAIN)

        if config and CONFIG_ASSIGN_MANAGER in config:
            await config[CONFIG_ASSIGN_MANAGER].async_device_unload(deviceEntry.id)


async def _cleanupDevice(hass, entry):
    deviceRegistry = device_registry.async_get(hass)
    deviceEntry = deviceRegistry.async_get_device(identifiers={(DOMAIN, entry.entry_id)})

    if deviceEntry:
        config = hass.data.get(DOMAIN)

        if config and CONFIG_ASSIGN_MANAGER in config:
            await config[CONFIG_ASSIGN_MANAGER].async_device_cleanup(deviceEntry.id)
