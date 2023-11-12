// page별 위에 나타내는 header 주기능은 다른 page로 navigate 해주는 기능
import * as React from "react";
import MenuIcon from "@mui/icons-material/Menu";
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
} from "@mui/material";
import logo from "../assets/logo.png";
import profile from "../assets/profile.png";
import { useNavigate } from "react-router-dom";
import { useUserID } from "../contexts/UserContext";
// 페이지들 목록
const pages = [
  "기업별 검색",
  "잠재 고객 검색",
  "올해 보고서 조회",
  "즐겨찾기 기업 확인",
];
// user icon click시 나타나는 목록
const settings = ["Profile", "Account", "Dashboard", "Logout"];

function ResponsiveAppBar() {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);
  const { setLoggedInUser } = useUserID();

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  // 다른 페이지들로 이동하기 위한 function
  const navigate = useNavigate();

  // mainpage로 이동
  const navtoMainPage = () => {
    navigate("/main");
  };
  // 잠재적 고객 페이지로 이동
  const navtoContactPage = () => {
    navigate("/contact");
  };
  // 즐겨찾기 목록 페이지로 이동
  const navtoStarredPage = () => {
    navigate("/starred");
  };
  // 검색페이지로 이동
  const navtoSearchPage = () => {
    navigate("/search");
  };
  //기업별 최신정보 페이지로 이동
  const navtoRecentPage = () => {
    navigate("/recent");
  };
  // 우측 상단의 logout button 클릭시 다시 로그인 화면으로 이동
  const navtoLogout = () => {
    setLoggedInUser("");
    navigate("/");
  };

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: "#FFFFFF",
      }}
    >
      <div
        style={{
          display: "flex",
          width: "1920px",
          height: "50px",
          minWidth: "1920px",
          maxWidth: "1920px",
          flexShrink: 0,
          alignItems: "center",
          padding: "1px 44px 6px 44px",
        }}
      >
        <Toolbar disableGutters>
          <img
            src={logo}
            alt="Logo"
            style={{
              width: "108px",
              height: "auto",
              marginRight: "20rem",
              cursor: "pointer",
            }}
            onClick={navtoMainPage}
          />
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleOpenNavMenu}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorElNav}
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "left",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "left",
            }}
            open={Boolean(anchorElNav)}
            onClose={handleCloseNavMenu}
            sx={{
              display: { xs: "block", md: "none" },
            }}
          >
            {pages.map((page) => (
              <MenuItem key={page} onClick={handleCloseNavMenu}>
                <Typography textAlign="center">{page}</Typography>
              </MenuItem>
            ))}
          </Menu>
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: "none", md: "flex" },
              justifyContent: "center",
            }}
          >
            <Button
              onClick={navtoSearchPage}
              sx={{
                mx: 2,
                my: 2,
                color: "#26265a",
                display: "block",
                fontSize: "23px",
              }}
            >
              {pages[0]}
            </Button>
            <Button
              onClick={navtoContactPage}
              sx={{
                mx: 2,
                my: 2,
                color: "#26265a",
                display: "block",
                fontSize: "23px",
              }}
            >
              {pages[1]}
            </Button>
            <Button
              onClick={navtoRecentPage}
              sx={{
                mx: 2,
                my: 2,
                color: "#26265a",
                display: "block",
                fontSize: "23px",
              }}
            >
              {pages[2]}
            </Button>
            <Button
              onClick={navtoStarredPage}
              sx={{
                mx: 2,
                my: 2,
                color: "#26265a",
                display: "block",
                fontSize: "23px",
              }}
            >
              {pages[3]}
            </Button>
          </Box>

          <Box sx={{ flexGrow: 0, marginLeft: "25rem" }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="Profile" src={profile} />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: "45px" }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting, index) => (
                <MenuItem
                  key={setting}
                  onClick={index === 3 ? navtoLogout : handleCloseUserMenu}
                >
                  <Typography textAlign="center">{setting}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </div>
    </AppBar>
  );
}

export default ResponsiveAppBar;
