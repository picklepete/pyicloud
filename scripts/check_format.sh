./scripts/common.sh

if ! hash python3; then
    echo "python3 is not installed"
    exit 0
fi

ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "36" ]; then
    echo "This script requires python 3.6 or greater"
    exit 0
fi

pip install black==19.10b0

black --check --fast .
