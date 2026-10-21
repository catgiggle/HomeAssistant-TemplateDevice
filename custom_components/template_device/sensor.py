from .constants import *
from .entry.DeviceEntry import DeviceEntry
from .entry.DiagnosticsEntry import DiagnosticsEntry


async def async_setup_entry(hass, entry, async_add_entities):
    entryType = entry.data.get(CONFIG_ENTRY_TYPE)

    if entryType == ENTRY_TYPE_DIAGNOSTICS:
        return await DiagnosticsEntry(hass, entry).async_setup_sensor(async_add_entities)

    if entryType == ENTRY_TYPE_DEVICE:
        return await DeviceEntry(hass, entry).async_setup_sensor(async_add_entities)

    return True
