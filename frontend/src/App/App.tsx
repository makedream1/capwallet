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
  const [data, setData] = useState<{
    status: string;
    data: {};
    error?: string;
  }>({ status: "", data: {} });

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetchDataApi(user.id);
      // @ts-ignore
      setData(response);
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
