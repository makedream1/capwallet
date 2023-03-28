import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { IFormData, IToken, IFetchData } from "../../types/types";
import { useTelegram } from "../../hooks/useTelegram";
import Header from "../../components/Header/Header";
import SendTokenForm from "../../components/SendTokenForm/SendTokenForm";
import BigBlueButton from "../../components/Buttons/BigBlueButton/BigBlueButton";

import { BASE_URL } from "../../api/data";

import "./Send.css";

const { tg } = useTelegram();

const Send = ({ data }: { data: IFetchData }) => {
  const navigate = useNavigate();
  const initData = tg.initData.split("&");
  const query_id = initData[0].split("=")[1];

  if (!data["wallets"]) {
    return <Navigate replace to="/" />;
  }
  const [formData, setFormData] = useState<IFormData>({
    user_id: "",
    source: "",
    amount: 0,
    gas_fee: 0,
    destination: "",
    coin: "",
    network: "",
    query_id: query_id + "ds",
  });

  const userId = data && data!["id"];

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
      if (!value)
        return (
          <BigBlueButton
            type={"button"}
            onClick={(e: Event) => {
              e.preventDefault();
            }}
            caption={"Отправить"}
            isDisabled={true}
          />
        );
    }
    return (
      <BigBlueButton
        type={"button"}
        onClick={(e: Event) => {
          e.preventDefault();
          setPage((currPage) => currPage + 1);
        }}
        caption={"Отправить"}
        isDisabled={false}
      />
    );
  };

  const handleSubmit = () => {
    fetch(`${BASE_URL}/withdraw`, {
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
      <section className="Send">
        <Header />
        {pageDisplay()}
        {page === 0 && validateFormData()}
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
