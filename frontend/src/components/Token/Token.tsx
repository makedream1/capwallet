import "./Token.css";

const Token = ({
  name,
  img,
  price,
  amount,
  shortName,
}: {
  name: string;
  img: string;
  price: number;
  amount: number;
  shortName: string;
}) => {
  return (
    <li className={"Token"}>
      <img className='tokenImage' src={img} alt={name} />
      <div className="tokenInfo">
        <div className="tokenRate">
          <div className="tokenName">{name}</div>
          {price && <div className="tokenPrice">{price}$</div>}
        </div>
        <div className="tokenTotal">
          <span className="tokenAmount">{amount}</span>
          <span className="tokenName">{shortName}</span>
        </div>
      </div>
    </li>
  );
};

export default Token;
