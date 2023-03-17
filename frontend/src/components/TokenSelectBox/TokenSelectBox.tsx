import Select from "react-select";
import { IToken, ITokenSelectBox } from "../../types/types";

import "./TokenSelectBox.css";

const TokenSelectBox: React.FC<ITokenSelectBox> = ({
  onChange,
  tokens,
  isDisabled,
  isRequired,
}) => {
  const options =
    tokens &&
    tokens.map((token) => {
      return {
        value: `${token.id}`,
        label: (
          <div className="token-select-option" key={token.id}>
            <div className="token-container">
              <img className="token-image" src={token.img} />
              <span>{token.name}</span>
            </div>
            <div className="token-amount-shortName">
              <span>{token.amount / 1e9}</span> <span>{token.shortName}</span>
            </div>
          </div>
        ),
      };
    });
  return (
    <div className="TokenSelectBox">
      <p className="token-select-label">Выберите токен</p>
      <Select
        isDisabled={isDisabled}
        options={options}
        placeholder={"Выберите токен"}
        isSearchable={false}
        required={isRequired}
        onChange={(value) => {
          if (value && onChange) {
            onChange(value?.value);
          }
        }}
      />
    </div>
  );
};

export default TokenSelectBox;
