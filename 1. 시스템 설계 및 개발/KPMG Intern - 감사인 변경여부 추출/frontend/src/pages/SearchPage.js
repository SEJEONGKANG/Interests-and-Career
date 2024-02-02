// CorpForm.js가 render되는 페이지
import React from "react";
import CorpForm from "../components/CorpForm";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import { useNavigate } from "react-router-dom";
import { useCurCorp } from "../contexts/curCorpContext";
import { useMultiCorp } from "../contexts/multiCorpContext";
import "./Context.css";

const SearchPage = () => {
  const { loggedinuser } = useUserID();
  const { starred } = useStarredList();
  const { setCurcorpname, setCurcorpcode } = useCurCorp();
  const { setMultiCorp } = useMultiCorp();
  const navigate = useNavigate();
  // CorpForm의 검색결과가 하나일 경우에는 handleOneSubmit을 통해 단일기업결과페이지로 이동
  const handleoneSubmit = (corplist) => {
    setCurcorpname(corplist[0].corp_name);
    setCurcorpcode(corplist[0].corp_code);
    navigate("/result");
  };

  // CorpForm의 검색결과가 두개이상의 기업일 경우에는 handleMultiSubmit을 통해 다중기업결과페이지로 이동
  const handlemultiSubmit = (corplist) => {
    setMultiCorp(corplist);
    navigate("/multiresult");
  };

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
            <CorpForm
              handleoneSubmit={handleoneSubmit}
              handlemultiSubmit={handlemultiSubmit}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
