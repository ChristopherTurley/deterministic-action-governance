from __future__ import annotations

import os

def _safe_int(x: str | None, default: int) -> int:
    try:
        return int(x) if x is not None else default
    except Exception:
        return default

def configure_sounddevice() -> None:
    """
    Force sounddevice to use a stable input device.
    Reads env var:
      VERA_INPUT_DEVICE (int)  -> input device index to use (default 0)
    """
    try:
        import sounddevice as sd

        input_idx = _safe_int(os.getenv("VERA_INPUT_DEVICE"), 0)

        # Preserve output device if set; otherwise keep whatever sounddevice already chose
        try:
            cur = sd.default.device
            out = cur[1] if isinstance(cur, (list, tuple)) and len(cur) > 1 else None
        except Exception:
            out = None

        sd.default.device = (input_idx, out)

        # Print a helpful confirmation line
        try:
            dev = sd.query_devices(input_idx)
            name = dev.get("name", "Unknown")
            max_in = dev.get("max_input_channels", "?")
            print(f"[AUDIO] Input device pinned -> {input_idx}: {name} (inputs={max_in})")
        except Exception:
            print(f"[AUDIO] Input device pinned -> {input_idx}")
    except Exception as e:
        print(f"[AUDIO] WARNING: sounddevice not configured ({e})")
