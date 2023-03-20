import "./TotalBalance.css";

const TotalBalance = ({
  totalBalance = 0
}: {
  totalBalance: number;
}) => {
  const formatedBalance = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(totalBalance);
  return (
    <div className={"TotalBalance"}>
      <div className="balance">
        <span className="balance-amount">{formatedBalance}</span>
      </div>
      <div className="balance-caption"><span className='balance-caption-text'>Общий баланс</span></div>
    </div>
  );
};

export default TotalBalance;
