# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a personal tech blog built with [Jekyll](https://jekyllrb.com/) using the **Minima** theme. Posts cover topics like .NET, Python, computer vision, ML, DevOps, and mobile development.

## Common Commands

```bash
# Install dependencies
bundle install

# Serve locally with live reload (http://localhost:4000)
bundle exec jekyll serve

# Build the static site into _site/
bundle exec jekyll build

# Serve with drafts visible
bundle exec jekyll serve --drafts
```

## Post Format

Posts live in `_posts/` and follow the naming convention `YYYY-MM-DD-title-slug.md`.

Each post requires this front matter:

```yaml
---
layout: post
title: "Post Title"
date: YYYY-MM-DD 00:00:00 +0000
categories: [category1, category2]
tags: [tag1, tag2]
description: "One-sentence description."
excerpt_separator: <!--more-->
---
```

The `<!--more-->` tag separates the excerpt (shown on the index) from the full post body. Place it after the first paragraph.

Images go in `assets/images/` and are referenced as `/assets/images/filename.ext`.

## Styles and Design

All styles and design decisions must follow the design from the **Stitch project "Davamix Blog"**. When making any visual or layout changes, refer to that project as the source of truth for colors, typography, spacing, and component styles.


