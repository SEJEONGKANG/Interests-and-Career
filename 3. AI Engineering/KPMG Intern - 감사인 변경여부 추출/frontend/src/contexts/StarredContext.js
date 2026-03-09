// 즐겨찾기 목록 추가 및 해제, 즐겨찾기 목록을 저장해주는 context
import { createContext, useContext, useState } from "react";

const StarredContext = createContext();

export const StarredProvider = ({ children }) => {
  const [starred, setStarred] = useState([]);

  const addStarred = (corp) => {
    setStarred([...starred, corp]);
  };

  const removeStarred = (Item) => {
    setStarred(
      starred.filter((ItemInArray) => Item.corp_code !== ItemInArray.corp_code)
    );
  };

  return (
    <StarredContext.Provider
      value={{
        starred: starred,
        setStarred: setStarred,
        addStarred: addStarred,
        removeStarred: removeStarred,
      }}
    >
      {children}
    </StarredContext.Provider>
  );
};

export const useStarredList = () => useContext(StarredContext);
