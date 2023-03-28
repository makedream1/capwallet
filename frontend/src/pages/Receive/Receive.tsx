import { useState } from "react";

import BigButton from "../../components/Buttons/BIgButtonLink/BigButtonLink";
import TokenSelectBox from "../../components/TokenSelectBox/TokenSelectBox";
import CopyAddress from "../../components/CopyAddress/CopyAddress";
import QRCode from "../../components/QRCodeImage/QRCodeImage";

import { IFetchData, IToken } from "../../types/types";

import "./Receive.css";
import { Navigate } from "react-router-dom";

const Receive = ({ data }: { data: IFetchData }) => {
  const [tokenId, setSelectedTokenId] = useState<string>();
  const [tokenAddress, setSelectedTokenAddress] = useState<string>("");
  const [tokenImg, setSelectedTokenImg] = useState<string>("");
  const [tokenNetwork, setSelectedTokenNetwork] = useState<{
    name: string;
    shortName: string;
  }>({ name: "", shortName: "" });
  if (!data["wallets"]) {
    return <Navigate replace to="/" />;
  }

  const tokens: IToken[] =
    data &&
    data["wallets"].map((wallet: any) => {
      return {
        id: wallet.address,
        amount: wallet.balance,
        min_withdraw_limit: wallet.min_withdraw_limit,
        name: wallet.coin.name,
        shortName: wallet.coin.short_name,
        img: wallet.coin.get_image,
        address: wallet.address,
        networkName: wallet.network.name,
        networkShortName: wallet.network.short_name,
        gas_fee: wallet.withdrawal_fee,
      };
    });

  const changingSelectedToken = (id: string) => {
    tokens
      .filter((token) => token.id === id)
      .map((selectedToken) => {
        setSelectedTokenId(selectedToken.id);
        setSelectedTokenAddress(selectedToken.address);
        setSelectedTokenImg(selectedToken.img);
        setSelectedTokenNetwork({
          name: selectedToken.networkName,
          shortName: selectedToken.networkShortName,
        });
      });
  };

  return (
    <>
      <section className="Receive">
        {!data ? (
          <div></div>
        ) : (
          <TokenSelectBox
            onChange={changingSelectedToken}
            isDisabled={false}
            tokens={tokens}
            isRequired={true}
          />
        )}
        {tokenAddress && (
          <>
            <QRCode
              token={tokenAddress}
              tokenImg={tokenImg}
              key={tokenId}
              network={tokenNetwork}
            />
            <CopyAddress token={tokenAddress} />
          </>
        )}

        <BigButton link={""} caption={"Вернуться в кошелек"} />
      </section>
    </>
  );
};

export default Receive;
