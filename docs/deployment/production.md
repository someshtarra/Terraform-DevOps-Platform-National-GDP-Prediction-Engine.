# Production Environment Deployment Guide

## Overview
Requires explicit manual approval in GitHub Environment settings.

## Steps
1. Release tag published (`v1.0.0`).
2. GitHub Actions triggers `cd-production.yml`.
3. Pauses at **Environment Approval Gate**.
4. Designated reviewer approves deployment in GitHub UI.
5. Performs zero-downtime rolling deployment to `gdp-production`.
6. Executes `./scripts/smoke_test.sh production`.
7. Automatically rolls back if deployment fails.
