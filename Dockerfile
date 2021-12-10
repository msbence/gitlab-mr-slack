FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN apt-get update && apt-get upgrade -y

RUN apt-get -y clean

ENV PORT=8080 \
    APP_MODULE="gitlabmrslack.app:app"

EXPOSE 8080

ENV USER=docker \
    GROUP=docker \
    UID=12345 \
    GID=23456 \
    HOME=/app \
    PYTHONUNBUFFERED=1
WORKDIR ${HOME}

# Create user/group
RUN addgroup --gid "${GID}" "${GROUP}" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "${GROUP}" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

RUN chown -R docker:docker ${HOME}

USER ${USER}

COPY requirements.txt ${HOME}/

RUN cd ${HOME} \
    && pip install -r requirements.txt

# Copy the application
COPY --chown=docker:docker gitlabmrslack gitlabmrslack
