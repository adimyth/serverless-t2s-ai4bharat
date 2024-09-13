## Deploying Huggingface Models on RunPod

### Running the project

1. Clone the repository
2. Install the requirements
```bash
pip install -r builder/requirements.txt
```
3. Run the project. Refer the [docs](https://docs.runpod.io/serverless/workers/development/overview) for more options. This will start the FastAPI server on the specified host at port 8000.
```bash
python3 src/handler.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_log_level DEBUG
```
4. Test the project
```bash
curl --location 'http://0.0.0.0:8000/runsync' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "input": {"sentence": "प्रत्येक व्यक्ति को शिक्षा का अधिकार है । शिक्षा कम से कम प्रारम्भिक और बुनियादी अवस्थाओं में निःशुल्क होगी ।", "language": "hi"}
}'
```

> [!IMPORTANT]
> It seems as if the `runsync` endpoint only returns JSON Response, even though it uses FastAPI to serve the model as an API. Hence, in the handler I have added an additional step to store the file to S3 & return the CDN URL. This is a workaround to the issue.

> [!NOTE]
> I am passing the AWS Creds (refer `src/.env.example`) as secrets. Runpod requires secrets to be prefixed with `RUNPOD_SECRET_`. Refer the [docs](https://docs.runpod.io/pods/templates/secrets) for more information.