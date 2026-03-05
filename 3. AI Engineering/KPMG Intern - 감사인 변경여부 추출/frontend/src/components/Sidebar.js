// 각 페이지마다 side에 보이는 sidebar => 해당 user의 즐겨찾기 목록을 보여줌
import React from "react";
import { Paper, Typography, Grid } from "@mui/material";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import { useCurCorp } from "../contexts/curCorpContext";
import StarIcon from "../assets/starred.png";
import { useNavigate } from "react-router-dom";

const Sidebar = () => {
  // 유저별로 즐겨찾기 관리
  const { loggedinuser } = useUserID();
  //starred에 있는 기업들 모두 표시하기 위해 받아옴
  const { starred } = useStarredList();
  // 목록에 있는 기업들 중 하나 선택시 해당 기업의 결과페이지로 이동
  const { setCurcorpcode } = useCurCorp();
  const navigate = useNavigate();

  const navtoResult = (corpCode) => {
    setCurcorpcode(corpCode);
    navigate("/result");
  };

  const navtoStarred = () => {
    navigate("/starred");
  };

  return (
    <Paper elevation={3} style={sidebarStyle}>
      <Typography variant="h5" style={usernameStyle}>
        {loggedinuser}
      </Typography>
      <div style={starredBarContainerStyle}>
        <Grid container spacing={2} alignItems="center" onClick={navtoStarred}>
          <Grid item>
            <img src={StarIcon} alt="Star Icon" style={starIconStyle} />
          </Grid>
          <Grid item>
            <Typography
              variant="h6"
              style={{
                fontFamily: "Noto Sans KR",
                fontSize: "20px",
                fontStyle: "normal",
                fontWeight: 500,
                lineHeight: "54.6px",
                color: "#00338D",
                cursor: "pointer",
              }}
            >
              즐겨찾기 목록
            </Typography>
          </Grid>
        </Grid>
        {/*즐겨찾기 목록 클릭시 해당 기업 상세정보로 이동 */}
        {starred.map((corp) => (
          <div
            key={corp}
            style={starredBarStyle}
            onClick={() => navtoResult(corp.corp_code)}
          >
            {corp.corp_name}
          </div>
        ))}
      </div>
      <div style={emptySpaceStyle}></div>
    </Paper>
  );
};

const sidebarStyle = {
  display: "flex",
  height: "100%",
  flexDirection: "column",
  width: "250px",
  backgroundColor: "#FFFFFF",
  color: "#000",
};

const usernameStyle = {
  textAlign: "center",
  padding: "10px",
  color: "#0A1A7E",
};

const starredBarContainerStyle = {
  display: "flex",
  flexDirection: "column",
  padding: "16px",
  flexGrow: 1,
};

const starredBarStyle = {
  height: "40px",
  marginBottom: "4px",
  display: "flex",
  alignItems: "center",
  justifyContent: "left",
  cursor: "pointer",
  overflow: "hidden",
  whiteSpace: "nowrap",
  textOverflow: "ellipsis",
};

const emptySpaceStyle = {
  flex: 1,
};

const starIconStyle = {
  width: 25,
  height: 25,
  cursor: "pointer",
};
export default Sidebar;
