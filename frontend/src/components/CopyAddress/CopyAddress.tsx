import useCopyToClipboard from "../../hooks/useCopyToClipboard";

import "./CopyAddress.css";

const CopyAddress = ({ token }: { token: string }) => {
  const [value, copy] = useCopyToClipboard();

  return (
    <div className="CopyAddress">
      <div className="copy-text">{token}</div>
      <div className="copy-button" id='copy-button' onClick={() => {
        copy(token);
        const x = document.getElementById("copy-button");
        x!.innerHTML='скопировано';
        setTimeout(()=>x!.innerHTML='копировать', 1000);
        }}>
        копировать
      </div>
    </div>
  );
};

export default CopyAddress;
