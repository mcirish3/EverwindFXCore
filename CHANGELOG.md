# Changelog

## 0.2.0-beta - 2026-11-11

First public release. Port of WindroseFXCore 1.0.2-beta to Everwind (Unreal Engine 5.5.2).

- New, experimental, on by default: `ExclusiveGameModule=1` gives the GameThread a whole FX module or physical core and keeps every other thread in the game off it. Needs 8 or more logical processors; otherwise it switches itself off.
- The user config folder is fixed to `%LOCALAPPDATA%\Everwind`. The game's project folder is `skyverse`, so it can't be derived from the DLL path.
- Tested on an FX-8350 with an RX 6600: the mod loads and tunes threads as designed. Its effect on frame rate has not been measured in isolation.
- Found while testing: with Frame Generation on and a 60 FPS limit the game renders only 30 real frames. With Frame Generation off and XeSS upscaling on Quality the test PC holds 60. See the README.
- The GameThread's CPU load reads high whenever the frame limiter is active, because the limiter busy-waits. The perf log notes say so.

## 0.1.0-beta - 2026-11-11

Not released. Straight port of WindroseFXCore with renamed files.
