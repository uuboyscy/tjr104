# Developer Handover: `job-demo` Execution Workflow

## 1. System Overview
This repository contains a Google Cloud Workflows definition (`workflow.yaml`) designed to orchestrate the execution of a serverless Cloud Run job named `job-demo`. Upon completion of the job, the workflow triggers a webhook notification to an external API endpoint.

## 2. Architecture Components
*   **Orchestrator:** Google Cloud Workflows
*   **Target Workload:** Google Cloud Run Job (`job-demo` deployed in `europe-west1`)
*   **Notification Sink:** External API (`https://uuboyscy.dev`)

## 3. Workflow Definition (`workflow.yaml`)
The workflow is defined declaratively using YAML and utilizes the Cloud Run Admin API connector.

### Step Breakdown:
*   `init`: Initializes necessary variables. It dynamically pulls the Google Cloud Project ID from the environment, sets the region, defines the target job name, and configures the notification URL.
*   `execute_cloud_run_job`: Makes a synchronous, authenticated API call to `googleapis.run.v1.namespaces.jobs.run`. The workflow execution blocks/waits at this step until the Cloud Run job finishes executing to ensure sequential processing.
*   `notify_user_via_api`: Issues an HTTP POST request to the configured notification URL. The payload includes a success status and the job name.
*   `final_return`: Returns a JSON object containing the execution results of both the Cloud Run job and the notification API call for logging and auditing within the Workflows console.

## 4. Prerequisites and IAM Roles
To deploy and execute this workflow, the following Google Cloud IAM permissions are required for the Workflow's associated service account:

*   **`roles/run.invoker`** (or `run.jobs.run` permission) on the specific Cloud Run job, to allow the workflow to execute the job.
*   **Network egress:** If the Workflows environment is enforcing VPC Service Controls or restricting egress, ensure outbound HTTPS traffic to `https://uuboyscy.dev` is permitted.

## 5. Deployment Instructions
Ensure you are authenticated with the `gcloud` CLI and have selected the correct project.

Deploy the workflow using the following command:
```bash
gcloud workflows deploy job-demo-workflow \
    --source=workflow.yaml \
    --location=europe-west1
```
*(Note: If you are using a specific service account for the workflow, append `--service-account=<SA_EMAIL>` to the command).*

## 6. Execution and Troubleshooting
*   **Manual Trigger:** The workflow can be triggered manually via the Google Cloud Console, or via the CLI: `gcloud workflows run job-demo-workflow --location=europe-west1`.
*   **Logs:** Execution logs are available in Cloud Logging under the `Workflows` resource type. Both the Cloud Run job output and the HTTP notification response are captured here.
*   **Error Handling (Future Enhancement):** The current iteration assumes a happy path. Future modifications should consider adding `try/except` blocks in the YAML to handle Cloud Run job failures (e.g., timeouts, application crashes) and send a failure notification ping.
