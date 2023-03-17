import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { IFormData, IToken } from "../../types/types";
import { useTelegram } from "../../hooks/useTelegram";
import Header from "../../components/Header/Header";
import SendTokenForm from "../../components/SendTokenForm/SendTokenForm";
import BigBlueButton from "../../components/Buttons/BigBlueButton/BigBlueButton";
import useFetch from "../../hooks/useFetch";
import { URL } from "../../helpers/consts";

import "./Send.css";

const { tg, user } = useTelegram();

const Send = () => {
  const navigate = useNavigate();
  const userId = user.id;

  const initData = tg.initData.split("&");
  const query_id = initData[0].split("=")[1];

  const url = `${URL}/users/${userId}/wallets`;
  const [data, isLoading, error] = useFetch(url);

  const [formData, setFormData] = useState<IFormData>({
    user_id: "",
    source: "",
    amount: 0,
    gas_fee: 0,
    destination: "",
    coin: "",
    network: "",
    query_id: query_id,

  });

  const tokens: IToken[] =
    data &&
    data.data.map((wallet: any) => {
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

  const [page, setPage] = useState<number>(0);

  const pageDisplay = () => {
    if (page === 0) {
      return (
        <SendTokenForm
          userId={userId}
          formData={formData}
          tokens={tokens}
          setFormData={setFormData}
        />
      );
    } else if (page === 1) {
      const total = formData.amount + formData.gas_fee;
      return (
        <div className="send-container confirm-send">
          <div className="send-title">Проверьте данные и подтвердите вывод</div>
          <p className="send-confirm-p">
            <span>Cумма вывода</span>{" "}
            <span>
              {formData.amount / 1e9} {formData.coin}
            </span>
          </p>
          <p className="send-confirm-p">
            <span>Комиссия</span>{" "}
            <span>
              {formData.gas_fee / 1e9} {formData.coin}
            </span>
          </p>
          <p className="send-confirm-p">
            <span>Общая сумма</span>{" "}
            <span>
              {total / 1e9} {formData.coin}
            </span>
          </p>
          <div className="send-confirm-address-wrapper">
            <span>Адрес</span>{" "}
            <span className="send-confirm-address">{formData.destination}</span>
          </div>
        </div>
      );
    }
  };

  const validateFormData = () => {
    for (const value of Object.values(formData)) {
      if (!value) return false;
    }
    return true;
  };

  const handleSubmit = () => {
    fetch(`${URL}/withdraw`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        navigate("/thank-you", { state: { data: data } });
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <>
      <Header />
      <section className="Send">
        {pageDisplay()}
        {page === 0 && validateFormData() && (
          <BigBlueButton
            type={"button"}
            onClick={(e: Event) => {
              e.preventDefault();
              setPage((currPage) => currPage + 1);
            }}
            caption={"Отправить"}
            isDisabled={false}
          />
        )}
        {page === 1 && (
          <BigBlueButton
            type={"button"}
            onClick={handleSubmit}
            caption={"Подтверждаю"}
            isDisabled={false}
          />
        )}
      </section>
    </>
  );
};

export default Send;
