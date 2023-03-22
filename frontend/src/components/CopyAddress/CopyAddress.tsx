import useCopyToClipboard from "../../hooks/useCopyToClipboard";

import "./CopyAddress.css";

const CopyAddress = ({ token }: { token: string }) => {
  const [value, copy] = useCopyToClipboard();

  return (
    <div className="CopyAddress">
      <div className="copy-text">
        <input id="copy-text" type="text" value={token} readOnly={true} />
      </div>
      <div
        className="copy-button"
        id="copy-button"
        onClick={() => {
          copy(token).catch(() => {
            let copyText = document.querySelector("#copy-text");
            // @ts-ignore
            copyText.select();
            document.execCommand("copy");
          });
          const x = document.getElementById("copy-button");
          x!.innerHTML = "скопировано";
          setTimeout(() => (x!.innerHTML = "копировать"), 1000);
        }}
      >
        копировать
      </div>
    </div>
  );
};

export default CopyAddress;
