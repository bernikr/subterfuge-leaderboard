FROM ghcr.io/astral-sh/uv:debian-slim

EXPOSE 8000
WORKDIR /usr/src

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get -y update && apt-get install -y cron
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.python-version,target=.python-version \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN chmod +x entrypoint.sh

ENV PATH="/usr/src/.venv/bin:$PATH"

CMD ["/usr/src/entrypoint.sh"]
