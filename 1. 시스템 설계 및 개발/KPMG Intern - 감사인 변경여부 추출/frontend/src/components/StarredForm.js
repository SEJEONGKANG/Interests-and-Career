// 즐겨찾기 목록내의 기업들의 다중결과페이지
import React, { useEffect, useState } from "react";
import { useStarredList } from "../contexts/StarredContext";
import {
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
import { useNavigate } from "react-router-dom";
import { useCurCorp } from "../contexts/curCorpContext";
import { useUserID } from "../contexts/UserContext";
import starredpic from "../assets/starred.png";
import notstarredpic from "../assets/notstarred.png";

const StarredForm = () => {
  // 유저별로 즐겨찾기 관리
  const { loggedinuser } = useUserID();
  // 즐겨찾기 해제 기능 => 유저의 즐겨찾기 목록에서 제거
  const { starred, addStarred, removeStarred } = useStarredList();
  // 즐겨찾기 목록을 fastapi server로 POST하고 해당 목록의 기업의 상세정보들을 저장하는 var
  const [starredInfo, setStarredInfo] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  // 결과창에서 기업명 클릭 시 해당 기업의 단일 결과 페이지로 이동
  const { setCurcorpcode } = useCurCorp();

  const navtoResult = (corpCode) => {
    setCurcorpcode(corpCode);
    navigate("/result");
  };
  /**
   *
   * @param {json} corp corp_code와 user_id를 fastapi 서버에 보내고, 만약 해당 corp_code와 user_id가 이미 user_interest table에 있다면 삭제, 없으면 추가
   * frontend에서도 없으면 추가, 있으면 삭제
   */
  const handleToggleStarred = async (corp) => {
    try {
      const response = await fetch(
        `http://localhost:8000/starred/change_starred_status?user_id=${loggedinuser}&corp_code=${corp.corp_code}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: loggedinuser,
            corp_code: corp.corp_code,
          }),
        }
      );

      if (response.ok) {
        if (
          starred.some(
            (item) =>
              item.corp_code === corp.corp_code &&
              item.corp_name === corp.corp_name
          )
        ) {
          removeStarred({
            corp_code: corp.corp_code,
            corp_name: corp.corp_name,
          });
        } else {
          addStarred({
            corp_code: corp.corp_code,
            corp_name: corp.corp_name,
          });
        }
      } else {
        console.error("Error updating Starred_List");
      }
    } catch (error) {
      console.error("Error updating Starred_List", error);
    }
  };
  /**
   * 즐겨찾기 목록이 바뀌면, update된 즐겨찾기목록을 받아옴
   */
  useEffect(() => {
    setLoading(true);
    try {
      const fetchData = async () => {
        const response = await fetch(
          `http://localhost:8000/starred/starred_corp_info_total?user_id=${loggedinuser}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_id: loggedinuser,
            }),
          }
        );
        if (response.ok) {
          const responseData = await response.json();
          if (Array.isArray(responseData)) {
            setStarredInfo(responseData);
          }
        }
      };

      fetchData();
    } catch (error) {
      console.error("Error fetching corporations:", error);
    } finally {
      setLoading(false);
    }
  }, [starred]);
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
        <p>Loading...</p>
      ) : (
        <div>
          <Typography
            variant="h4"
            style={{
              color: "#0A1A7E",
              marginTop: "20px",
              marginBottom: "20px",
            }}
          >
            즐겨찾기 기업 목록
          </Typography>
          <TableContainer component={Paper} sx={{ width: "1400px" }}>
            <Table
              style={{ borderCollapse: "collapse", border: "1px solid #ccc" }}
            >
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: "bold" }}>기업 코드</TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>기업명</TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    최신 보고서명
                  </TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>당기 감사인</TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>전기 감사인</TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    전전기 감사인
                  </TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    감사인 변동 여부
                  </TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    지정감사여부
                  </TableCell>
                  <TableCell sx={{ fontWeight: "bold" }}>
                    즐겨찾기 추가
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {starredInfo.map((corp, index) => (
                  <TableRow key={index}>
                    <TableCell width="100px" alignItems="center">
                      {corp.corp_code}
                    </TableCell>
                    <TableCell
                      width="200px"
                      alignItems="center"
                      onClick={() => navtoResult(corp.corp_code)}
                      style={{
                        cursor: "pointer",
                      }}
                    >
                      {
                        <Tooltip title={`${corp.corp_name} 기업 정보 상세보기`}>
                          {corp.corp_name}
                        </Tooltip>
                      }
                    </TableCell>
                    <TableCell width="200px" alignItems="center">
                      {corp.report_nm}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.auditor_now}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.auditor_prior}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.auditor_two_years_ago}
                    </TableCell>
                    <TableCell width="110px" alignItems="center">
                      {corp.is_changed}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.is_audit_currently_assigned}
                    </TableCell>
                    <TableCell>
                      <Tooltip title={`${corp.corp_name} 즐겨찾기에 추가`}>
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
                                  item.corp_code === corp.corp_code &&
                                  item.corp_name === corp.corp_name
                              )
                                ? starredpic
                                : notstarredpic
                            }
                            alt={
                              starred.some(
                                (item) =>
                                  item.corp_code === corp.corp_code &&
                                  item.corp_name === corp.corp_name
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
export default StarredForm;
