// 단일기업 결과를 render하는 페이지로, curcorpcode가 변동되는 경우(검색창에서 단일기업 검색하거나 다른 페이지에서 특정 기업명을 클릭한 경우) 해당페이지로 이동되며 render됨
import React, { useState, useEffect } from "react";
import { useCurCorp } from "../contexts/curCorpContext";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import { useNavigate } from "react-router-dom";
import {
  Button,
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Link,
} from "@mui/material";
import add from "../assets/add-to-starred.png";
import remove from "../assets/remove-from-starred.png";
import "./Context.css";

const ResultPage = () => {
  // 다른 페이지들에서 setcurcorpname과 setcurcorpcode로 설정된 curcorpcontext
  const { curcorpname, curcorpcode } = useCurCorp();
  // fastapiserver로 curpcorpcode를 보내고 해당 기업의 정보를 저장하는 var [{exists: bool, data:{corp_code: str, corp_name: str, ...}}, ...]
  const [corpData, setCorpData] = useState(null);
  const [exists, setExists] = useState(false);
  const { loggedinuser } = useUserID();
  const { starred, addStarred, removeStarred } = useStarredList();
  const navigate = useNavigate();
  // 다시검색하기 버튼
  const navtoSearch = () => {
    navigate("/search");
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/info/get_latest_info?corp_code=${curcorpcode}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              corp_code: curcorpcode,
            }),
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data.exist) {
            setCorpData(data.data);
            setExists(true);
          } else {
            setExists(false);
          }
        } else {
          console.error("Failed to fetch corporation data.");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [curcorpname, curcorpcode]);

  const handleToggleStarred = async () => {
    if (corpData) {
      try {
        const response = await fetch(
          `http://localhost:8000/starred/change_starred_status?user_id=${loggedinuser}&corp_code=${corpData.corp_code}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "applicati on/json",
            },
            body: JSON.stringify({
              user_id: loggedinuser,
              corp_code: corpData.corp_code,
            }),
          }
        );

        if (response.ok) {
          if (
            starred.some(
              (item) =>
                item.corp_code === corpData.corp_code &&
                item.corp_name === corpData.corp_name
            )
          ) {
            removeStarred({
              corp_code: corpData.corp_code,
              corp_name: corpData.corp_name,
            });
          } else {
            addStarred({
              corp_code: corpData.corp_code,
              corp_name: corpData.corp_name,
            });
          }
        } else {
          console.error("Error updating Starred_List");
        }
      } catch (error) {
        console.error("Error updating Starred_List", error);
      }
    }
  };
  return (
    <div>
      <Header />
      <div style={{ marginTop: "15px", display: "flex" }}>
        <Sidebar username={loggedinuser} starred={starred} />
        <div className="mainContextStyle" style={{ marginLeft: "15px" }}>
          <Paper
            elevation={3}
            style={{
              padding: "40px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            {exists ? (
              <Container>
                <Grid container spacing={6} alignItems="center">
                  <Grid item xs={16}>
                    <Grid container alignItems="center">
                      <Grid item xs={10}>
                        <Typography variant="h4" style={{ color: "#0A1A7E" }}>
                          기업 및 보고서 상세정보
                        </Typography>
                      </Grid>
                      <Grid item xs={2} style={{ textAlign: "right" }}>
                        <img
                          src={
                            starred.some(
                              (item) =>
                                item.corp_code === corpData.corp_code &&
                                item.corp_name === corpData.corp_name
                            )
                              ? remove
                              : add
                          }
                          alt={
                            starred.some(
                              (item) =>
                                item.corp_code === corpData.corp_code &&
                                item.corp_name === corpData.corp_name
                            )
                              ? "Remove from Starred"
                              : "Add to Starred"
                          }
                          style={{
                            ...logoStyle,
                            cursor: "pointer",
                          }}
                          onClick={handleToggleStarred}
                        />
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        기업명
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.corp_name}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        기업코드
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.corp_code}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        감사인 변경 여부
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.is_changed}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        보고서명
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.report_nm}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        보고서 공시일
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.rcept_dt}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        지정감사 여부
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.is_audit_currently_assigned}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        당기 감사인
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.auditor_now}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        전기 감사인
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.auditor_prior}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <div className="outerLayoutStyle">
                      <Typography
                        style={{ typographyStyle, fontWeight: "bold" }}
                      >
                        전전기 감사인
                      </Typography>
                      <div className="innerLayoutStyle">
                        <Typography style={{ innertypographyStyle }}>
                          {corpData.auditor_two_years_ago}
                        </Typography>
                      </div>
                    </div>
                  </Grid>
                  <Grid item xs={12} sm={6} md={8}>
                    <Typography style={{ typographyStyle, fontWeight: "bold" }}>
                      회계감사인의 변경 상세설명
                    </Typography>
                    <Typography
                      style={{ innertypographyStyle, marginTop: "10px" }}
                    >
                      {corpData.description}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} sm={6} md={4}>
                    <Typography style={{ typographyStyle, fontWeight: "bold" }}>
                      <Link
                        href={corpData.xml_content}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        공시보고서 원문 링크
                      </Link>
                    </Typography>
                  </Grid>
                </Grid>
                <div style={{ marginTop: "20px" }}></div>
                <Grid container spacing={1}>
                  <Grid item xs={12} sm={12}>
                    <Typography style={{ typographyStyle, fontWeight: "bold" }}>
                      감사인 관련 표
                    </Typography>
                    <div
                      className="scroll"
                      style={{
                        maxHeight: "400px",
                        overflow: "auto",
                        marginTop: "10px",
                        border: "1px solid #ccc",
                        padding: "10px",
                      }}
                    >
                      {corpData.auditor_in_heads.map((htmlTable, index) => (
                        <div
                          key={index}
                          dangerouslySetInnerHTML={{
                            __html: htmlTable,
                          }}
                          style={{
                            marginBottom: "20px",
                          }}
                        />
                      ))}
                    </div>
                  </Grid>
                </Grid>
              </Container>
            ) : (
              <Typography>No matching corporation found.</Typography>
            )}

            <Button
              type="submit"
              variant="contained"
              color="primary"
              onClick={navtoSearch}
              sx={{ cursor: "pointer", marginTop: "20px", alignSelf: "center" }}
            >
              다시 검색하기
            </Button>
          </Paper>
        </div>
      </div>
    </div>
  );
};

const logoStyle = {
  width: "40px",
  height: "auto",
};

const typographyStyle = {
  color: "#333",
  fontFamily: "Noto Sans KR",
  fontSize: "16px",
  fontStyle: "normal",
  fontWeight: 600,
  lineHeight: "20.8px",
};

const innertypographyStyle = {
  color: "#000",
  fontFamily: "Noto Sans KR",
  fontSize: "16px",
  fontStyle: "normal",
  fontWeight: 350,
  lineHeight: "20.8px",
};

export default ResultPage;
