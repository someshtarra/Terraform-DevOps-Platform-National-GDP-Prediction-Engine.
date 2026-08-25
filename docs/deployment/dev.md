# Development Environment Deployment Guide

## Overview
Automated deployment to the `gdp-dev` EKS namespace whenever code is pushed to the `main` or `dev` branches.

## Steps
1. Push code to `main` branch.
2. `.github/workflows/cd-dev.yml` builds Docker image tagged with `<git-sha>`.
3. Pushes image to ECR `gdp-prediction-app-dev`.
4. Executes `helm upgrade --install gdp-app-dev ./helm/gdp-prediction-app --values ./helm/gdp-prediction-app/values-dev.yaml`.
5. Runs `./scripts/smoke_test.sh dev`.
