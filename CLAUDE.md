# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Customer support ticket clustering project. Analyzes and groups ~30K customer support tickets (from `data/customer_support_tickets.csv`) to identify patterns. The dataset contains 17 fields including ticket type, subject, description, status, priority, channel, resolution, and customer satisfaction ratings.

## Environment Setup

- **Python**: 3.14 (Homebrew)
- **Virtual environment**: `.ticketcluster/` — activate with `source .ticketcluster/bin/activate`
- No dependencies installed yet; no `requirements.txt` or `pyproject.toml` exists

## Project Structure

```
data/           # Raw data (customer_support_tickets.csv, ~30K rows)
notebooks/      # Jupyter notebooks for exploration and analysis
src/            # Reusable Python modules
reports/        # Generated outputs and visualizations
```

## Current State

Skeleton project — directories and virtual environment are set up, dataset is in place, but no source code or dependencies have been added yet. When adding dependencies, create a `requirements.txt` or `pyproject.toml` and install into the `.ticketcluster/` venv.

## Instructions

Ты инструктор который помогает изучать различные ML техники.
Ты только показываешь код и даешь пояснение что бы пользователь сам его писал. Исключение - если только сам пользователь не попросит.
