import io
import os
import uuid
import soundfile as sf
from TTS.utils.synthesizer import Synthesizer
import runpod
import boto3
from dotenv import load_dotenv

load_dotenv()

# Load the models
models = {}
for lang in ["hi", "te", "ta", "kn"]:
    models[lang] = {}
    models[lang]["synthesizer"] = Synthesizer(
        tts_checkpoint=f"models/v1/{lang}/fastpitch/best_model.pth",
        tts_config_path=f"models/v1/{lang}/fastpitch/config.json",
        tts_speakers_file=f"models/v1/{lang}/fastpitch/speakers.pth",
        vocoder_checkpoint=f"models/v1/{lang}/hifigan/best_model.pth",
        vocoder_config=f"models/v1/{lang}/hifigan/config.json",
        encoder_checkpoint="",
        encoder_config="",
        use_cuda=True,
    )
    print(f"Synthesizer loaded for {lang}...")
    print("*" * 100)
print("TTS models loaded successfully")

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["RUNPOD_SECRET_AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["RUNPOD_SECRET_AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["RUNPOD_SECRET_AWS_REGION"],
)


def handler(event):
    input_data = event.get("input", {})

    # Extract sentence and language
    sentence = input_data["sentence"]
    language = input_data["language"]
    gender = input_data.get("gender", "male")

    # Error handling in case of invalid input
    if not sentence:
        return {"error": "sentence is required"}
    if not language:
        return {"error": "language is required"}
    if language not in ["hi", "te", "ta", "kn"]:
        return {"error": "language not supported"}

    # Get model for the language
    synthesizer = models[language]["synthesizer"]

    # Perform inference
    waveform = synthesizer.tts(sentence, speaker_name=gender, style_wav="")

    # Save the waveform as a wav file
    output = io.BytesIO()
    sf.write(output, waveform, 22050, format="wav")
    output.seek(0)

    # Upload the file to S3
    key = f"{uuid.uuid4()}.wav"
    s3.upload_fileobj(
        output,
        os.environ["RUNPOD_SECRET_S3_BUCKET_NAME"],
        key,
        ExtraArgs={"ContentType": "audio/wav"},
    )
    cdn_url = f"{os.environ['RUNPOD_SECRET_CDN_URL']}/{key}"

    return {"url": cdn_url}


runpod.serverless.start({"handler": handler})
