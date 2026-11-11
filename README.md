# VouchNexa Telegram Bot

Sanitized source archive for the VouchNexa Telegram voucher bot. Copy `.env.example` to `.env` and add your own newly issued Telegram bot token and settings before deployment. Never commit `.env`.

## Run locally

1. Install Python 3.11+ and dependencies with `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and set your configuration.
3. Run `python -m app`.

## Deploy on Railway

Add a PostgreSQL database and set the environment variables listed in `.env.example`, using Railway's database URL.

Note: this archive contains application scaffolding; the README claims more purchase/admin workflows than the current bot handlers implement.
