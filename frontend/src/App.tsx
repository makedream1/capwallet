import { useEffect } from "react";
import { Route, Routes } from "react-router-dom";

import { useTelegram } from "./hooks/useTelegram";

import Home from "./pages/Home/Home";
import Receive from "./pages/Receive/Receive";
import Send from "./pages/Send/Send";
import ResponseForm from './pages/ResponseForm/ResponseForm';

import "./assets/css/App.css";

function App() {
  const { tg } = useTelegram();

  useEffect(() => {
    tg.ready();
    tg.expand();
  }, []);

  return (
    <div className="App">
      <Routes>
        <Route index element={<Home />} />
        <Route path={"send"} element={<Send />} />
        <Route path={"receive"} element={<Receive />} />
        <Route path={"thank-you"} element={<ResponseForm />} />
      </Routes>
    </div>
  );
}

export default App;
