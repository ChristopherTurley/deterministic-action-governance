from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

ESPN_SCOREBOARD: Dict[str, str] = {
    "NHL": "https://site.api.espn.com/apis/v2/sports/hockey/nhl/scoreboard",
    "NBA": "https://site.api.espn.com/apis/v2/sports/basketball/nba/scoreboard",
    "WNBA": "https://site.api.espn.com/apis/v2/sports/basketball/wnba/scoreboard",
    "NFL": "https://site.api.espn.com/apis/v2/sports/football/nfl/scoreboard",
    "MLB": "https://site.api.espn.com/apis/v2/sports/baseball/mlb/scoreboard",
    "NCAAF": "https://site.api.espn.com/apis/v2/sports/football/college-football/scoreboard",
    "NCAAM": "https://site.api.espn.com/apis/v2/sports/basketball/mens-college-basketball/scoreboard",
    "NCAAW": "https://site.api.espn.com/apis/v2/sports/basketball/womens-college-basketball/scoreboard",
    "EPL": "https://site.api.espn.com/apis/v2/sports/soccer/eng.1/scoreboard",
    "UCL": "https://site.api.espn.com/apis/v2/sports/soccer/uefa.champions/scoreboard",
}
MAJOR_DEFAULT_LEAGUES: List[str] = ["NHL", "NBA", "NFL", "MLB", "EPL", "UCL"]

@dataclass
class SourceLink:
    title: str
    url: str

@dataclass
class GameItem:
    league: str
    start_iso: str
    status: str
    away: str
    home: str
    broadcast: Optional[str] = None
    url: Optional[str] = None

@dataclass
class SportsResult:
    date_iso: str
    leagues: List[str]
    games: List[GameItem]
    sources: List[SourceLink]
    errors: List[str]

def _today_local() -> dt.date:
    return dt.datetime.now().date()

def resolve_date_ref(text: str, today: Optional[dt.date] = None) -> dt.date:
    t = (text or "").lower()
    today = today or _today_local()
    if "tomorrow" in t:
        return today + dt.timedelta(days=1)
    if "tonight" in t or "today" in t:
        return today
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    for i, wd in enumerate(weekdays):
        if wd in t:
            delta = (i - today.weekday()) % 7
            return today + dt.timedelta(days=delta)
    return today

def infer_leagues(text: str) -> List[str]:
    t = (text or "").lower()
    if "nhl" in t or "hockey" in t:
        return ["NHL"]
    if "nba" in t:
        return ["NBA"]
    if "wnba" in t:
        return ["WNBA"]
    if "nfl" in t or "football" in t:
        return ["NFL"]
    if "mlb" in t or "baseball" in t:
        return ["MLB"]
    if "college football" in t or "ncaaf" in t:
        return ["NCAAF"]
    if "men's college" in t or "ncaam" in t:
        return ["NCAAM"]
    if "women's college" in t or "ncaaw" in t:
        return ["NCAAW"]
    if "epl" in t or "premier league" in t:
        return ["EPL"]
    if "champions league" in t or "ucl" in t:
        return ["UCL"]
    return MAJOR_DEFAULT_LEAGUES[:]

def fetch_espn_scoreboard(league: str, date: dt.date, timeout_s: float = 8.0) -> Tuple[List[GameItem], Optional[str]]:
    url = ESPN_SCOREBOARD.get(league)
    if not url:
        return [], f"Unknown league: {league}"
    params = {"dates": date.strftime("%Y%m%d")}
    try:
        r = requests.get(url, params=params, timeout=timeout_s)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return [], f"{league} fetch failed: {e}"

    games: List[GameItem] = []
    for ev in (data.get("events") or []):
        try:
            comp = (ev.get("competitions") or [])[0]
            competitors = comp.get("competitors") or []
            away = next(c for c in competitors if c.get("homeAway") == "away")
            home = next(c for c in competitors if c.get("homeAway") == "home")

            start = ev.get("date") or ""
            status = ((ev.get("status") or {}).get("type") or {}).get("description") or "Scheduled"

            broadcast = None
            broadcasts = comp.get("broadcasts") or []
            if broadcasts:
                names = broadcasts[0].get("names")
                if isinstance(names, list) and names:
                    broadcast = ", ".join(names)

            link = None
            links = ev.get("links") or []
            if links:
                link = links[0].get("href")

            games.append(
                GameItem(
                    league=league,
                    start_iso=start,
                    status=status,
                    away=((away.get("team") or {}).get("displayName")) or "Away",
                    home=((home.get("team") or {}).get("displayName")) or "Home",
                    broadcast=broadcast,
                    url=link,
                )
            )
        except Exception:
            continue

    return games, None

def get_games(text: str, today: Optional[dt.date] = None) -> SportsResult:
    date = resolve_date_ref(text, today=today)
    leagues = infer_leagues(text)

    all_games: List[GameItem] = []
    errors: List[str] = []
    for lg in leagues:
        games, err = fetch_espn_scoreboard(lg, date)
        if err:
            errors.append(err)
        all_games.extend(games)

    all_games.sort(key=lambda g: g.start_iso or "")

    sources: List[SourceLink] = []
    for lg in leagues:
        if lg in ESPN_SCOREBOARD:
            sources.append(SourceLink(title=f"{lg} scoreboard (ESPN)", url=ESPN_SCOREBOARD[lg]))

    return SportsResult(
        date_iso=date.isoformat(),
        leagues=leagues,
        games=all_games,
        sources=sources[:3],
        errors=errors,
    )

def format_sports_response(result: SportsResult, max_spoken: int = 3) -> Dict[str, Any]:
    games = result.games
    if not games:
        spoken = f"I am not seeing any games for {result.date_iso}. Say a league (NHL, NBA, NFL, MLB) or a team and I will narrow it."
        display = [spoken, "", "Sources:"] + [f"{i}. {s.title}" for i, s in enumerate(result.sources, start=1)]
        return {"spoken": spoken, "display_lines": display, "sources": [s.__dict__ for s in result.sources]}

    def one_line(g: GameItem) -> str:
        t = "TBD"
        if g.start_iso and "T" in g.start_iso:
            t = g.start_iso.split("T", 1)[1][:5]
        net = f" on {g.broadcast}" if g.broadcast else ""
        return f"{g.away} at {g.home} {t}{net}"

    total = len(games)
    leagues = ", ".join(sorted(set(g.league for g in games)))
    highlights = games[:max_spoken]

    spoken = (
        f"{result.date_iso}: {total} games across {leagues}. "
        + " / ".join(one_line(g) for g in highlights)
        + ". Say 'full list' or name a team."
    )

    display: List[str] = []
    by_league: Dict[str, List[GameItem]] = {}
    for g in games:
        by_league.setdefault(g.league, []).append(g)

    for lg in sorted(by_league.keys()):
        display.append(f"== {lg} ==")
        for g in by_league[lg]:
            display.append(one_line(g))

    display.append("")
    display.append("Sources:")
    for i, s in enumerate(result.sources, start=1):
        display.append(f"{i}. {s.title}")

    return {"spoken": spoken, "display_lines": display, "sources": [s.__dict__ for s in result.sources]}
