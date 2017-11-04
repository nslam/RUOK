import soundfile as sf


data, samplerate = sf.read('output.wav')
sf.write('output.flac', data, samplerate)
