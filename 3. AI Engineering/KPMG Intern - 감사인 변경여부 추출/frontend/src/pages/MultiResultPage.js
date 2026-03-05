// MultiCorpForm.js를 render하는 페이지
import React from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import MultiCorpForm from "../components/MultiCorpForm";
import "./Context.css";

const MultiResultPage = () => {
  const { loggedinuser } = useUserID();
  const { starred } = useStarredList();
  return (
    <div>
      <Header />
      <div style={{ marginTop: "15px", display: "flex" }}>
        <Sidebar username={loggedinuser} starred={starred} />
        <div className="mainContextStyle" style={{ marginLeft: "15px" }}>
          <div
            style={{
              flex: 1,
              marginLeft: "10px",
              marginRight: "10px",
            }}
          >
            <MultiCorpForm />
          </div>
        </div>
      </div>
    </div>
  );
};

export default MultiResultPage;
