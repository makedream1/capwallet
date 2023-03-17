import { useNavigate } from "react-router-dom";

import "./ButtonBack.css";

const ButtonBack = () => {
  const  navigate = useNavigate();
    return (
          <div onClick={() => navigate(-1)} className={"Button-Back"}></div>
    );
  };

  export default ButtonBack;