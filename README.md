# GitLab-MR-Slack

Reacts for GitLab Merge Request messages in Slack.

---

**WARNING: This application is currently in beta stage. Breaking changes and unexpected errors may happen.**

---

## Usage

First, you have to obtain a Slack API token. This can be done by creating and installing a slack application in the desired workspace. Now you should assign the OAuth scopes detailed below, in order to get an app token.

Once you are running this application, you have to configure GitLab to send webhooks from **Merge Request** and **Comments** events. The URL should be like this: `base.domain/webhook/channel-id/<channel_id>`

Now when somebody sends in a Merge Request URL, and GitLab notifies this application about an event, it will get a reaction automatically.

### Required Bot OAuth scopes (SlackAPI)

 - **channels:history** - View messages in public channels (where the integration is added).
 - **groups:history** - View messages in private channels (where the integration is added).
 - **reactions:read** - Add reaction to messages.
 - **reactions:write** - Remove reaction from messages.

### Environment variables
| **Name** | **Description** | **Default** | **Required** |
|-|-|-|-|
|`SLACK_APP_TOKEN`| The Slack application token to use | - | **yes** |
|`GITLAB_WEBHOOK_TOKEN`| GitLab webhook token to accept | `None` | no |
|`REACTION_COMMENTS`| Name of the reaction to use when MR gets comment | `speech_balloon` | no |
|`REACTION_APPROVED`| Name of the reaction to use when MR gets approved | `white_check_mark` | no |
|`REACTION_MERGED`| Name of the reaction to use when MR gets merged | `leftwards_arrow_with_hook` | no |


## Run

### Running in Docker

```bash
docker run -d -p 8080:8080 -e SLACK_APP_TOKEN="*****" registry.mbraptor.tech/public/gitlab-mr-slack:latest
```

### Run as AWS Lambda function

**UNTESTED!** *But you will need to zip the gitlabmrslack folder, upload it to S3, install the requirements, use API Gateway, and specify the correct lambda handler function.*

### Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn gitlabmrslack.app:app
```

## Build

### Docker container

```bash
docker build -t gitlab-mr-slack .
```

## Testing

:'(
