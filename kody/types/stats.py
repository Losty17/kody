from typing import TypedDict


class Stats(TypedDict):
    total_votes: int
    vote_streak: int
    max_vote_streak: int

    total_dailies: int
    daily_streak: int
    max_daily_streak: int

    quests_seen: int
    quests_answered: int
    quests_right: int
