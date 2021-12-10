"""This module provides the Slack related functions"""

from typing import NamedTuple, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from gitlabmrslack.config import SLACK_APP_TOKEN

slack_api = WebClient(token=SLACK_APP_TOKEN)

class SlackMessage(NamedTuple):
    """Class to define a Slack message

    Parameters
    ----------
    NamedTuple : NamedTuple
        A tuple describing a message
    """
    text: str
    timestamp: str
    channel_id: str

def get_messages(channel_id: str) -> List[SlackMessage]:
    """Gets last 200 messages in the given channel

    Parameters
    ----------
    channel_id : str
        Channel ID as visible in Slack

    Returns
    -------
    List[SlackMessage]
        The last 200 message in the channel
    """
    try:
        response = slack_api.conversations_history(channel=channel_id, limit=200)
        messages = []
        if response["ok"]:
            for message in response["messages"]:
                if message["type"] == "message":
                    messages.append(SlackMessage(
                        text=message.get("text", ""),
                        timestamp=message["ts"],
                        channel_id=channel_id))
        return messages
    except SlackApiError as api_exception:
        print(api_exception.response["error"])
        return []

def add_reaction(message: SlackMessage, reaction: str) -> None:
    """Reacts to the given message

    Parameters
    ----------
    message : SlackMessage
        Slack message to react to
    reaction : str
        The reaction to use
    """
    try:
        slack_api.reactions_add(
            channel=message.channel_id,
            name=reaction,
            timestamp=message.timestamp)
    except SlackApiError as api_exception:
        print(api_exception.response["error"])

def remove_reaction(message: SlackMessage, reaction: str) -> None:
    """Removes reaction from the given message

    Parameters
    ----------
    message : SlackMessage
        Slack message to remove the reaction from
    reaction : str
        The reaction to remove
    """
    try:
        slack_api.reactions_remove(
            channel=message.channel_id,
            name=reaction,
            timestamp=message.timestamp)
    except SlackApiError as api_exception:
        print(api_exception.response["error"])
