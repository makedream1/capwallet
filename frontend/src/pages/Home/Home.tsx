import CircleButtonLink from "../../components/Buttons/CircleButtonLink/CircleButtonLink";
import TokenList from "../../components/TokenList/TokenList";
import TotalBalance from "../../components/TotalBalance/TotalBalance";
import { IFetchData } from '../../types/types';

import receiveImg from "./../../assets/images/icon_receive.svg";
import sendImg from "./../../assets/images/icon_send.svg";

import "./Home.css";

const Home = ({ data }: { data: IFetchData }) => {
  return (
    <section className="Home">
      <div className="wrapper-balance-buttons">
        {!data ? (
          <div></div>
        ) : (
          <TotalBalance totalBalance={data && data["total_balance"]} />
        )}

        <div className="action-buttons">
          <CircleButtonLink
            link="receive"
            img={receiveImg}
            caption="Получить"
          />
          <CircleButtonLink link="send" img={sendImg} caption="Отправить" />
        </div>
      </div>
      {
        <TokenList wallets={data && data["wallets"]} />
      }
    </section>
  );
};

export default Home;
