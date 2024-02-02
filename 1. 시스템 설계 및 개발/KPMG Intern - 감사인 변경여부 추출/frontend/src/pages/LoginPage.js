// loginform을 render시키는 page
import React from "react";
import LoginForm from "../components/LoginForm";
import { useNavigate } from "react-router-dom";
import { useUserID } from "../contexts/UserContext";
import "./LoginPage.css";

const LoginPage = () => {
  const { setLoggedInUser } = useUserID();
  const navigate = useNavigate();

  const handleLogin = (username) => {
    setLoggedInUser(username);
    navigate("/main");
  };

  return (
    <div className="login-page">
      <div className="login-content">
        <LoginForm handleLogin={handleLogin} />
      </div>
    </div>
  );
};

export default LoginPage;
