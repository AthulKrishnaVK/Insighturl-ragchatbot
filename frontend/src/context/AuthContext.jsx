import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";

import { supabase }
from "../lib/supabase";

const AuthContext =
  createContext();

export function AuthProvider(
  { children }
) {

  const [user, setUser] =
    useState(null);

  useEffect(() => {

    supabase.auth
      .getUser()
      .then(({ data }) => {

        setUser(data.user);
      });

    const {
      data: listener
    } = supabase.auth
      .onAuthStateChange(
        (_, session) => {

          setUser(
            session?.user || null
          );
        }
      );

    return () =>
      listener.subscription.unsubscribe();

  }, []);

  const login = async () => {

    await supabase.auth
      .signInWithOAuth({
        provider: "google",
        options: {
        redirectTo: "https://insighturl-ragchatbot.vercel.app/"
      }});
  };

  const logout = async () => {

    await supabase.auth.signOut();
  };

  return (

    <AuthContext.Provider
      value={{
        user,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () =>
  useContext(AuthContext);