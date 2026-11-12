# EverwindFXCore

**A runtime CPU scheduling mod for Everwind on older CPUs, plus the two in-game settings that matter most.**

EverwindFXCore is a small native DLL that loads with the game and changes **how Windows schedules Everwind's
threads on your CPU**. It doesn't change graphics settings, game files or saves. It is a port of
[WindroseFXCore](https://github.com/mcirish3/WindroseFXCore) to Everwind (Unreal Engine 5.5).

It was built and tested on an AMD FX-8350 with a Radeon RX 6600 and adapts to whatever CPU it finds.

> **Status: 0.2.0-beta, and an honest one.** The mod builds, loads and tunes the game's threads as designed.
> Its effect on frame rate has **not** been measured in isolation yet. On the test PC the big win came from two
> in-game settings (below), not from the DLL. Please report your results with your log file.

---

## First: check these two settings

On the test PC (FX-8350, RX 6600, 1080p, 60 FPS limit) these made the largest difference by far:

| Setup | Real frames per second | GPU use |
|---|---|---|
| Frame Generation **on**, 60 FPS limit | **30** (shown as 60) | 59% |
| Frame Generation off, native resolution | 55.6 average, dips to 47 | 91% |
| Frame Generation off, **XeSS upscaling on Quality** | **59.5 average**, lowest 52 | 73% |

- **Frame Generation with a 60 FPS limit renders only 30 real frames.** The limit applies to the displayed frames,
  so half of them are interpolated. On a 60 Hz display, turn Frame Generation off.
- **Use XeSS upscaling (Quality)** if your graphics card is near 100%. XeSS works on AMD and NVIDIA cards too.

You don't need this mod for either of those.

## What the mod does

| Fix | What it does |
|---|---|
| **Exclusive game module** (experimental, on by default) | The GameThread, the busiest frame thread in Everwind, gets a whole FX module or physical core to itself. Every other thread in the game is kept off it, so nothing shares its FPU, decoder or L2 cache. Needs 8 or more logical processors. |
| **Topology-aware thread placement** | GameThread, RenderThread and RHIThread each prefer their own module (AMD FX) or core (SMT CPUs), read from your CPU's real cache layout at launch. |
| **Background worker isolation** | Unreal's background pool (asset streaming, decompression) is kept off the cores the frame threads prefer. |
| **Audio protection** | The audio mixer runs at time-critical priority on its own preferred core. |
| **Audio buffer fix** (optional, off by default) | Raises Unreal's audio buffer size. See [Audio dropouts or static](#audio-dropouts-or-static). |
| **Priority floors** | Frame threads run at least at Above Normal priority. |
| **0.5 ms timer resolution** | Lets the frame limiter and thread waits wake on time. |
| **Power-throttling opt-out** | Stops Windows from applying EcoQoS or timer coalescing to the game. |

**What to expect:** at best, steadier frame times on CPUs where threads fight over shared cores. It won't turn an old
CPU into a new one, and it can't help if your graphics card is the limit.

| CPU family | What applies |
|---|---|
| **AMD FX** (FX-8xxx/9xxx) | Everything, including the exclusive game module. |
| **Intel Core i7 with Hyper-Threading, Ryzen with 8+ threads** | Everything. Critical threads stay inside one L3 domain on multi-CCX Ryzen chips. |
| **Intel 12th gen and newer** | Critical threads are placed on P-cores. |
| **6 logical processors or fewer** | The exclusive game module switches itself off. |
| **Dual cores, or quad cores without SMT** | Thread placement switches itself off. The timer, priority and power fixes still apply. |

## Install

1. Download the latest zip from [Nexus Mods](https://www.nexusmods.com/everwind/mods/18), [GameBanana](https://gamebanana.com/mods/739464) or [Releases](../../releases).
2. In Steam, right-click **Everwind → Manage → Browse local files**.
3. Extract the zip into that folder. The files land in `skyverse\Binaries\Win64\`, next to
   `Everwind-Win64-Shipping.exe`:
   - `version.dll`
   - `EverwindFXCore.ini`
4. Launch the game through Steam as usual.

## Check that it's working

After launching, open `skyverse\Binaries\Win64\EverwindFXCore.log`. On an FX-8350 it looks like this:

```
EverwindFXCore 0.2.0-beta loaded into ...\Everwind-Win64-Shipping.exe
CPU: AMD FX(tm)-8350 Eight-Core Processor
Topology: 8 logical processors, 4 execution groups, 1 L3 domain(s)
Timer resolution: 0.500 ms
Power throttling opt-out: ok (execution speed only)
Process priority: raised
Critical LPs: game 0, render 2, rhi 4, audio 6 | background mask 0xe8
Exclusive game module: GameThread mask 0x3, every other thread 0xfc
  GameThread       tid  ...  prio 1
Exclusive game module: moved 11 thread(s) off the GameThread's group
  RHIThread        tid  ...  prio 1
  RenderThread     tid  ...  prio 1
  AudioMixer       tid  ...  prio 15
```

If there's no log file at all, the DLL isn't loading. Please open an issue.

## Configure

Every fix can be turned off on its own in `EverwindFXCore.ini`. That's the easiest way to A/B test:
turn one off, play the same stretch, and compare.

| Setting | Default | Notes |
|---|---|---|
| `Enabled` | 1 | Master switch |
| `TimerResolution100ns` | 5000 | 0.5 ms. `10000` = 1 ms, `0` = leave alone |
| `DisablePowerThrottling` | 1 | |
| `ProcessPriority` | 1 | 0 Normal, 1 Above Normal, 2 High (not recommended) |
| `PlaceCriticalThreads` | 1 | |
| `IsolateBackgroundWorkers` | 1 | |
| `ExclusiveGameModule` | 1 | Experimental. `0` = the plain WindroseFXCore placement |
| `BoostCriticalPriority` | 1 | |
| `BoostAudioPriority` | 1 | |
| `AudioMixerPriority` | 15 | 15 = time-critical, 2 = highest |
| `PlaceAudioThread` | 1 | |
| `AudioBufferFix` | 0 | Writes the audio buffer size to `Engine.ini`. See below |
| `AudioBufferFrames` | 2048 | Frames per buffer (256–8192) |
| `AudioBuffersToEnqueue` | 4 | Buffers queued ahead (2–8) |
| `VerboseLog` | 0 | Logs every worker thread too |
| `PerfLogSeconds` | 0 | Diagnostics: every N seconds, logs CPU use of the frame threads and workers (100% = one full core) |

**Reading the perf log:** the GameThread reads 85–95% whenever the game's frame limiter is active, because the
limiter busy-waits. That is not proof of a CPU limit. Compare runs at the same frame rate.

## Audio dropouts or static

This fix is carried over from WindroseFXCore and has **not been needed or tested in Everwind** on the test PC.
If Everwind's audio drops out or crackles, set `AudioBufferFix=1` in `EverwindFXCore.ini` and launch the game.

- At every launch the mod writes these lines to `%LOCALAPPDATA%\Everwind\Saved\Config\Windows\Engine.ini`:
  ```
  [/Script/WindowsTargetPlatform.WindowsTargetSettings]
  AudioCallbackBufferFrameSize=2048
  AudioNumBuffersToEnqueue=4
  ```
- The first time, an existing `Engine.ini` is copied to `Engine.ini.EverwindFXCore.bak`, and the original values of
  those two keys are recorded in `EverwindFXCore.state` next to the DLL.
- **To undo:** set `AudioBufferFix=0` (or `Enabled=0`) and launch once. The original values are put back, and
  `Engine.ini` is removed if the mod created it.

## Uninstall

1. If you turned on `AudioBufferFix`, set it to `0` and launch the game once so your `Engine.ini` is restored.
2. Delete `version.dll`, `EverwindFXCore.ini`, `EverwindFXCore.log` and `EverwindFXCore.state` (if present) from
   `skyverse\Binaries\Win64`.

Without the audio buffer fix, nothing outside the mod's own files is changed.

## FAQ

**Is it safe online?** Everwind had no anti-cheat in its install folder when this was written (November 2026).
If a future patch adds anti-cheat, remove the DLL before playing online. This mod is not intended for use with anti-cheat.

**Will it mess up my saves or settings?** No. It never touches saves or game files, and it only touches
`Engine.ini` if you turn on `AudioBufferFix`, with a backup and automatic restore.

**Does it work with other mods?** Yes, unless another mod also uses `version.dll` as its loader. In that case
only one can be installed at a time.

**The game won't start after an update.** Delete `version.dll` to rule it out, then open an issue with the game version.

## Reporting results

Open an [issue](../../issues) with:
- your CPU, GPU and RAM
- your `EverwindFXCore.log`
- average FPS and 1% lows with `Enabled=1` and with `Enabled=0`, in the same spot, with Frame Generation off

## Building from source

The mod is plain C with no dependencies.

```
pip install ziglang
python -m ziglang cc -target x86_64-windows-gnu -O2 -shared -o version.dll src/version_proxy.c src/fxcore.c src/version.def -ladvapi32 -s
```
Or run `build.bat` (Windows) or `build.sh` (Linux/macOS). `python package.py <version>` makes the release zip.

**How it loads:** Unreal Engine links `version.dll`, so the game loads it from its own folder first.
`src/version_proxy.c` forwards all 17 real exports to `System32\version.dll`, and `src/fxcore.c` starts one
background thread that does the work. It only activates inside an executable whose name contains `Shipping`,
so the crash reporter and other tools are never affected.

## License

MIT. See [LICENSE](LICENSE).

Created by Patrick McCoy, with Claude (Anthropic).
