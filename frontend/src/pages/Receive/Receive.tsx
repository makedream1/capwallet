import { useState } from "react";

import BigButton from "../../components/Buttons/BIgButtonLink/BigButtonLink";
import TokenSelectBox from "../../components/TokenSelectBox/TokenSelectBox";
import CopyAddress from "../../components/CopyAddress/CopyAddress";
import QRCode from "../../components/QRCodeImage/QRCodeImage";

import { IToken } from "../../types/types";

import "./Receive.css";


const Receive = ({
  data,
}: {
  data: { status: string; data: {}; error?: string };
}) => {

  const [tokenId, setSelectedTokenId] = useState<string>();
  const [tokenAddress, setSelectedTokenAddress] = useState<string>("");
  const [tokenImg, setSelectedTokenImg] = useState<string>("");
  const [tokenNetwork, setSelectedTokenNetwork] = useState<{
    name: string;
    shortName: string;
  }>({ name: "", shortName: "" });

  // @ts-ignore
  const tokens: IToken[] =
    data &&
    // @ts-ignore
    data.data["wallets"].map((wallet: any) => {
      return {
        id: wallet.address,
        amount: wallet.balance,
        name: wallet.coin.name,
        shortName: wallet.coin.short_name,
        img: wallet.coin.get_image,
        address: wallet.address,
        networkName: wallet.network.name,
        networkShortName: wallet.network.short_name,
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
