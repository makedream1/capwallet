import { useEffect, useRef } from "react";

import "./QRCodeImage.css";

import QRCodeStyling from "qr-code-styling";
import useCopyToClipboard from "../../hooks/useCopyToClipboard";

const qrCode = new QRCodeStyling({
  width: 210,
  height: 210,
  type: "svg",
  qrOptions: { errorCorrectionLevel: "H" },
  // imageOptions: {
  //   hideBackgroundDots: true,
  //   imageSize: 0.4,
  //   margin: 2,
  // },
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
  token,
  // tokenImg,
  network
}: {
  token: string;
  tokenImg: string;
  network: {name:string, shortName: string};
}) => {
  const [value, copy] = useCopyToClipboard();
  const ref = useRef(null);

  useEffect(() => {
    ref.current && qrCode.append(ref.current);
  }, []);

  useEffect(() => {
    qrCode.update({
      data: token,
      // image: tokenImg,
    });
  }, [token]);

  return (
    <div className="qrCode-wrapper">
      <p className="receive-token-subtitle">
        Используйте сеть {network.name} ({network.shortName})
      </p>

      <div className="qrCode-title-container">
        <span>Отсканируйте QR-code или используйте адрес ниже</span>
      </div>
      <div className="qrCode-container" onClick={() => copy(token)}>
        <div ref={ref} />
      </div>
    </div>
  );
};

export default QRCodeImage;
