# -*- coding: utf-8 -*-
#!/usr/bin/env3 python
# [START import_libraries]
from __future__ import division
import sys
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from konlpy.tag import Twitter
import requests
import os


twitter = Twitter()
# [END import_libraries]

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
'''=================Custom Parameter ======================='''
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\hjpark\Desktop\LoRa-AISpeaker-seminar\CODE\hjpark-1020-562fbb05f3b5.json"
myIp = 'http://192.168.0.145' # INPUT_YOUR_WEMOS_IP

urlList = [
    myIp+'/first_floor_off',
    myIp+'/first_floor_on',
    myIp+'/second_floor_off',
    myIp+'/second_floor_on',
    '분석 실패하여 Log 를 저장합니다.'
]
# 동사 목록
# frame : ['형태소원형','URL weight']
verbList = [
    ['끄다',0],
    ['켜다',1]
]
# 명사 목록
nounList = [
    # 명령어, 대답
    ['위층',2],
    ['윗층',2],
    ['위',2],
    ['아래층',0],
    ['아렛층',0],
    ['밑',0],
]
# 1층 으로 인식될떄의 1에대한 Number 형태소
numberList = [
    ['1',0],
    ['2',2]
]
def getUrl(nounWeight,numberWeight,verbWeight):
    urlResult = -1
    if nounWeight == -1 and numberWeight != -1 and verbWeight != -1:  # 숫자로 말한경우
        urlResult = numberWeight + verbWeight
    elif nounWeight != -1 and numberWeight == -1 and verbWeight != -1:
        urlResult = nounWeight + verbWeight

    return urlResult

def getWeightNoun(dicts):
    print(">>> 명사(Noun )  형태소: ", end='')
    nounWeight = -1
    for d in dicts:
        if d[1] == 'Noun':
            for n in nounList:
                if d[0] == n[0]:
                    nounWeight = n[1]
            print(d, end=',')
    print()
    return nounWeight
def getWeightNumber(dicts):
    print(">>> 숫자(Number) 형태소: ", end='')
    numberWeight = -1
    for d in dicts:
        if d[1] == 'Number':
            print(d, end=',')
            for n in numberList:
                if d[0] == n[0]:
                    numberWeight = n[1]
    print()
    return numberWeight

def getWeightVerb(dicts):
    print(">>> 동사(Verb)   형태소: ", end='')
    verbWeight = -1
    for d in dicts:
        if d[1] == 'Verb':
            print(d, end=',')
            for v in verbList:
                if d[0] == v[0]:
                    verbWeight = v[1]
    print()
    return verbWeight


'''========================================================='''
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]
"""
리턴이 0이면 종료
"""
def CommandProc(stt):
    # 문자 양쪽 공백 제거
    cmd = stt.strip().replace(' ','')
    # 입력 받은 문자 화면에 표시
    print('나 : ' + cmd)

    #NLP get weight
    dicts = twitter.pos(cmd, norm=True, stem=True)

    print(">>> 전체 형태소        : ",dicts)
    nounWeight = getWeightNoun(dicts)
    numberWeight = getWeightNumber(dicts)
    verbWeight = getWeightVerb(dicts)
    print(">>> Weight 값        : Noun = {}, Number = {}, Verb = {}".
        format(nounWeight, numberWeight, verbWeight))
    urlResult = getUrl(nounWeight,numberWeight,verbWeight)

    # 결과
    print(">>> GET : ",urlList[urlResult])
    try:
        requests.get(urlList[urlResult])
    except:
        pass
    print("___"*30) # 줄 분리

    return 1 # 60초 동안 계속 사용하기위해
def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # There could be multiple results in each response.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            #### 추가 ### 화면에 인식 되는 동안 표시되는 부분.
            sys.stdout.write('나 : ')
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            #### 추가 ###
            if CommandProc(transcript) == 0:
                break;
            """
                # 원래 있던 코드는 주석처리
                print(transcript + overwrite_chars)
                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break
            """
            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    #language_code = 'en-US'  # a BCP-47 language tag
    language_code = 'ko-KR'  # 한국어로 변경
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)
        # Now, put the transcription responses to use.
        listen_print_loop(responses)

if __name__ == '__main__':
    main()