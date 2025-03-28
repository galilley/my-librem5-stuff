#!/usr/bin/python3

# https://dbus.freedesktop.org/doc/dbus-python/tutorial.html
# https://github.com/GNOME/mutter/blob/b5f99bd12ebc483e682e39c8126a1b51772bc67d/data/dbus-interfaces/org.gnome.Mutter.DisplayConfig.xml
# https://discussion.fedoraproject.org/t/change-scaling-resolution-of-primary-monitor-from-bash-terminal/19892

import dbus
bus = dbus.SessionBus()

display_config_well_known_name = "org.gnome.Mutter.DisplayConfig"
display_config_object_path = "/org/gnome/Mutter/DisplayConfig"

display_config_proxy = bus.get_object(display_config_well_known_name, display_config_object_path)
display_config_interface = dbus.Interface(display_config_proxy, dbus_interface=display_config_well_known_name)

serial, physical_monitors, logical_monitors, properties = display_config_interface.GetCurrentState()

updated_logical_monitors=[]
#print(len(logical_monitors))
for x, y, scale, transform, primary, linked_monitors_info, props in logical_monitors:
    #print(primary, type(primary))
    #print(linked_monitors_info)
    #if primary == 1:
    #    scale = 2.0 if (scale == 1.0) else 1.0 # toggle scaling between 1.0 and 2.0 for the primary monitor
    physical_monitors_config = []
    for linked_monitor_connector, linked_monitor_vendor, linked_monitor_product, linked_monitor_serial in linked_monitors_info:
        for monitor_info, monitor_modes, monitor_properties in physical_monitors:
            monitor_connector, monitor_vendor, monitor_product, monitor_serial = monitor_info
            if linked_monitor_connector == monitor_connector:
                if monitor_connector == 'DP-1':
                    primary = True
                else:
                    primary = False
                for mode_id, mode_width, mode_height, mode_refresh, mode_preferred_scale, mode_supported_scales, mode_properties in monitor_modes:
                    if mode_properties.get("is-current", False): # ( mode_properties provides is-current, is-preferred, is-interlaced, and more)
                        physical_monitors_config.append([monitor_connector, mode_id, {}])
    updated_logical_monitors.append([x, y, scale, transform, primary, physical_monitors_config])

properties_to_apply = { "layout_mode": properties.get("layout-mode")}
method = 2 # 2 means show a prompt before applying settings; 1 means instantly apply settings without prompt
display_config_interface.ApplyMonitorsConfig(serial, method, updated_logical_monitors, properties_to_apply)
