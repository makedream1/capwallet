import { Link } from "react-router-dom";
import "./CircleButtonLink.css";

const CircleButtonLink = ({
  link,
  img,
  caption,
}: {
  link: string;
  img: string;
  caption: string;
}) => {
  return (
    <Link to={`/${link}`} className="CircleButtonLink">
      <img src={img} alt={link} />
      <span className="CircleButtonCaption">{caption}</span>
    </Link>
  );
};

export default CircleButtonLink;
