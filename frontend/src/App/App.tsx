import React, { useEffect, useMemo, useState } from "react";
import { Route, Routes } from "react-router-dom";

import Home from "../pages/Home/Home";
import Receive from "../pages/Receive/Receive";
import Send from "../pages/Send/Send";
import ResponseForm from "../pages/ResponseForm/ResponseForm";

import { useTelegram } from "../hooks/useTelegram";
import "./App.css";
import { fetchDataApi } from "../api/data";

const { tg, user } = useTelegram();

function App() {
  const userId = user?.id ? user.id : "131371085";

  const [data, setData] = useState<{
    wallets: any[];
    id: string;
    total_balance: number;
  }>({
    wallets: [],
    id: "",
    total_balance: 0,
  });

  useEffect(() => {
    const fetchData = () => {
      const response = fetchDataApi(userId);
      response.then((response) => setData(response.data));
    };
    tg.ready();
    tg.expand();
    fetchData();
  }, []);
  const cachedData = useMemo(() => data, [data]);

  return (
    <div className="App">
      <Routes>
        {cachedData && (
          <>
            <Route index element={<Home data={cachedData} />} />
            <Route path={"send"} element={<Send data={cachedData} />} />
            <Route path={"receive"} element={<Receive data={cachedData} />} />
          </>
        )}
        <Route path={"thank-you"} element={<ResponseForm />} />
      </Routes>
    </div>
  );
}

export default App;
