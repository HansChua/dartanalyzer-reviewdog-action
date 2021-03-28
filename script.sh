#!/bin/sh

cd "${GITHUB_WORKSPACE}/${INPUT_WORKDIR}" || exit 1

TEMP_PATH="$(mktemp -d)"
PATH="${TEMP_PATH}:$PATH"

if "$(python -V)" =~ "Python 3" ; then
  python -V
else
  echo 'This repository was not configured for python3, process done.'
  exit 1
fi

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

echo 'Installing reviewdog'
curl -sfL https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh | sh -s -- -b "${TEMP_PATH}" "${REVIEWDOG_VERSION}" 2>&1

echo "Install dartcop (dartanalyzer wrapper)"
curl -fSL https://github.com/HansChua/dartcop/raw/master/src/dartcop/dartcop.py -o "${TEMP_PATH}/dartcop" \
    && chmod +x "${TEMP_PATH}/dartcop"

dartcop --options analysis_options.yaml ${INPUT_WORKDIR}

echo "$(<output_checkstyle.xml)" | reviewdog -f=checkstyle -name="dartanalyzer" -reporter="${INPUT_REPORTER}" -filter-mode="${INPUT_FILTER_MODE}" -level="${INPUT_LEVEL}" ${INPUT_REVIEWDOG_FLAGS}

reviewdog_rc=$?
exit $reviewdog_rc
