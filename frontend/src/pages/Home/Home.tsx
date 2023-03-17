import CircleButtonLink from "../../components/Buttons/CircleButtonLink/CircleButtonLink";
import TokenList from "../../components/TokenList/TokenList";
import TotalBalance from "../../components/TotalBalance/TotalBalance";

import receiveImg from "./../../assets/images/icon_receive.svg";
import sendImg from "./../../assets/images/icon_send.svg";

import "./Home.css";
import useFetch from "../../hooks/useFetch";
import { useTelegram } from "../../hooks/useTelegram";
import { URL } from "../../helpers/consts";

const { user } = useTelegram();

const Home = () => {
  const userId = user.id;

  const url = `${URL}/users/${userId}`;

  const [data, isLoading, error] = useFetch(url);

  return (
    <section className="Home">
      <div className="wrapper-balance-buttons">
        {isLoading || !data ? (
          <div></div>
        ) : (
          <TotalBalance totalBalance={data && data.data["total_balance"]} />
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
      <TokenList userId={userId} />
    </section>
  );
};

export default Home;
