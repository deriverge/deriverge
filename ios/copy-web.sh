#!/bin/sh
# Přenese aktuální appku z kava/ do nativního obalu.
# Pusť po každé úpravě kava/index.html, než budeš znovu buildit v Xcode.
set -e
cd "$(dirname "$0")"
cp ../kava/index.html Kasa/Resources/index.html
echo "Hotovo: Kasa/Resources/index.html je aktuální."
