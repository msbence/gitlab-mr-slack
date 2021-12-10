"""This module handles the app configuration"""

import os

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
GITLAB_WEBHOOK_TOKEN = os.getenv("GITLAB_WEBHOOK_TOKEN")
REACTION_COMMENTS = os.getenv("REACTION_COMMENTS", "speech_balloon")
REACTION_APPROVED = os.getenv("REACTION_APPROVED", "white_check_mark")
REACTION_MERGED = os.getenv("REACTION_MERGED", "leftwards_arrow_with_hook")
