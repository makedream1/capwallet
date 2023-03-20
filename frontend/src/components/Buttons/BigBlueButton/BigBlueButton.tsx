import "./BigBlueButton.css";

const BigBlueButton = ({
  type,
  caption,
  onClick,
  isDisabled
}: {
  type: "button" | "submit" | "reset" | undefined;
  caption: string;
  state?: {};
  isDisabled: boolean;
  onClick: any;
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      style={ isDisabled ? { backgroundColor: "#799fc6"} : {}}
      className="BigBlueButton"
    >
      <span className="BigBlueButtonCaption">{caption}</span>
    </button>
  );
};

export default BigBlueButton;
