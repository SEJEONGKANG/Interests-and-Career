// 다른 서비스들로 이동할 수 있는 mainpage
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Typography, Paper, Grid } from "@mui/material";
import service1pic from "../assets/service1pic.jpg";
import service2pic from "../assets/service2pic.jpg";
import service3pic from "../assets/service3pic.jpg";
import service4pic from "../assets/service4pic.jpg";
import "./Context.css";

const MainPage = () => {
  const navigate = useNavigate();

  const navtoSearchPage = () => {
    navigate("/search");
  };
  const navtoContactPage = () => {
    navigate("/contact");
  };
  const navtoRecentPage = () => {
    navigate("/recent");
  };
  const navtoStarredPage = () => {
    navigate("/starred");
  };

  const [hoveredImage, setHoveredImage] = useState(null);
  const handleMouseEnter = (index) => {
    setHoveredImage(index);
  };
  const handleMouseLeave = () => {
    setHoveredImage(null);
  };

  const serviceItems = [
    {
      pic: service1pic,
      title: "기업별 검색",
      description: "찾고자 하는 기업 검색",
      onClick: navtoSearchPage,
    },
    {
      pic: service2pic,
      title: "잠재 고객 검색",
      description: "지정감사가 끝난 기업 검색",
      onClick: navtoContactPage,
    },
    {
      pic: service3pic,
      title: "올해 보고서 조회",
      description: "이번 기에 공시된 보고서 검색",
      onClick: navtoRecentPage,
    },
    {
      pic: service4pic,
      title: "즐겨찾기 기업 확인",
      description: "즐겨찾기로 등록한 기업 검색",
      onClick: navtoStarredPage,
    },
  ];

  return (
    <div>
      <div className="mainPageStyle">
        <Paper
          elevation={3}
          style={{
            padding: "40px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginTop: "150px",
            borderRadius: "40px",
          }}
        >
          <Typography
            variant="h4"
            style={{
              color: "#0A1A7E",
              marginTop: "20px",
              marginBottom: "50px",
            }}
          >
            SR Services
          </Typography>
          <Grid
            container
            spacing={4}
            justifyContent="center"
            alignItems="center"
          >
            {serviceItems.map((item, index) => (
              <Grid
                item
                key={index}
                xs={6}
                sm={3}
                onMouseEnter={() => handleMouseEnter(index)}
                onMouseLeave={handleMouseLeave}
                onClick={item.onClick}
                style={{ cursor: "pointer" }}
              >
                <Paper elevation={3} style={styles.servicePaper}>
                  <img
                    src={item.pic}
                    alt={item.title}
                    style={{
                      ...styles.serviceImage,
                      transform:
                        hoveredImage === index ? "scale(1.2)" : "scale(1)",
                      transition: "transform 0.3s ease-in-out",
                    }}
                  />
                  <Typography variant="h6" style={styles.serviceTitle}>
                    {item.title}
                  </Typography>
                  <Typography style={styles.serviceDescription}>
                    {item.description}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </div>
    </div>
  );
};

const styles = {
  servicePaper: {
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    borderRadius: "6px",
    border: "1px solid #FFF",
    cursor: "pointer",
  },
  serviceImage: {
    width: "246px",
    height: "246px",
    borderRadius: "123px",
    marginBottom: "30px",
  },
  serviceTitle: {
    color: "#333",
    fontFamily: "Noto Sans KR",
    fontSize: "22px",
    fontWeight: 700,
    lineHeight: "28.6px",
    textAlign: "center",
  },
  serviceDescription: {
    color: "#333",
    fontFamily: "Noto Sans KR",
    fontSize: "16px",
    fontWeight: 350,
    lineHeight: "20.8px",
    textAlign: "center",
  },
};

export default MainPage;
