import { useLocation } from "react-router-dom";
import "./ResponseForm.css";
import BigButton from "../../components/Buttons/BIgButtonLink/BigButtonLink";

import congrat from "../../assets/images/gif/congrat.gif";
import sad from "../../assets/images/gif/sad.gif";
import cry from "../../assets/images/gif/cry.gif";

const ResponseForm = () => {
  const { state } = useLocation();
  const { data } = state;

  return (
    <section className="Send">
      <div className="emoji-wrapper">
        {data && data.status === "ok" && (
          <>
            <div className="emoji">
              <img src={congrat} alt="congrat face" />
            </div>
            <div className="message">{data.detail}</div>
          </>
        )}
        {data && data.error && (
          <>
            <div className="emoji">
              <img src={cry} alt="crying face" />
            </div>
            <div className="message">{data.error}</div>
          </>
        )}
      </div>
      <BigButton link={""} caption={"Вернуться в кошелек"} />
    </section>
  );
};

export default ResponseForm;
