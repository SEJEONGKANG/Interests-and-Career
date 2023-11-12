// 기업별 최신 정보를 보여주는 페이지/excel 다운받을 수 있는 페이지
import React, { useState, useEffect } from "react";
import {
  Box,
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Tooltip,
  Typography,
} from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import { useNavigate } from "react-router-dom";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import { useRecent } from "../contexts/RecentContext";
import { useCurCorp } from "../contexts/curCorpContext";
import DownloadCSV from "../components/DownloadCSV";
import starredpic from "../assets/starred.png";
import notstarredpic from "../assets/notstarred.png";

const ViewRecent = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // 단일 기업 검색결과로 이동
  const { setCurcorpcode } = useCurCorp();
  // 로그인을 하면 바로 최신기업정보를 backend에 요청
  const { loggedinuser } = useUserID();
  const { starred, addStarred, removeStarred } = useStarredList();
  // 최신 기업 정보가 저장되는 context
  const { recentCorps, setRecentCorps } = useRecent();
  const navtoResult = (corpCode) => {
    setCurcorpcode(corpCode);
    navigate("/result");
  };
  // info/get_this_year_info로부터 올해 게시된 보고서중 가장 최근의 보고서에 대한 정보를 모든 기업에 대해 불러옴
  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/info/get_this_year_info`,
          {
            method: "GET",
          }
        );

        if (response.ok) {
          const responseData = await response.json();
          if (Array.isArray(responseData)) {
            setRecentCorps(responseData);
          }
        }
      } catch (error) {
        window.alert("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [loggedinuser]);
  // 즐겨찾기 추가 및 해제
  const handleToggleStarred = async (corp) => {
    if (corp.exist === true) {
      try {
        const response = await fetch(
          `http://localhost:8000/starred/change_starred_status?user_id=${loggedinuser}&corp_code=${corp.data.corp_code}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "applicati on/json",
            },
            body: JSON.stringify({
              user_id: loggedinuser,
              corp_code: corp.data.corp_code,
            }),
          }
        );

        if (response.ok) {
          if (
            starred.some(
              (item) =>
                item.corp_code === corp.data.corp_code &&
                item.corp_name === corp.data.corp_name
            )
          ) {
            removeStarred({
              corp_code: corp.data.corp_code,
              corp_name: corp.data.corp_name,
            });
          } else {
            addStarred({
              corp_code: corp.data.corp_code,
              corp_name: corp.data.corp_name,
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
    <Paper
      elevation={3}
      style={{
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      {loading ? (
        <div style={{ width: "100%", marginTop: "20px" }}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              flexDirection: "column",
            }}
          >
            <CircularProgress />
            <Typography variant="body1" style={{ marginTop: "10px" }}>
              로딩중...
            </Typography>
          </Box>
        </div>
      ) : (
        <div>
          <Typography
            variant="h4"
            style={{ color: "#0A1A7E", marginTop: "20px" }}
          >
            올해 보고서를 공시한 기업 목록
          </Typography>
          <Typography variant="subtitle1">
            올해 사업/반기/분기 보고서를 공시한 기업 목록입니다. 자세한 정보를
            위해서는 기업명을 클릭하세요.
          </Typography>
          <Box
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginBottom: "10px",
            }}
          >
            {/*엑셀 다운로드 용 버튼 */}
            <DownloadCSV />
          </Box>
          <TableContainer component={Paper} sx={{ width: "1400px" }}>
            <Table
              style={{ borderCollapse: "collapse", border: "1px solid #ccc" }}
            >
              <TableHead>
                <TableRow>
                  <TableCell>기업 코드</TableCell>
                  <TableCell>기업명</TableCell>
                  <TableCell>최신 보고서명</TableCell>
                  <TableCell>당기 감사인</TableCell>
                  <TableCell>전기 감사인</TableCell>
                  <TableCell>전전기 감사인</TableCell>
                  <TableCell>감사인 변동 여부</TableCell>
                  <TableCell>지정감사여부</TableCell>
                  <TableCell>즐겨찾기 추가</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recentCorps.map((corp, index) => (
                  <TableRow key={index}>
                    <TableCell width="100px" alignItems="center">
                      {corp.data.corp_code}
                    </TableCell>
                    <TableCell
                      width="200px"
                      alignItems="center"
                      onClick={() => navtoResult(corp.data.corp_code)}
                      style={{
                        cursor: "pointer",
                      }}
                    >
                      {
                        <Tooltip
                          title={`${corp.data.corp_name} 기업 정보 상세보기`}
                        >
                          {corp.data.corp_name}
                        </Tooltip>
                      }
                    </TableCell>
                    <TableCell width="200px" alignItems="center">
                      {corp.exist === true ? corp.data.report_nm : "-"}
                    </TableCell>
                    <TableCell width="60px" alignItems="center">
                      {corp.exist === true ? corp.data.auditor_now : "-"}
                    </TableCell>
                    <TableCell width="60px" alignItems="center">
                      {corp.exist === true ? corp.data.auditor_prior : "-"}
                    </TableCell>
                    <TableCell width="60px" alignItems="center">
                      {corp.exist === true
                        ? corp.data.auditor_two_years_ago
                        : "-"}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true ? corp.data.is_changed : "-"}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true
                        ? corp.data.is_audit_currently_assigned
                        : "-"}
                    </TableCell>
                    <TableCell>
                      <Tooltip title={`${corp.data.corp_name} 즐겨찾기에 추가`}>
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            height: "100%",
                          }}
                        >
                          <img
                            src={
                              starred.some(
                                (item) =>
                                  item.corp_code === corp.data.corp_code &&
                                  item.corp_name === corp.data.corp_name
                              )
                                ? starredpic
                                : notstarredpic
                            }
                            alt={
                              starred.some(
                                (item) =>
                                  item.corp_code === corp.data.corp_code &&
                                  item.corp_name === corp.data.corp_name
                              )
                                ? "Remove from Starred"
                                : "Add to Starred"
                            }
                            style={{
                              ...logoStyle,
                              cursor: "pointer",
                            }}
                            onClick={() => handleToggleStarred(corp)}
                          />
                        </div>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )}
    </Paper>
  );
};
const logoStyle = {
  width: "20px",
  height: "auto",
};
export default ViewRecent;
