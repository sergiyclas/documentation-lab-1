# src/common/constants.py

"""Application constants"""

SUBSCRIPTION_TYPES = {
    "FREE": "FreeSubscription",
    "PREMIUM": "PremiumSubscription",
    "STUDENT": "StudentSubscription",
}

SUBSCRIPTION_PRICING = {
    "FreeSubscription": 0.00,
    "PremiumSubscription": 9.99,
    "StudentSubscription": 4.99,
}

SUBSCRIPTION_FEATURES = {
    "FreeSubscription": {
        "offline_download": False,
        "high_quality": False,
        "ad_free": False,
    },
    "PremiumSubscription": {
        "offline_download": True,
        "high_quality": True,
        "ad_free": True,
    },
    "StudentSubscription": {
        "offline_download": True,
        "high_quality": False,
        "ad_free": False,
    },
}
