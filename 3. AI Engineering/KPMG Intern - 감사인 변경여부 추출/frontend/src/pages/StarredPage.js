// 즐겨찾기 목록에 대한 기업정보들이 render되는 페이지
import React from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import StarredForm from "../components/StarredForm";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import "./Context.css";

const StarredPage = () => {
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
            <StarredForm />
          </div>
        </div>
      </div>
    </div>
  );
};
export default StarredPage;
