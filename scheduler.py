from anki_sm_2 import Scheduler, Card as SMCard, Rating
from datetime import datetime, timezone

scheduler = Scheduler()

def review(card_model, grade: int):
    smcard = SMCard(due=datetime.now(timezone.utc))
    smcard.ease_factor = card_model.ef
    smcard.interval = card_model.interval
    smcard.repetitions = card_model.repetitions

    smcard, review = scheduler.review_card(smcard,
                                           rating=Rating(grade))
    card_model.ef = smcard.ease_factor
    card_model.interval = smcard.interval
    card_model.repetitions = smcard.repetitions
    card_model.due = review.review_datetime.replace(tzinfo=None)
    return card_model
