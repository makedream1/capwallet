import { useState } from "react";

import { useTelegram } from "../../../hooks/useTelegram";

import icon_qr_scan from "../../../assets/images/icon_qr_scan.svg";

import "./AddressInput.css";
import { IFormData } from "../../../types/types";

const { tg } = useTelegram();

const AddressInput = ({
  networkShortName,
  addressLength,
  isDisabled,
  isRequired,
  formData,
  setFormData,
}: {
  networkShortName: string;
  addressLength: number;
  isDisabled: boolean;
  isRequired: boolean;
  formData: IFormData;
  setFormData: (val: IFormData) => void;
}) => {
  const [errorText, setErrorText] = useState<string>("");
  const [destinationAddress, setDestAddress] = useState<string>("");

  const handleScanClick = (shortName: string) => {
    tg.showScanQrPopup({ text: `Наведите на QR-код c адресом ${shortName}` });
  };
  tg.onEvent("qrTextReceived", (qr: { data: string }) => {
    setDestAddress(qr.data);
    validateAddress(qr.data) &&
      setFormData({ ...formData, destination: qr.data });
    tg.closeScanQrPopup();
  });

  const validateAddress = (value: string) => {
    setErrorText("");
    if (!value) return false;
    if (value.length !== addressLength) {
      setErrorText("Укажите валидный адрес");
      return false;
    }
    return true;
  };

  const handleChangeAddress = (event: React.ChangeEvent<HTMLInputElement>) => {
    const address = event.target.value;
    setDestAddress(event.target.value);
    if (validateAddress(address)) {
      setFormData({
        ...formData,
        destination: address,
      });
    } else {
      setFormData({
        ...formData,
        destination: "",
      });
    }
  };

  return (
    <>
      <div className="AddressInput-wrapper">
        <input
          className="AddressInput-input"
          type="text"
          value={destinationAddress}
          onChange={(e) => handleChangeAddress(e)}
          disabled={isDisabled}
          required={isRequired}
        />
        <img
          className="AddressInput-button"
          src={icon_qr_scan}
          alt="qr-scan"
          onClick={() => handleScanClick(networkShortName)}
        ></img>
      </div>
      <span className="input-error">{errorText}</span>
    </>
  );
};

export default AddressInput;
