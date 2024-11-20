FROM python:3.12-slim AS base

ARG USERNAME=avicable
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV  POETRY_VERSION="^1" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN apt-get update -y \
    && apt-get install --no-install-recommends -y \
    libpq-dev gcc libgraphviz-dev \
    binutils libproj-dev gdal-bin postgresql-client \
    &&  apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*



FROM base AS builder
RUN --mount=type=cache,target=/root/.cache \
  pip install "poetry"
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/cache \
    poetry install --without dev --no-root


FROM base AS production
COPY --from=builder $VENV_PATH $VENV_PATH
COPY . /app
WORKDIR /app

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN chown -R $USERNAME:$USERNAME /app

USER $USERNAME

VOLUME ["/app/uploads"]

EXPOSE 8000

ENTRYPOINT ["bash", "/usr/bin/docker-entrypoint.sh"]
