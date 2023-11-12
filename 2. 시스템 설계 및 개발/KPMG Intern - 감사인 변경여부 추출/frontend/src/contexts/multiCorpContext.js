// 검색창에서 두개 이상의 기업을 선택했을 경우 handlemultisumbmit 시 해당 기업들로 변경 
import { createContext, useContext, useState } from "react";

const MultiCorpContext = createContext();

export const MultiCorpProvider = ({ children }) => {
    const [multiCorp, setMultiCorp] = useState([]);

    return (
        <MultiCorpContext.Provider
            value={{
                multiCorp: multiCorp,
                setMultiCorp: setMultiCorp,
            }}
        >
            {children}
        </MultiCorpContext.Provider>
    );
};
/**
 * 
 * CorpForm.js에서 기업을 여러개 선택한 경우 선택된 기업들의 Context
 * const [multiCorp, setMultiCorp] = useState([]) => multiCorp를 변경해주며 MultiResultPage에서 fastapi server로 전송
 */
export const useMultiCorp = () => useContext(MultiCorpContext);
