import { useEffect, useRef } from "react";

import "./QRCodeImage.css";

import QRCodeStyling from "qr-code-styling";

const qrCode = new QRCodeStyling({
  width: 210,
  height: 210,
  type: "svg",
  qrOptions: { errorCorrectionLevel: "H" },
  dotsOptions: {
    color: "#5eb5ea",
    type: "rounded",
  },
  cornersDotOptions: {
    type: "dot",
  },
  cornersSquareOptions: { type: "dot" },
});

const QRCodeImage = ({
  token
}: {
  token: string;
  tokenImg: string;
  network: {name:string, shortName: string};
}) => {
  const ref = useRef(null);

  useEffect(() => {
    ref.current && qrCode.append(ref.current);
  }, []);

  useEffect(() => {
    qrCode.update({
      data: token,
    });
    const svg = document.getElementsByClassName('qrCode-container').item(0)!.firstElementChild;
    qrCode && svg && (
     svg.setAttribute('viewBox', "0 0 210 210")
    );

  }, [token]);

  return (
    <div className="qrCode-wrapper">
      <div className="qrCode-title-container">
        <span>Отсканируйте QR-code или используйте адрес ниже</span>
      </div>
      <div className="qrCode-container" ref={ref} />
    </div>
  );
};

export default QRCodeImage;
