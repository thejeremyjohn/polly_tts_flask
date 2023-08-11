from flask import Flask, Response, request, jsonify
import boto3

app = Flask(__name__)


@app.route('/synthesize_speech', methods=['GET'])
def synthesize_speech():
    polly = boto3.client('polly')
    args = request.args
    text = args.get('text', 'Hello World!')
    voice_id = args.get('voice_id', 'Joanna')
    output_format = args.get('output_format', 'mp3')
    engine = args.get('engine', 'standard')
    response = polly.synthesize_speech(
        Text=text, OutputFormat=output_format, VoiceId=voice_id, Engine=engine)
    audio_stream = response['AudioStream'].read()
    return Response(audio_stream, mimetype='audio/mpeg')


@app.route('/describe_voices', methods=['GET'])
def describe_voices():
    polly = boto3.client('polly')
    voices = []
    response = polly.describe_voices()
    voices.extend(response['Voices'])
    while 'NextToken' in response:
        response = polly.describe_voices(NextToken=response['NextToken'])
        voices.extend(response['Voices'])
    return jsonify(voices)


if __name__ == '__main__':
    app.run(debug=True)
