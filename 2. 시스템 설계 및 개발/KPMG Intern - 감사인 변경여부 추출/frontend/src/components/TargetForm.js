// 올해를 포함한 3년간 지정감사 대상이고, 내년에 자유선임이 되는 기업들을 보여주는 component
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tooltip,
  Autocomplete,
  TextField,
  Typography,
} from "@mui/material";
import { useCurCorp } from "../contexts/curCorpContext";
import { escapeRegExp } from "lodash";
import "../pages/Context.css";
import {createFuzzyMatcher} from "./filter"


const TargetForm = () => {
  // 회계법인 검색용 지정감사를 수행했던 모든 회계법인들의 array
  const [auditors, setAuditors] = useState([]);
  // 영업 대상인 기업들에 대한 정보가 저장되는 var
  const [contactCorps, setContactCorps] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // 해당 기업의 단일 검색 결과페이지로 이동
  const { setCurcorpcode } = useCurCorp();
  // 회계법인 검색창에서 선택된 회계법인들 목록
  const [selectedAuditors, setSelectedAuditors] = useState([]);
  const navtoResult = (corpCode) => {
    setCurcorpcode(corpCode);
    navigate("/result");
  };
  /**
   * 영업대상인 기업들에 대한 정보를 받아옴
   */
  useEffect(() => {
    setLoading(true);
    try {
      const fetchData = async () => {
        const response = await fetch(
          "http://localhost:8000/contact/show_contact_list",
          { method: "GET" }
        );
        const data = await response.json();
        const contact_array = data.data;
        const auditorArray = data.auditor_list;
        setAuditors(auditorArray);

        if (Array.isArray(contact_array)) {
          setContactCorps(contact_array);
        } else {
          console.error("Data fetched is not an array:", contact_array);
        }
      };

      fetchData();
    } catch (error) {
      console.error("Error fetching contact list:", error);
    } finally {
      setLoading(false);
    }
  }, []);

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
            style={{ color: "#0A1A7E", marginTop: "20px" }}
          >
            지정감사 종료 기업 목록
          </Typography>
          <Typography variant="subtitle1" style={{ marginBottom: "20px" }}>
            올해 지정감사가 종료되는 기업 목록입니다. 자세한 정보를 위해서는
            기업명을 클릭하세요.
          </Typography>
          <TableContainer component={Paper} sx={{ width: "1400px" }}>
            <Table
              style={{ borderCollapse: "collapse", border: "1px solid #ccc" }}
            >
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontSize: "16px", fontWeight: "bold" }}>
                    기업 코드
                  </TableCell>
                  <TableCell sx={{ fontSize: "16px", fontWeight: "bold" }}>
                    기업명
                  </TableCell>
                  <TableCell
                    width="700px"
                    sx={{ fontSize: "16px", fontWeight: "bold" }}
                  >
                    최근 3년 지정감사 수행 법인
                    <Autocomplete
                      sx={{ width: 500 }}
                      multiple
                      options={auditors}
                      getOptionLabel={(option) => `${option}`}
                      value={selectedAuditors}
                      onChange={(event, newValue) => {
                        setSelectedAuditors(newValue);
                      }}
                      filterOptions={(options, state) => {
                        if (state.inputValue === "") return options;

                        const regex = createFuzzyMatcher(state.inputValue);
                        const filteredoption = options
                          .filter((auditor) => {
                            return regex.test(auditor);
                          })
                          .map((auditor) => {
                            return auditor;
                          });
                        return filteredoption;
                      }}
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          label="회계법인 선택"
                          margin="normal"
                        />
                      )}
                    />
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {(selectedAuditors != []) & (selectedAuditors.length >= 1)
                  ? contactCorps
                      .filter((contact) =>
                        selectedAuditors.includes(contact.auditor)
                      )
                      .map((contact) => (
                        <TableRow key={contact.corp_code}>
                          <TableCell>{contact.corp_code}</TableCell>
                          <TableCell
                            onClick={() => navtoResult(contact.corp_code)}
                          >
                            <Tooltip
                              title={`${contact.corp_code} 기업정보 상세보기`}
                            >
                              {contact.corp_name}
                            </Tooltip>
                          </TableCell>
                          <TableCell>{contact.auditor}</TableCell>
                        </TableRow>
                      ))
                  : contactCorps.map((contact) => (
                      <TableRow key={contact.corp_code}>
                        <TableCell sx={{ fontSize: "16px" }}>
                          {contact.corp_code}
                        </TableCell>
                        <TableCell
                          onClick={() => navtoResult(contact.corp_code)}
                          sx={{ cursor: "pointer", fontSize: "16px" }}
                        >
                          <Tooltip
                            title={`${contact.corp_name} 기업정보 상세보기`}
                          >
                            {contact.corp_name}
                          </Tooltip>
                        </TableCell>
                        <TableCell sx={{ fontSize: "16px" }}>
                          {contact.auditor}
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

export default TargetForm;
