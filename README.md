### setting up deployment environment
rename `gae/scheduler-app/credentials.sample.yaml` and `gcf/scheduled-function/settings.sample.json`

```bash
gcloud config set project test-gcf-scheduling
gcloud auth activate-service-account --key-file=test-gcf-scheduling-key.json

gcloud services enable appengine
gcloud services enable cloudfunctions
```

### deploying GCS resources
```bash
gsutil mb -c regional -l us-central1 gs://gcf-test-scheduling-staging

cat > gcf-test-scheduling-staging-lifecycle.json <<EOL
{
  "rule":
  [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 7}
    }
  ]
}
EOL
gsutil lifecycle set gcf-test-scheduling-staging-lifecycle.json gs://gcf-test-scheduling-staging
```

### deploying GCF resources
```bash
gcloud beta functions deploy scheduled --source=gcf/scheduled-function --stage-bucket gcf-test-scheduling-staging --memory=128MB --region=us-central1 --trigger-http
```

### deploying App Angine resources
```bash
gcloud app deploy gae/scheduler-app/app.yaml
gcloud app deploy gae/scheduler-app/cron.yaml
```
