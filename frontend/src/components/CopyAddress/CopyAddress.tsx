import useCopyToClipboard from "../../hooks/useCopyToClipboard";

import "./CopyAddress.css";

const CopyAddress = ({ token }: { token: string }) => {
  const [value, copy] = useCopyToClipboard();

  return (
    <div className="CopyAddress">
      <div className="copy-text">{token}</div>
      <div className="copy-button" onClick={() => copy(token)}>
        copy
      </div>
    </div>
  );
};

export default CopyAddress;
