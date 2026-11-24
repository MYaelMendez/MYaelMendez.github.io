"""SDK speaker bridge: play a 16-bit PCM WAV on a configured Asimov speaker.

Follows menlo-sdk examples/play_audio.py: Robot().connect(require_state=False),
robot.has('speaker'), then robot.speaker.play_pcm(pcm, sample_rate_hz, channels)
in 1-second chunks. Returns JSON. Never contacts a robot in local mode.
"""
import sys, wave, json

def main():
    path = sys.argv[1]
    try:
        from menlo.asimov import Robot
    except Exception as e:
        print(json.dumps({'success': False, 'error': f'menlo-sdk unavailable: {e}'})); return
    try:
        with wave.open(path, 'rb') as w:
            if w.getsampwidth() != 2:
                print(json.dumps({'success': False, 'error': 'WAV is not 16-bit PCM'})); return
            rate, channels = w.getframerate(), w.getnchannels()
            pcm = w.readframes(w.getnframes())
        with Robot().connect(require_state=False) as robot:
            if not robot.has('speaker'):
                print(json.dumps({'success': False, 'error': 'no speaker on this connection; use hybrid/livekit'})); return
            step = int(rate * 1.0) * 2 * channels
            for start in range(0, len(pcm), step):
                robot.speaker.play_pcm(pcm[start:start+step], sample_rate_hz=rate, channels=channels)
        print(json.dumps({'success': True, 'mode': 'sdk', 'played_s': round(len(pcm)/(2*channels*rate), 3),
                          'sample_rate_hz': rate, 'channels': channels, 'wav': path}))
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)[:500]}))

if __name__ == '__main__':
    main()
