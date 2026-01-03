from __future__ import annotations

import json
import os
import queue
from dataclasses import dataclass
from typing import Optional

import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer


@dataclass
class STTConfig:
    model_path: str
    sample_rate: int = 16000
    device_index: Optional[int] = None
    block_seconds: float = 0.25


class VoskSTT:
    """
    Offline, streaming STT using Vosk.
    Phase 1 goals:
      - Short utterances
      - Wake-word compatible
      - No lyric runaway
    """

    def __init__(self, cfg: STTConfig):
        self.cfg = cfg
        self.model = Model(cfg.model_path)
        self.rec = KaldiRecognizer(self.model, cfg.sample_rate)
        self.rec.SetWords(False)
        self._q: queue.Queue[bytes] = queue.Queue()

    def _callback(self, indata, frames, time, status):
        if status:
            # Ignore transient warnings
            pass
        # Convert float32 -> int16 PCM
        pcm16 = (np.clip(indata[:, 0], -1.0, 1.0) * 32767).astype(np.int16)
        self._q.put(pcm16.tobytes())

    def listen_once(self, max_seconds: float = 6.0) -> Optional[str]:
        """
        Listen for up to max_seconds and return a finalized utterance.
        """
        sr = self.cfg.sample_rate
        blocks = int(max_seconds / self.cfg.block_seconds)

        with sd.InputStream(
            samplerate=sr,
            channels=1,
            dtype="float32",
            callback=self._callback,
            device=self.cfg.device_index,
            blocksize=int(sr * self.cfg.block_seconds),
        ):
            for _ in range(blocks):
                try:
                    data = self._q.get(timeout=self.cfg.block_seconds + 0.1)
                except queue.Empty:
                    continue

                if self.rec.AcceptWaveform(data):
                    res = json.loads(self.rec.Result())
                    text = (res.get("text") or "").strip()
                    if text:
                        return text

            # Final attempt if silence ended the stream
            res = json.loads(self.rec.FinalResult())
            text = (res.get("text") or "").strip()
            return text if text else None


def build_stt_from_env() -> VoskSTT:
    """
    Environment variables:
      VERA_STT_MODEL     path to Vosk model directory
      VERA_INPUT_DEVICE integer sounddevice input index
    """
    model_path = os.environ.get("VERA_STT_MODEL", "models/vosk-model-small-en-us-0.15")
    dev = os.environ.get("VERA_INPUT_DEVICE")
    device_index = int(dev) if dev and dev.isdigit() else None
    cfg = STTConfig(model_path=model_path, device_index=device_index)
    return VoskSTT(cfg)
