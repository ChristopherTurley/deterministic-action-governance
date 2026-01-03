from __future__ import annotations

import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import List


def nhl_games_today(max_games: int = 6) -> List[str]:
    """
    Dependency-free NHL schedule.
    Uses ESPN scoreboard JSON. Retries + longer timeout.
    Returns [] if unavailable (caller can fallback).
    """
    date = datetime.now().strftime("%Y%m%d")
    url = f"https://site.web.api.espn.com/apis/v2/sports/hockey/nhl/scoreboard?dates={date}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/605.1.15 Safari/605.1.15"},
    )

    last_err = None
    for _ in range(2):
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read().decode("utf-8"))
            events = data.get("events") or []
            out: List[str] = []
            for ev in events:
                comps = (ev.get("competitions") or [])
                if not comps:
                    continue
                c = comps[0]
                competitors = c.get("competitors") or []
                if len(competitors) < 2:
                    continue
                a = competitors[0].get("team", {}).get("displayName", "Team A")
                b = competitors[1].get("team", {}).get("displayName", "Team B")
                status = c.get("status", {}).get("type", {}).get("shortDetail", "") or ""
                line = f"{a} vs {b}"
                if status:
                    line += f" — {status}"
                out.append(line)
                if len(out) >= max_games:
                    break
            return out
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            continue
        except Exception as e:
            last_err = e
            break

    return []
