// login form component
import React, { useState } from "react";
import { useStarredList } from "../contexts/StarredContext";
import "./LoginForm.css";
import Logo from "../assets/logo.png";

const LoginForm = ({ handleLogin }) => {
  // 로그인 시 user/login endpoint로부터 해당 user의 starred목록을 받고 이를 starredcontext에 저장 sidebar component에 띄워주기 위함
  const { setStarred } = useStarredList();
  // login 입력이 바뀔 때마다 username을 설정
  const [username, setUsername] = useState("");
  // password 입력이 바뀔 때마다 password를 설정
  const [password, setPassword] = useState("");
  // enter key를 입력해도 submit을 할 수 있게 설정해주는 함수
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };
  /**
   * 
   * @param {event} e 제출 시 fastapi server에서 userid와 password가 일치하는지 확인 후 response 수신 
   */
  const handleSubmit = async (e) => {
    try {
      const response = await fetch(
        `http://localhost:8000/user/login?id_input=${username}&password=${password}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id_input: username,
            password: password,
          }),
        }
      );

      if (response.ok) {
        const responseData = await response.json();
        if (responseData.log_in === true) {
          handleLogin(username);
          setStarred(responseData.starred);
        } else {
          window.alert("잘못된 비밀번호입니다.");
        }
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };
  return (
    <div className="login-form">
      <img
        src={Logo}
        alt="Logo"
        style={{ width: "150px", height: "auto" }}
        sx={{ display: { xs: "none", md: "flex" }, mr: 1 }}
      />
      <h2>Live Audit Information</h2>
      <div className="input-group">
        {/*ID 입력칸*/}
        <input
          type="text"
          id="username"
          value={username}
          placeholder="ID를 입력하세요"
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleKeyPress}
          style={{ width: "250px" }}
        />
      </div>
      <div className="input-group">
        {/*password 입력칸 */}
        <input
          type="password"
          id="password"
          value={password}
          placeholder="비밀번호를 입력하세요"
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleKeyPress}
          style={{ width: "250px" }}
        />
      </div>
      <div className="input-group">
        <div className="login-button" onClick={handleSubmit}>
          Login
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
