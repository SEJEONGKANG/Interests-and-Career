// 기업별 올해 게시된 가장 최신 보고서에 대한 정보들이 담긴 페이지
import { createContext, useContext, useState } from "react";

const RecentContext = createContext();

export const RecentProvider = ({ children }) => {
  const [recentCorps, setRecentCorps] = useState([]);

  return (
    <RecentContext.Provider
      value={{
        recentCorps: recentCorps,
        setRecentCorps: setRecentCorps,
      }}
    >
      {children}
    </RecentContext.Provider>
  );
};

export const useRecent = () => useContext(RecentContext);
