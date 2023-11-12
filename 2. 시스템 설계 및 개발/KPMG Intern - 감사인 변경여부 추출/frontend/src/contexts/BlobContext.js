// 다운 받을 기업별 올해 게시된 보고서의 정보 엑셀파일의 context => login시 excel파일에 대해 요청을 보냄
import { createContext, useContext, useState } from "react";

const BlobContext = createContext();

export const BlobProvider = ({ children }) => {
  const [blob, setBlob] = useState(null);

  return (
    <BlobContext.Provider
      value={{
        blob: blob,
        setBlob: setBlob,
      }}
    >
      {children}
    </BlobContext.Provider>
  );
};

export const useBlob = () => useContext(BlobContext);
