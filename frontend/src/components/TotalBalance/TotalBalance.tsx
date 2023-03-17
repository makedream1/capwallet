import "./TotalBalance.css";

const TotalBalance = ({
  totalBalance = 0
}: {
  totalBalance: number;
}) => {
  const formatedBalance = totalBalance.toLocaleString("en-US", { maximumFractionDigits: 2, minimumFractionDigits: 2 });
  return (
    <div className={"TotalBalance"}>
      <div className="balance">
        <span className="balance-amount">{formatedBalance}</span>
        <span className="balance-currency">$</span>
      </div>
      <div className="balance-caption"><span className='balance-caption-text'>Общий баланс</span></div>
    </div>
  );
};

export default TotalBalance;
