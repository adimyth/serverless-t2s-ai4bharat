## Deploying Huggingface Models on RunPod

### Languages supported
- Hindi
- Kannada
- Tamil
- Telugu
- Marathi
- Malayalam
- Bengali
- Gujarati
- Punjabi

### Running the project locally

1. Clone the repository
2. Create a virtual environment
```bash
python3.10 -m venv .venv

source .venv/bin/activate
```
3. Install the requirements
```bash
pip install -r builder/requirements.txt
```
4. Download a model. We will only be testing with Hindi. You can opt to download other models as well.
```bash
mkdir models/

wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip && unzip hi.zip -d models/v1 && rm hi.zip
```
5. Install `TTS dependencies`
```bash
git clone https://github.com/adimyth/TTS 
cd TTS && python3.10 -m pip install -e .
```
6. Install `nltk`
```bash
python3.10 -m pip install nltk
python3.10 -c "import nltk; nltk.download('punkt')"
```
7. Modify the `src/handler.py` to only keep hindi model. Remove the other models. from the list. 
```python
# for lang in ["hi", "kn", "ta", "te", "mr", "ml", "bn", "gu", "pa"]:
for lang in ["hi"]:
```
8. Run the project. Refer the [docs](https://docs.runpod.io/serverless/workers/development/overview) for more options. This will start the FastAPI server on the specified host at port 8000.
```bash
python3 src/handler.py --rp_serve_api --rp_api_host 0.0.0.0 --rp_log_level DEBUG
```
9. Test the project
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

### Hosting the model on RunPod

Create the docker image
```bash
docker build -f Dockerfile -t adimyth/serverless-t2s-ai4bharat:v1.0.0 .
```

Push the docker image to dockerhub
```bash
docker push adimyth/serverless-t2s-ai4bharat:v1.0.0
```