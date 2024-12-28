# Pandemic Helper CLI

A command-line tool for tracking infection cards in the Pandemic board game.

## Commands

- `print` (shorthand: `p`): Display current infection deck and discard pile
- `draw_card` (shorthand: `dc`): Move card(s) from infection deck to discard
- `remove_discard` (shorthand: `rd`): Remove card(s) from discard pile
- `shuffle`: Move all cards from discard pile to a new infection deck
- `mark`: Mark cards with colors for highlighting (e.g., red, yellow). Use color `none` to reset to default
- `save`: Copy current state to a backup file
- `load`: Restore from backup

City names with spaces should use underscores (e.g., `new_york`). Game state is stored in `state.json` in the current directory.

## Running

You can either:
- Run directly: `python3 helper_cli.py`
- Install as CLI: `pip install -e .`

## Command Completion

1. Update `cards.txt` with the city names in your game, one per line
2. Enable completion by running:
```bash
eval "$(_PANDEMIC_HELPER_COMPLETE=bash_source pandemic_helper)"
```

After setup, you can use tab completion for city names in commands.
