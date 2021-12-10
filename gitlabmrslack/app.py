"""Main module of gitlab-mr-slack"""
from typing import Dict

from fastapi import FastAPI, Request
from mangum import Mangum
from gitlabmrslack.structure import ActionType
from gitlabmrslack.config import REACTION_APPROVED, REACTION_COMMENTS, REACTION_MERGED
from gitlabmrslack.gitlab import handle_webhook, GitlabEvent

import gitlabmrslack.slack

# Main entrypoint of the application
app = FastAPI()

# AWS Lambda entrypoint using Mangum wrapper
aws_handler = Mangum(app)


@app.get("")
@app.get("/")
async def root() -> Dict[str, str]:
    """Handles requests coming to the root path

    Returns
    -------
    Dict[str, str]
        Usage as JSON
    """
    return {"Usage": "Configure a GitLab webhook for: /webhook/channel-id/<channel_id>"}

@app.post("/webhook/channel-id/{channel_id}")
@app.post("/webhook/channel-id/{channel_id}/")
async def gitlab_webhook_endpoint(channel_id: str, request: Request) -> Dict:
    """Handles request coming to the webhook endpoint

    Parameters
    ----------
    channel_id : str
        Channel ID as visible in Slack
    request : Request
        The FastAPI request

    Returns
    -------
    dict
        The FastAPI response
    """
    response, gitlab_event = await handle_webhook(request)
    if gitlab_event is not None:
        process_gitlab_event(channel_id, gitlab_event)
    return response

def process_gitlab_event(channel_id: str, event: GitlabEvent) -> Dict[str, str]:
    """Processes a valid GitLab event

    Parameters
    ----------
    channel_id : str
        Channel ID as visible in Slack
    event : GitlabEvent
        Details of the GitLab event

    Returns
    -------
    Dict[str, str]
        Status as JSON
    """
    slack_messages = gitlabmrslack.slack.get_messages(channel_id)
    print(event)
    for message in slack_messages:
        if event.url in message.text:
            print(message)
            if event.action_type == ActionType.UNAPPROVE:
                gitlabmrslack.slack.remove_reaction(message, REACTION_APPROVED)
            elif event.action_type == ActionType.APPROVE:
                gitlabmrslack.slack.add_reaction(message, REACTION_APPROVED)
            elif event.action_type == ActionType.MERGE:
                gitlabmrslack.slack.add_reaction(message, REACTION_MERGED)
            elif event.action_type == ActionType.COMMENT:
                gitlabmrslack.slack.add_reaction(message, REACTION_COMMENTS)
            break
    return {'detail': 'OK'}
