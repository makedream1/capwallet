import "./TokenList.css";

import Token from "../Token/Token";
interface IToken {
  id: string;
  name: string;
  img: string;
  price: number;
  shortName: string;
  amount: number;
}

const TokenList = ({ wallets }: { wallets: any[] }) => {
  const tokens =
    wallets &&
    wallets.map((wallet: any) => {
      return {
        id: wallet.address,
        amount: wallet.wallet_balance,
        name: wallet.coin.name,
        shortName: wallet.coin.short_name,
        img: wallet.coin.get_image,
        price: wallet.coin.price,
      };
    });

  return (
    <div className="Content">
      <h3 className="tokenListTitle">Токены</h3>
      {!wallets ? (
        <div></div>
      ) : (
        <ul className="Tokens">
          {tokens.map((token: IToken) => {
            return (
              <Token
                key={token.id}
                name={token.name}
                img={token.img}
                price={token.price}
                shortName={token.shortName}
                amount={token.amount}
              />
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default TokenList;
