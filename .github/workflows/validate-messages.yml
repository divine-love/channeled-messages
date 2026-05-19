name: Validate and Generate

on:
  push:
    paths:
      - 'content/messages/**/*.md'
      - 'spirits/**/*.yml'
      - 'mediums/**/*.yml'
  pull_request:
    paths:
      - 'content/messages/**/*.md'
      - 'spirits/**/*.yml'
      - 'mediums/**/*.yml'

jobs:
  validate-and-generate:
    name: Validate and Generate Index Files
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml jsonschema

      - name: Validate message files
        run: python .github/scripts/validate_messages.py

      - name: Generate browse index
        run: python .github/scripts/generate_browse.py

      - name: Generate AI index
        run: python .github/scripts/generate_llms.py

      - name: Generate collection pages
        run: python .github/scripts/generate_collections.py

      - name: Generate essential teachings pages
        run: python .github/scripts/generate_essential_teachings.py

      - name: Commit generated files
        if: github.event_name == 'push'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add content/browse.md llms.txt content/collections/ content/essential-teachings/
          git diff --staged --quiet || git commit -m "chore: regenerate index and collection files [skip ci]"
          git push