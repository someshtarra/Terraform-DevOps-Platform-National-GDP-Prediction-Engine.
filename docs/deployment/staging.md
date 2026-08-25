# Staging Environment Deployment Guide

## Overview
Triggered when release candidate tags (`v*.*.*-rc*`) are pushed to the repository.

## Steps
1. Tag release: `git tag v1.0.0-rc1 && git push origin v1.0.0-rc1`.
2. Pipeline deploys to `gdp-staging` namespace.
3. Executes integration test suite.
