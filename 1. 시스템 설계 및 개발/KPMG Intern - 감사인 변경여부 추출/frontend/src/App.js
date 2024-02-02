import React from "react";
import { Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SearchPage from "./pages/SearchPage";
import ResultPage from "./pages/ResultPage";
import MultiResultPage from "./pages/MultiResultPage";
import TargetPage from "./pages/TargetPage";
import StarredPage from "./pages/StarredPage";
import MainPage from "./pages/MainPage";
import ViewRecentPage from "./pages/ViewRecentPage";
import { StarredProvider } from "./contexts/StarredContext";
import { UserProvider } from "./contexts/UserContext";
import { CurCorpProvider } from "./contexts/curCorpContext";
import { MultiCorpProvider } from "./contexts/multiCorpContext";
import { RecentProvider } from "./contexts/RecentContext";
import { BlobProvider } from "./contexts/BlobContext";
const App = () => {
  return (
    <BlobProvider>
      <RecentProvider>
        <MultiCorpProvider>
          <CurCorpProvider>
            <UserProvider>
              <StarredProvider>
                <Routes>
                  <Route path="/" element={<LoginPage />} />
                  <Route path="/main" element={<MainPage />} />
                  <Route path="/search" element={<SearchPage />} />
                  <Route path="/result" element={<ResultPage />} />
                  <Route path="/multiresult" element={<MultiResultPage />} />
                  <Route path="/contact" element={<TargetPage />} />
                  <Route path="/starred" element={<StarredPage />} />
                  <Route path="/recent" element={<ViewRecentPage />} />
                </Routes>
              </StarredProvider>
            </UserProvider>
          </CurCorpProvider>
        </MultiCorpProvider>
      </RecentProvider>
    </BlobProvider>
  );
};

export default App;
