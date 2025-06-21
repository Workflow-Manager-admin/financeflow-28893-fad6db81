#!/bin/bash
cd /home/kavia/workspace/code-generation/financeflow-28893-fad6db81/expense_frontend_workspace/expense_frontend
npm run lint
ESLINT_EXIT_CODE=$?
npm run build
BUILD_EXIT_CODE=$?
if [ $ESLINT_EXIT_CODE -ne 0 ] || [ $BUILD_EXIT_CODE -ne 0 ]; then
   exit 1
fi

