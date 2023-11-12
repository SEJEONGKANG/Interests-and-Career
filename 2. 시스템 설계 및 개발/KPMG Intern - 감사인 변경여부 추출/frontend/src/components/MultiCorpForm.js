// CorpForm.js에서 selectedCorps가 둘 이상이면 handlemultisubmit 함수를 통해 해당 component로 이동, 다중 기업 검색의 결과를 보여줌
import React, { useState, useEffect } from "react";
import { useMultiCorp } from "../contexts/multiCorpContext";
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
import starredpic from "../assets/starred.png";
import notstarredpic from "../assets/notstarred.png";
import { useUserID } from "../contexts/UserContext";
import { useStarredList } from "../contexts/StarredContext";
import { useCurCorp } from "../contexts/curCorpContext";

const MultiCorpForm = () => {
  // 검색 시 handlemultisubmit 함수를 통해 설정된 다중 기업들의 목록=> corp_code/corp_name
  const { multiCorp } = useMultiCorp();
  // multiCorp를 backend로 넘긴 후에 response로 받는 해당 기업들의 정보를 모두 받아온 var
  const [multiinfo, setMultiinfo] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // 기업명 클릭시 해당 기업 하나의 Resultpage로 이동
  const { setCurcorpcode } = useCurCorp();
  const navtoResult = (corpCode) => {
    setCurcorpcode(corpCode);
    navigate("/result");
  };
  // 검색 결과에서 즐겨찾기 추가 및 해제용 usercontext와 starredcontext
  const { loggedinuser } = useUserID();
  const { starred, addStarred, removeStarred } = useStarredList();
    /**
     * CorpForm에서 입력된 다수의 기업들의 corpcode들을 fastapi server로 보낸 후에 해당 기업들에 대한 정보를 json형식으로 받아옴
     * 검색창에서 다수 기업 선택시 handlemultisubmit이 실행되어 multiCorp이란 변수가 변경될 경우 실행되는 useEffect react-hooks.
     */
  useEffect(() => {
    setLoading(true);
    const corpcodeList = multiCorp.map(function (item) {
      return item.corp_code;
    });

    const fetchData = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/info/select_info_total`,
          {
            method: "POST",
            headers: {
              accept: "application/json",
              "Content-Type": "application/json",
            },
            body: JSON.stringify(corpcodeList),
          }
        );

        if (response.ok) {
          const responseData = await response.json();
          if (Array.isArray(responseData)) {
            setMultiinfo(responseData);
          }
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [multiCorp]);
  /**
   *
   * @param {json} corp corp_code와 user_id를 fastapi 서버에 보내고, 만약 해당 corp_code와 user_id가 이미 user_interest table에 있다면 삭제, 없으면 추가
   * frontend에서도 없으면 추가, 있으면 삭제
   */
  const handleToggleStarred = async (corp) => {
    if (corp.exist === true) {
      try {
        const response = await fetch(
          `http://localhost:8000/starred/change_starred_status?user_id=${loggedinuser}&corp_code=${corp.data.corp_code}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
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
    <Paper elevation={3} style={{ padding: "40px" }}>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <Typography
            variant="h4"
            style={{ color: "#0A1A7E", marginTop: "20px" }}
          >
            선택한 기업 목록
          </Typography>
          <Typography variant="subtitle1" style={{ marginBottom: "20px" }}>
            자세한 정보를 위해서는 기업명을 클릭하세요.
          </Typography>
          <TableContainer component={Paper}>
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
                {multiinfo.map((corp, index) => (
                  <TableRow key={index}>
                    <TableCell width="100px" alignItems="center">
                      {corp.data.corp_code}
                    </TableCell>
                    <TableCell
                      width="100px"
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
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true ? corp.data.report_nm : "-"}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true ? corp.data.auditor_now : "-"}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true ? corp.data.auditor_prior : "-"}
                    </TableCell>
                    <TableCell width="100px" alignItems="center">
                      {corp.exist === true
                        ? corp.data.auditor_two_years_ago
                        : "-"}
                    </TableCell>
                    <TableCell width="110px" alignItems="center">
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
export default MultiCorpForm;
