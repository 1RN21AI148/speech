import React, { useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import apiJson from './services/apiJson';
import axios from './services/axiosInstance';

const Dictaphone = () => {

  const [recData, setRecData] = useState('')

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  const stopClicked = async () => {
    SpeechRecognition.stopListening();
    const requestObject = {...apiJson['getCommandData']};
    requestObject.data = {
      "data": transcript
    }
    console.log('request object',requestObject)
    try {
      const response = await axios(requestObject)
      console.log('response',response.data)
      setRecData(response.data.data)

    } catch (error) {
      console.log(error)
    }
  }

  return (
    <div>
      <p>Microphone: {listening ? 'on' : 'off'}</p>
      <button onClick={SpeechRecognition.startListening}>Start</button>
      <button onClick={stopClicked}>Stop</button>
      <button onClick={resetTranscript}>Reset</button>
      <p>{transcript}</p>
      {recData && <p>{recData}</p>}
    </div>
  );
};
export default Dictaphone;