import React, { useState, useEffect } from "react";

var a;
const AudioPlay = () => {
  const [buttonName, setButtonName] = useState("Play");

  const [audio, setAudio] = useState();

  useEffect(() => {
    if (a) {
      a.pause();
      a = null;
      setButtonName("Play");
    }
    if (audio) {
      a = new Audio(audio);
      a.onended = () => {
        setButtonName("Play");
      };
    }
  }, [audio]);

  const handleClick = () => {
    if (buttonName === "Play") {
      a.play();
      setButtonName("Pause");
    } else {
      a.pause();
      setButtonName("Play");
    }
  };

  const addFile = (e) => {
    if (e.target.files[0]) {
      setAudio(URL.createObjectURL(e.target.files[0]));
    }
  };

  return (
    <div>
      <button onClick={handleClick}>{buttonName}</button>
      <input type="file" onChange={addFile} />
    </div>
  );
};

export default AudioPlay;
