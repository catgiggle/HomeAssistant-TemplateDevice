from homeassistant.helpers import config_validation as cv

from .constants import *
from .entry.DeviceEntry import DeviceEntry
from .entry.DiagnosticsEntry import DiagnosticsEntry
from .model.AssignManager import AssignManager
from .model.DiagnosticCoordinator import DiagnosticCoordinator
from .model.StorageBuilder import StorageBuilder
from .service.AssignService import AssignService
from .service.ClearService import ClearService
from .service.StatusService import StatusService
from .service.UnassignService import UnassignService

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass, _config):
    config = await _createRootConfig(hass)

    await StorageBuilder(hass, config[CONFIG_STORAGE_PATH]).async_build()
    AssignService(hass).register()
    UnassignService(hass).register()
    ClearService(hass).register()
    StatusService(hass).register()

    return True


async def async_migrate_entry(hass, entry):
    if CONFIG_ENTRY_TYPE not in entry.data:
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, CONFIG_ENTRY_TYPE: ENTRY_TYPE_DEVICE},
        )

    return True


async def async_setup_entry(hass, entry):
    entryType = entry.data.get(CONFIG_ENTRY_TYPE)

    if entryType == ENTRY_TYPE_DIAGNOSTICS:
        return await DiagnosticsEntry(hass, entry).async_setup()

    if entryType == ENTRY_TYPE_DEVICE:
        return await DeviceEntry(hass, entry).async_setup()

    return True


async def async_unload_entry(hass, entry):
    entryType = entry.data.get(CONFIG_ENTRY_TYPE)

    if entryType == ENTRY_TYPE_DIAGNOSTICS:
        return await DiagnosticsEntry(hass, entry).async_unload()

    if entryType == ENTRY_TYPE_DEVICE:
        return await DeviceEntry(hass, entry).async_unload()

    return True


async def async_remove_entry(hass, entry):
    entryType = entry.data.get(CONFIG_ENTRY_TYPE)

    if entryType == ENTRY_TYPE_DIAGNOSTICS:
        return await DiagnosticsEntry(hass, entry).async_remove()

    if entryType == ENTRY_TYPE_DEVICE:
        return await DeviceEntry(hass, entry).async_remove()


async def _createRootConfig(hass):
    path = hass.config.path(f".storage/{DOMAIN}/storage.db")
    assignManager = AssignManager(hass, path)
    diagnosticCoordinator = DiagnosticCoordinator(hass, assignManager)

    config = {
        CONFIG_STORAGE_PATH: path,
        CONFIG_ASSIGN_MANAGER: assignManager,
        CONFIG_DIAGNOSTIC_COORDINATOR: diagnosticCoordinator,
    }
    hass.data.setdefault(DOMAIN, config)

    return config
