// 기업별 최신 보고서에 대한 정보가 render되는 페이지
import React from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import ViewRecent from "../components/ViewRecent";
import "./Context.css";

const ViewRecentPage = () => {
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
            <ViewRecent />
          </div>
        </div>
      </div>
    </div>
  );
};
export default ViewRecentPage;
