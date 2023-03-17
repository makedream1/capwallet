import { useState } from "react";

import TokenSelectBox from "../../components/TokenSelectBox/TokenSelectBox";
import TokenAmountInput from "../../components/Inputs/TokenAmountInput/TokenAmountInput";
import AddressInput from "../../components/Inputs/AddressInput/AddressInput";

import "./SendTokenForm.css";
import { IFormData, IToken } from "../../types/types";

const SendTokenForm = ({
  userId,
  formData,
  setFormData,
  tokens,
}: {
  userId: string;
  formData: IFormData;
  tokens: IToken[];
  setFormData: (val: IFormData) => void;
}) => {
  const [tokenId, setSelectedTokenId] = useState<string>();
  const [amount, setAmount] = useState<number>(0);
  const [fee, setFee] = useState<number>(0);
  const [minWithdrawal, setMinWithdrawal] = useState<number>(0);
  const [networkShortName, setNetworkShortName] = useState<string>("");

  const changingSelectedToken = (id: string) => {
    tokens
      .filter((token) => token.id === id)
      .map((selectedToken) => {
        setSelectedTokenId(selectedToken.id);
        setAmount(selectedToken.amount);
        setMinWithdrawal(selectedToken.min_withdraw_limit);
        setFee(selectedToken.gas_fee);
        setNetworkShortName(selectedToken.networkShortName);
        setFormData({
          ...formData,
          user_id: userId,
          source: selectedToken.address,
          gas_fee: selectedToken.gas_fee,
          coin: selectedToken.shortName,
          network: selectedToken.networkShortName,
        });
      });
  };

  return (
    <>
      <TokenSelectBox
        onChange={changingSelectedToken}
        isDisabled={false}
        tokens={tokens}
        isRequired={true}
      />
      {tokenId && (
        <>
          <div className="send-container">
            <p className="send-title">Укажите сумму</p>
            <p className="send-subtitle-text">
              Комиссия {fee / 1e9} {networkShortName}
            </p>
            <TokenAmountInput
              totalAmount={amount}
              fee={fee}
              minWithdrawalAmount={minWithdrawal}
              formData={formData}
              setFormData={setFormData}
              isRequired={true}
            />
          </div>

          <div className="send-address-container">
            <p className="send-title">Адрес</p>
            <p className="send-subtitle-text">
              Используйте сеть для отправки {networkShortName}
            </p>
            <AddressInput
              networkShortName={networkShortName}
              addressLength={tokenId.length}
              formData={formData}
              setFormData={setFormData}
              isDisabled={false}
              isRequired={true}
            />
          </div>
        </>
      )}
    </>
  );
};

export default SendTokenForm;
