// TargetForm, 영업대상기업들에 대한 정보가 render되는 페잊
import React from "react";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import TargetForm from "../components/TargetForm";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import "./Context.css";

function TargetPage() {
  const { loggedinuser } = useUserID();
  const { starred } = useStarredList();

  return (
    <div>
      <Header />
      <div style={{ marginTop: "10px", display: "flex" }}>
        <Sidebar username={loggedinuser} starred={starred} />
        <div className="mainContextStyle" style={{ marginLeft: "15px" }}>
          <div
            style={{
              flex: 1,
              marginLeft: "10px",
              marginRight: "10px",
            }}
          >
            <TargetForm />
          </div>
        </div>
      </div>
    </div>
  );
}

export default TargetPage;
