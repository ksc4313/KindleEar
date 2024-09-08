#!/bin/bash
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
  echo ""
  read -p "Please input your project ID: " GOOGLE_CLOUD_PROJECT
  if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo "Error: Project ID cannot be empty."
    exit 1
  fi
  export GOOGLE_CLOUD_PROJECT
fi
gcloud config set project $GOOGLE_CLOUD_PROJECT
if ! gcloud app describe >/dev/null 2>&1; then
  gcloud app create   #select a region for app if it's first time
fi

SH_DIR="$(dirname "$0")"
KE_DIR="$(dirname "$SH_DIR")"

if ! python3 ${SH_DIR}/update_req.py gae[$@]; then
  echo "Error: Update requirements failed. The deployment is terminated."
  exit 1
fi

echo -e "\nDownloading the latest recipe collection..."
rm -rf ${KE_DIR}/calibre
git clone --depth 1 https://github.com/kovidgoyal/calibre ${KE_DIR}/calibre
rm -f ${KE_DIR}/application/recipes/builtin_recipes.*
mv -f ${KE_DIR}/calibre/recipes/*.recipe ${KE_DIR}/application/recipes/
rm -rf ${KE_DIR}/calibre
python3 -m venv ${KE_DIR}/myenv
source ${KE_DIR}/myenv/bin/activate
pip3 install --upgrade pip
pip3 install --no-cache-dir -q -r ${KE_DIR}/requirements.txt
python3 ${KE_DIR}/tools/archive_builtin_recipes.py -q
rm -f ${KE_DIR}/application/recipes/*.recipe > /dev/null 2>&1
deactivate
rm -rf ${KE_DIR}/myenv

echo -e "\nEnabling APIs..."
gcloud services enable firestore.googleapis.com datastore.googleapis.com \
cloudtasks.googleapis.com cloudscheduler.googleapis.com appenginereporting.googleapis.com \
artifactregistry.googleapis.com cloudbuild.googleapis.com cloudtrace.googleapis.com \
containerregistry.googleapis.com firebaserules.googleapis.com logging.googleapis.com \
pubsub.googleapis.com storage-api.googleapis.com
gcloud logging buckets update _Default --location=global --retention-days=7

if ! gcloud beta app deploy --version=1 ${KE_DIR}/app.yaml ${KE_DIR}/worker.yaml; then
  echo "The deployment is terminated."
  exit 1
fi

gcloud beta app deploy --quiet --version=1 ${KE_DIR}/cron.yaml
gcloud beta app deploy --quiet --version=1 ${KE_DIR}/queue.yaml
gcloud beta app deploy --quiet --version=1 ${KE_DIR}/dispatch.yaml

echo -e "\nDeleting repositories (build cache)..."
REPOS=$(gcloud beta artifacts repositories list 2>/dev/null)
REPO=$(echo "$REPOS" | grep -oP '(?<=REPOSITORY: ).*')
LOC=$(echo "$REPOS" | grep -oP '(?<=LOCATION: ).*')
if [[ -n "$REPO" && -n "$LOC" ]]; then
  gcloud beta artifacts repositories delete $REPO --location=$LOC --quiet
else
  echo "REPO or LOC is empty. Skipping delete command."
  echo "You can delete manually artifacts in https://console.cloud.google.com/artifacts"
fi

echo "The deployment is completed."
echo "The access address is: https://$GOOGLE_CLOUD_PROJECT.appspot.com"
