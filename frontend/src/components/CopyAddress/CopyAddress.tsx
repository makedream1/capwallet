import "./CopyAddress.css";

const CopyAddress = ({ token }: { token: string }) => {
  return (
    <div className="CopyAddress">
      <div className="copy-text">
        <input id="copy-text" type="text" value={token} readOnly={true} />
      </div>
      <div
        className="copy-button"
        id="copy-button"
        onClick={() => {
          const copyText = document.querySelector("#copy-text");
          // @ts-ignore
          copyText.select();
          document.execCommand("copy");
          const copyBtn = document.getElementById("copy-button");
          copyBtn!.innerHTML = "скопировано";
          setTimeout(() => (copyBtn!.innerHTML = "копировать"), 1000);
        }}
      >
        копировать
      </div>
    </div>
  );
};

export default CopyAddress;
