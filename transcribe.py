import os
import csv
from tqdm import tqdm
import assemblyai as aai


def setup_transcriber(api_key):
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(
        language_code="en",
        speaker_labels=True,
        word_boost=["TEMI"],
        disfluencies=True
    )
    return aai.Transcriber(config=config)


def process_file(file, transcriber):
    transcript = transcriber.transcribe(f"Audio files/{file}")
    participant = os.path.splitext(os.path.basename(file))[0].split()[1]
    output_filename = f"Transcription {participant}.csv"

    return output_filename, transcript, participant


def write_transcription(output_filename, transcript, participant):
    os.makedirs("Transcriptions", exist_ok=True)
    with open(f"Transcriptions/{output_filename}", mode='w', newline='') as csv_file:
        fieldnames = ["start (in ms)", "speaker", "text"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for utterance in transcript.utterances:
            if utterance.speaker == "A":
                speaker = participant
            elif utterance.speaker == "B":
                speaker = "TEMI"
            else:
                speaker = "UNIDENTIFIED"

            writer.writerow({"start (in ms)": utterance.start, "speaker": speaker, "text": utterance.text})


def main():
    transcriber = setup_transcriber("d6db0f1589054dcd821af1456e348b1f")
    files = os.listdir("Audio files")

    for file in tqdm(files, desc="Transcribing audio files"):
        output_filename, transcript, participant = process_file(file, transcriber)
        write_transcription(output_filename, transcript, participant)
        print(f"\nFinished transcribing -> {file}")


if __name__ == "__main__":
    main()
