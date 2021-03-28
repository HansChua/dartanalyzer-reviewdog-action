# GitHub Action: Run dartanalyzer with reviewdog

This action runs [dartanalyzer](https://dart.dev/tools/dart-analyze) with [reviewdog](https://github.com/reviewdog/reviewdog).

## Additional Requirements

Python 3

## Inputs

#### `github_token`

**Required**. Must be in form of `github_token: ${{ secrets.github_token }}`.

#### `level`

Optional. Report level for reviewdog [`info`,`warning`,`error`].
It's same as `-level` flag of reviewdog.
The default is `error`.

#### `reporter`

Optional. Reporter of reviewdog command [`github-check`, `github-pr-check`,`github-pr-review`].
The default is `github-check`.

#### `filter_mode`
Optional. Filter mode of reviewdog command [`added`,`diff_context`,`file`,`nofilter`]
Default is `added`.

#### `reviewdog_flags`

Optional. Additional flags to be passed to reviewdog cli.
The default is ``.

#### `workdir`

Optional. The directory from which to run dartanalyzer.
Default `.`.

## Example usage

```yml
name: reviewdog
on: [pull_request]
jobs:
  dartanalyzer:
    name: Check Code Quality
    runs-on: ubuntu-latest

    steps:
      - name: Clone repo
        uses: actions/checkout@main
        with:
          fetch-depth: 1
      - name: Setup Dart SDK
        uses: dart-lang/setup-dart@v1
        with:
          sdk: stable
      - name: Setup python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
          architecture: x64
      - name: Setup Flutter env
        uses: subosito/flutter-action@v1
        with:
          flutter-version: '2.0.3'
      - name: Run dartanalyzer
        uses: HansChua/dartanalyzer-reviewdog-action@main
        with:
          github_token: ${{ secrets.github_token }}
          reporter: github-pr-review # Change reporter
```
