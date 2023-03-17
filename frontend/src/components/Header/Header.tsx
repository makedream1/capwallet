import { useLocation } from 'react-router-dom';

import ButtonBack from '../Buttons/ButtonBack/ButtonBack';

import "./Header.css";

const Header = () => {
  const location = useLocation();

  return (
    <header className="Header">
      {location.pathname !== '/' && <ButtonBack />}
    </header>
  );
};

export default Header;
