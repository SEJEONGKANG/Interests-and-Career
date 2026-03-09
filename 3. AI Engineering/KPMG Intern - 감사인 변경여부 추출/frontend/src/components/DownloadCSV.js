import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import { useUserID } from "../contexts/UserContext";
import { useBlob } from "../contexts/BlobContext";
const DownloadCSV = () => {
  // info/download_csv로부터 받아온 excel file을 설정해주는 useContext hooks (전체 repository에 적용)
  const { blob, setBlob } = useBlob();
  // excel파일을 유저가 접근할 수 있을 때까지 downloading=True: 버튼 비활성화, 접근가능하면 downloading=False: 버튼 활성화
  const [downloading, setDownloading] = useState(false);
  // user가 login할 때부터 해당 파일을 다운받기 위해 userContext가 변동되면 excel download가 진행되는 useEffect hooks 활용
  const { loggedinuser } = useUserID();
  /** Fastapi에서 받아온 excel file을 blob형식으로 저장하고 이를 다운받는 function */
  const handleDownload = () => {
    if (blob) {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "recent_auditors.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    }
  };
  /** user가 login할 때부터 download가 시작되게 만들어주는 useEffect hooks */
  useEffect(() => {
    const fetchData = async () => {
      setDownloading(true);
      try {
        const response = await fetch("http://localhost:8000/info/download_csv");

        if (response.ok) {
          const newBlob = await response.blob();
          setBlob(newBlob);
        } else {
          console.error("Failed to fetch CSV file.");
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setDownloading(false);
      }
    };

    fetchData();
  }, [loggedinuser]);

  return (
    <div>
      <Button
        type="button"
        variant="contained"
        color="primary"
        onClick={handleDownload}
        disabled={downloading}
        sx={{ cursor: "pointer", marginTop: "20px", alignSelf: "center" }}
      >
        {downloading ? "Downloading..." : "Download CSV"}
      </Button>
    </div>
  );
};

export default DownloadCSV;
