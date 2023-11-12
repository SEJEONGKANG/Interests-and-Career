// 기업 검색창 component
import React, { useState, useEffect } from "react";
import {
  Paper,
  Button,
  Container,
  Typography,
  CircularProgress,
  Autocomplete,
  TextField,
} from "@mui/material";
import { createFuzzyMatcher } from "./filter";

const CorpForm = ({ handleoneSubmit, handlemultiSubmit }) => {
  // error 발생시 어떤 error인지 확인해주는 useState hooks
  const [errorMessage, setErrorMessage] = useState("");
  // Loading중인지 아닌지 설정해주는 useState hooks
  const [loading, setLoading] = useState(false);
  // info/cur_corp_list endpoint로부터 db에서 받아오는 전체 기업 코드 및 이름 array => [ {corp_code:str, corp_name:str}, ...]
  const [corporations, setCorporations] = useState([]);
  // 검색창에서 선택된 기업들의 array
  const [selectedCorps, setSelectedCorps] = useState([]);

  // 검색창에 뜰 모든 기업 목록 info/curc_corp_list로부터 받아오기
  useEffect(() => {
    setLoading(true);
    try {
      const fetchData = async () => {
        const response = await fetch(
          "http://localhost:8000/info/cur_corp_list",
          { method: "GET" }
        );
        const data = await response.json();
        const corp_json = data;

        if (Array.isArray(corp_json)) {
          setCorporations(corp_json);
        } else {
          console.error("Data fetched is not an array:", corp_json);
        }
      };

      fetchData();
    } catch (error) {
      console.error("Error fetching corporations:", error);
    } finally {
      setLoading(false);
    }
  }, []);
  /**
   *
   * form 제출 시 실행되는 함수
   * @returns selectedCorps의 길이가 1일 경우 handleoneSubmit 함수를, 1보다 더 크면 handlemultiSubmit 함수를 실행
   */
  const onSubmit = async (e) => {
    e.preventDefault();

    if (selectedCorps.length === 0) {
      setErrorMessage("기업을 선택해주세요.");
      return;
    }

    setErrorMessage("");
    setLoading(true);

    try {
      if (selectedCorps.length === 1) {
        await handleoneSubmit(selectedCorps);
      } else {
        await handlemultiSubmit(selectedCorps);
      }
    } catch (error) {
      console.error("Error submitting form:", error);

      setErrorMessage(`요청 처리 중에 오류가 발생했습니다. ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper style={{ padding: "20px" }}>
      <Container sx={{ minWidth: "1200px" }}>
        <Typography variant="h4" style={{ color: "#0A1A7E" }}>
          기업 정보 검색
        </Typography>
        <form onSubmit={onSubmit}>
          {/* 검색 및 필터링 기능
              mui library의 Autocomplete component 활용
              multiple: 다중 선택 허용
              options: 전체 기업 목록
              getOptionLabel: 기업 목록이 검색 결과에서 나타나는 모습 => "기업명 기업코드"
              value: 현재 선택된 기업 목록 array(selectedCorps)
              onChange: 선택된 기업 목록 array가 바뀔 때마다 selectedCorps를 새로 지정해주기
              filterOptions: 검색창에 입력한 stirng과 matching되는 기업 목록

          */}
          <Autocomplete 
            multiple
            options={corporations}
            getOptionLabel={(option) =>
              `${option.corp_name} ${option.corp_code}`
            }
            value={selectedCorps}
            onChange={(event, newValue) => {
              setSelectedCorps(newValue);
            }}
            filterOptions={(options, state) => {
              if (state.inputValue === "") return options;

              const regex = createFuzzyMatcher(state.inputValue);
              const filteredoption = options
                .filter((corp) => {
                  return regex.test(`${corp.corp_name} ${corp.corp_code}`);
                })
                .map((corp) => {
                  return corp;
                });
              return filteredoption;
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="기업명 및 기업코드 검색"
                fullWidth
                margin="normal"
              />
            )}
          />
          
          {errorMessage && (
            <Typography style={{ color: "red" }}>{errorMessage}</Typography>
          )}
          <Button
            type="submit"
            disabled={loading}
            variant="contained"
            color="primary"
          >
            {loading ? <CircularProgress size={24} /> : "기업 검색"}
          </Button>
        </form>
      </Container>
    </Paper>
  );
};

export default CorpForm;
