from __future__ import annotations

import os
import tempfile
import wave
import threading
from dataclasses import dataclass
from typing import Optional, List

import numpy as np
import sounddevice as sd


@dataclass
class ListenerConfig:
    sample_rate: int = 16000
    channels: int = 1
    dtype: str = "float32"

    # utterance controls
    max_utterance_s: float = 10.0       # allow slow speakers
    min_utterance_s: float = 0.45       # ignore tiny noise clips
    pre_roll_s: float = 0.35            # don't clip first word
    silence_seconds: float = 0.70       # stop after this much silence
    rms_speech_threshold: float = 0.012 # raise if too sensitive, lower if missing speech
    frame_ms: int = 30                  # processing chunk size


class VoiceListener:
    """
    VAD-style listener that records ONE full utterance (until silence),
    then transcribes it with Whisper.

    Adds clean shutdown to avoid macOS CoreAudio/PortAudio teardown crashes.
    """

    def __init__(self, model_size: str = "base", record_seconds: float = 0.0):
        self.model_size = model_size
        self.cfg = ListenerConfig()
        self._whisper_model = None

        # Shutdown / lifecycle
        self._stop_event = threading.Event()
        self._stream: Optional[sd.InputStream] = None

    # ---------------------------
    # Public API
    # ---------------------------
    def listen(self) -> str:
        if self._stop_event.is_set():
            return ""
        audio = self._record_until_silence()
        if audio is None:
            return ""
        return self._transcribe_with_whisper(audio)

    def close(self) -> None:
        """
        Best-effort cleanup to prevent segfaults at interpreter shutdown.
        """
        self._stop_event.set()

        # Stop/close any active stream
        try:
            st = self._stream
            if st is not None:
                try:
                    st.stop()
                except Exception:
                    pass
                try:
                    st.close()
                except Exception:
                    pass
        finally:
            self._stream = None

        # Ensure PortAudio stops
        try:
            sd.stop()
        except Exception:
            pass

        # sounddevice has a private PortAudio terminator; use best-effort
        try:
            if hasattr(sd, "_terminate"):
                sd._terminate()  # type: ignore[attr-defined]
        except Exception:
            pass

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass

    # ---------------------------
    # Recording (silence-based)
    # ---------------------------
    def _record_until_silence(self) -> Optional[np.ndarray]:
        if self._stop_event.is_set():
            return None

        sr = self.cfg.sample_rate
        frame_len = int(sr * (self.cfg.frame_ms / 1000.0))
        max_frames = int((self.cfg.max_utterance_s * sr) / frame_len)

        pre_roll_frames = max(1, int((self.cfg.pre_roll_s * sr) / frame_len))
        silence_frames_needed = max(1, int((self.cfg.silence_seconds * sr) / frame_len))

        ring: List[np.ndarray] = []
        captured: List[np.ndarray] = []

        speech_started = False
        silence_run = 0

        try:
            with sd.InputStream(
                samplerate=sr,
                channels=self.cfg.channels,
                dtype=self.cfg.dtype,
                blocksize=frame_len,
            ) as stream:
                self._stream = stream

                for _ in range(max_frames):
                    if self._stop_event.is_set():
                        break

                    frame, _ = stream.read(frame_len)
                    x = frame[:, 0].astype(np.float32)

                    # Pre-roll ring buffer
                    ring.append(x)
                    if len(ring) > pre_roll_frames:
                        ring.pop(0)

                    rms = float(np.sqrt(np.mean(x * x)))

                    if not speech_started:
                        # Wait for speech energy
                        if rms >= self.cfg.rms_speech_threshold:
                            speech_started = True
                            captured.extend(ring)  # include pre-roll
                            captured.append(x)
                            silence_run = 0
                        else:
                            continue
                    else:
                        captured.append(x)

                        # silence detection (slightly below threshold to avoid early cutoff)
                        if rms < (self.cfg.rms_speech_threshold * 0.85):
                            silence_run += 1
                        else:
                            silence_run = 0

                        if silence_run >= silence_frames_needed:
                            break

        except Exception:
            # CoreAudio hiccup -> return None (main loop can rebuild)
            return None
        finally:
            # Make sure stream reference doesn't linger
            self._stream = None

        if self._stop_event.is_set():
            return None

        if not captured:
            return None

        audio = np.concatenate(captured, axis=0)
        dur = len(audio) / sr
        if dur < self.cfg.min_utterance_s:
            return None

        # light normalization (helps whisper)
        peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
        if peak > 0.0:
            audio = audio / max(peak, 1e-6)

        return audio

    # ---------------------------
    # WAV temp writer (for whisper file-path workflows)
    # ---------------------------
    def _write_wav_temp(self, audio: np.ndarray) -> str:
        sr = self.cfg.sample_rate
        audio16 = np.clip(audio, -1.0, 1.0)
        audio16 = (audio16 * 32767.0).astype(np.int16)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_path = tmp.name
        tmp.close()

        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sr)
            wf.writeframes(audio16.tobytes())

        return tmp_path

    # ---------------------------
    # Whisper transcription
    # ---------------------------
    def _transcribe_with_whisper(self, audio: np.ndarray) -> str:
        if self._whisper_model is None:
            import whisper
            self._whisper_model = whisper.load_model(self.model_size)

        wav_path = self._write_wav_temp(audio)
        try:
            result = self._whisper_model.transcribe(wav_path, fp16=False)
            text = (result.get("text") or "").strip()
            return text
        finally:
            try:
                os.remove(wav_path)
            except Exception:
                pass


# --- compatibility alias (runtime expects Listener) ---
Listener = VoiceListener
