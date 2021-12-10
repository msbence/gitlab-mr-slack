"""This module provides the GitLab related functions"""

from typing import Tuple, NamedTuple, Any
from fastapi import Request, status, HTTPException

from gitlabmrslack.structure import ActionType
from gitlabmrslack.config import GITLAB_WEBHOOK_TOKEN

class GitlabEvent(NamedTuple):
    """Class to define a GitLab event

    Parameters
    ----------
    NamedTuple : NamedTuple
        A tuple describing an event
    """
    url: str
    action_type: ActionType

async def handle_webhook(request: Request) -> Tuple[dict, GitlabEvent]:
    """Handles an incoming GitLab webhook

    Parameters
    ----------
    request : Request
        The incoming FastAPI request

    Returns
    -------
    Tuple[dict, GitlabEvent]
        Status and GitLab event as Tuple

    Raises
    ------
    HTTPException
        Exception if token is not provided, but required
    HTTPException
        Exception if token is invalid, but required
    """
    if GITLAB_WEBHOOK_TOKEN is not None:
        if 'X-Gitlab-Token' not in request.headers:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="Secret Token is mandatory, but not provided.")
        if request.headers['X-Gitlab-Token'] != GITLAB_WEBHOOK_TOKEN:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                detail="Secret Token is invalid.")
    webhook_data = await request.json()
    if webhook_data['event_type'] == 'note':
        return process_note_webhook(webhook_data)
    if webhook_data['event_type'] == 'merge_request':
        return process_merge_request_webhook(webhook_data)

def process_note_webhook(webhook_data: Any) -> Tuple[dict, GitlabEvent]:
    """Processes a GitLab comment/note event webhook

    Parameters
    ----------
    webhook_data : Any
        FastAPI request body as JSON

    Returns
    -------
    Tuple[dict, GitlabEvent]
        Status and GitLab event as Tuple
    """
    if webhook_data['object_attributes']['noteable_type'] != "MergeRequest":
        return {'detail': 'OK, but not MR note.'}, None
    event = GitlabEvent(
        url=webhook_data['object_attributes']['url'].split('#')[0],
        action_type=ActionType.COMMENT
    )
    return {'detail': 'OK'}, event

def process_merge_request_webhook(webhook_data: Any) -> Tuple[dict, GitlabEvent]:
    """Processes a GitLab merge request event webhook

    Parameters
    ----------
    webhook_data : Any
        FastAPI request body as JSON

    Returns
    -------
    Tuple[dict, GitlabEvent]
        Status and GitLab event as Tuple
    """
    if webhook_data['object_attributes']['action'] not in ['approved', 'unapproved', 'merge']:
        return {'detail': 'OK, but nothing to do.'}, None
    event = GitlabEvent(
        url=webhook_data['object_attributes']['url'],
        action_type=json_action_type_to_enum(webhook_data['object_attributes']['action'])
    )
    return {'detail': 'OK'}, event

def json_action_type_to_enum(json_action_type: str) -> ActionType:
    """Converts the GitLab action type found in JSON to Enum

    Parameters
    ----------
    json_action_type : str
        Action type string as found in JSON

    Returns
    -------
    ActionType
        Action type as Enum
    """
    if json_action_type == 'approved':
        return ActionType.APPROVE
    if json_action_type == 'unapproved':
        return ActionType.UNAPPROVE
    if json_action_type == 'merge':
        return ActionType.MERGE
    return None
