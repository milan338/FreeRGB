# Run this file after creating / modifying custom effect definitions
# This script will generate a JSON file containing relevant definitions
# needed to integrate custom effects into the UI

from ui.effects.Effects import Effects

effects = Effects
effects()
