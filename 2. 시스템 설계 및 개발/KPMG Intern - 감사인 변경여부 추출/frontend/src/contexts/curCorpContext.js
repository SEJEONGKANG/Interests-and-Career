// 각 페이지들에서 기업명을 클릭시 해당 기업으로 curcorpcode가 설정되고 해당 corpcode에 해당하는 단일검색결과를 backend에 요청하는 useEffect hooks를 trigger
import { createContext, useContext, useState } from "react";

const CurCorpContext = createContext();

export const CurCorpProvider = ({ children }) => {
    const [curcorpname, setCurcorpname] = useState("");
    const [curcorpcode, setCurcorpcode] = useState("");

    return (
        <CurCorpContext.Provider
            value={{
                curcorpname: curcorpname,
                setCurcorpname: setCurcorpname,
                curcorpcode: curcorpcode,
                setCurcorpcode: setCurcorpcode,
            }}
        >
            {children}
        </CurCorpContext.Provider>
    );
};

export const useCurCorp = () => useContext(CurCorpContext);
