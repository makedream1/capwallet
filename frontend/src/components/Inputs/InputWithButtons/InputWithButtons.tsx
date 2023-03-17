import { useState } from 'react';
import "./InputWithButtons.css";

const InputWithButtons = () => {
  const [address, setAddress] = useState<string>("");
  return (
    <div className="InputWithButtons">
      <input
        className="inputButton-input"
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />
      <span className="inputButton-button">
        <span>Вставить</span>
      </span>
      <span
        className="inputButton-button"
        // onClick={() => handleScanClick(networkShortName)}
      >
        scan
      </span>
    </div>
  );
};

export default InputWithButtons;
