import { Link } from "react-router-dom";
import "./BigButtonLink.css";

const BigButtonLink = ({
  link = "",
  caption,
  state = {}
}: {
  link: string;
  caption: string;
  state?: {};
}) => {
  return (
    <Link to={`/${link}`} className="BigButtonLink" state={state}>
      <span className="BigButtonLinkCaption">{caption}</span>
    </Link>
  );
};

export default BigButtonLink;
