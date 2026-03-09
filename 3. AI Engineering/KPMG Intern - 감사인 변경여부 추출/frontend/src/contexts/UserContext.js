// 사용자 정보(userid)를 저장해주는 context
import { createContext, useContext, useState } from "react";

const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [loggedinuser, setLoggedInUser] = useState("");

    return (
        <UserContext.Provider
            value={{
                loggedinuser: loggedinuser,
                setLoggedInUser: setLoggedInUser,
            }}
        >
            {children}
        </UserContext.Provider>
    );
};

export const useUserID = () => useContext(UserContext);
