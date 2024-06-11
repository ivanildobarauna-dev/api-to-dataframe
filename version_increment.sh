#!/bin/bash

read -p "Increment Patch Version'? (s/N): " response

if [[ "$response" =~ ^([sS][iI][mM]|[sS])$ ]]; then
  poetry version patch
  git add pyproject.toml
  echo "Incremented Version and pyproject.toml added for commit."
else
  echo "Version not incremented."
fi
