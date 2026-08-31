#!/bin/sh
# Přenese aktuální appku z tapkasa/ do nativního obalu.
# Pusť po každé úpravě tapkasa/index.html, než budeš znovu buildit v Xcode.
set -e
cd "$(dirname "$0")"
cp ../tapkasa/index.html Kasa/Resources/index.html
echo "Hotovo: Kasa/Resources/index.html je aktuální."
