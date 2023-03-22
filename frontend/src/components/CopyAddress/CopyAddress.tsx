import "./CopyAddress.css";

const CopyAddress = ({ token }: { token: string }) => {

  return (
    <div className="CopyAddress">
      <div className="copy-text">
      <input id="copy-text" type="text" value={token} disabled={true} />
      </div>
      <div
        className="copy-button"
        id="copy-button"
        onClick={() => {
          let copyText = document.querySelector("#copy-text");
          // @ts-ignore
          copyText.select();
          document.execCommand("copy");
          const x = document.getElementById("copy-button");
          x!.innerHTML = "скопировано";
          setTimeout(() => (x!.innerHTML = "копировать"), 1000);
          // navigator.clipboard.writeText(token);
        }}
      >
        копировать
      </div>
    </div>
  );
};

export default CopyAddress;
