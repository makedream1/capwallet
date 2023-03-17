import { useState } from "react";
import { IFormData } from "../../../types/types";

import "./TokenAmountInput.css";

const TokenAmountInput = ({
  totalAmount,
  fee,
  minWithdrawalAmount,
  isRequired,
  formData,
  setFormData,
}: {
  totalAmount: number;
  fee: number;
  minWithdrawalAmount: number;
  isRequired: boolean;
  formData: IFormData;
  setFormData: (val: IFormData) => void;
}) => {
  const [tokenAmount, setTokenAmount] = useState<string>("");
  const [errorText, setErrorText] = useState<string>("");

  const onMaxAmountClick = () => {
    const maxAmount = String((Number(totalAmount) - fee) / 1e9);

    setTokenAmount(maxAmount);
    validateAmount(maxAmount) &&
      setFormData({
        ...formData,
        amount: totalAmount - fee,
      });
  };

  const handleAmountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const amount = event.target.value;
    setTokenAmount(amount);
    if(validateAmount(amount)){
      setFormData({
        ...formData,
        amount: Number(amount) * 1e9,
      });
    } else {
      setFormData({
        ...formData,
        amount: 0,
      });
    }
  };

  const validateAmount = (value: string) => {
    setErrorText("");
    if (!value) return false;
    if (Number(value) * 1e9 > totalAmount - fee) {
      setErrorText("У вас недостаточно токенов");
      return false;
    }
    if (Number(value) * 1e9 < minWithdrawalAmount) {
      setErrorText(
        `Минимальная сумма вывода: ${minWithdrawalAmount / 1e9} ${
          formData.coin
        }`
      );
      return false;
    }
    return true;
  };

  return (
    <div className="TokenAmountInput">
      <div className="amount-input-wrapper">
        <input
          className="send-input amount-input"
          type="number"
          inputMode="decimal"
          value={tokenAmount || ""}
          required={isRequired}
          onChange={handleAmountChange}
        />
        <span onClick={onMaxAmountClick} className="max-amount-button">
          макс
        </span>
      </div>
      <span className="input-error">{errorText}</span>
    </div>
  );
};

export default TokenAmountInput;
