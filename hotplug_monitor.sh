#!/bin/bash

X_USER=purism
export DISPLAY=:0
export XAUTHORITY=/home/$X_USER/.Xauthority
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus

function connect() {
	systemd-cat echo "mon connect"
	sleep 1
	switch-primary-display.py
}

function disconnect() {
	systemd-cat echo "mon disconnect"
}

if [ $(cat /sys/class/drm/card2-DP-1/status) == "connected" ] ; then
	connect
elif [ $(cat /sys/class/drm/card2-DP-1/status) == "disconnected" ] ; then
	disconnect
else
	exit
fi
