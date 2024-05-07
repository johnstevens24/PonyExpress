import { createContext, useContext, useState } from "react";

const getToken = () => sessionStorage.getItem("__pony_express_token__");
const storeToken = (token) => sessionStorage.setItem("__pony_express_token__", token);
const clearToken = () => sessionStorage.removeItem("__pony_express_token__");

const AuthContext = createContext();

function AuthProvider({ children }) {
  const [token, setToken] = useState(getToken);

  const login = (tokenData) => {
    setToken(tokenData.access_token);
    storeToken(tokenData.access_token);
  };

  const logout = () => {
    setToken(null);
    clearToken();
  };

  const isLoggedIn = !!token;

  const contextValue = {
    login,
    token,
    isLoggedIn,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

// custom hook
const useAuth = () => useContext(AuthContext);

export { AuthProvider, useAuth };