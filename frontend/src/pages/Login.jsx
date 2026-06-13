{/* <div className="login-form">
  <div className="logo-circle">
    🔍
  </div>

  <h2>InsightURL</h2>

  <p className="login-subtitle">
    Turn websites into searchable AI knowledge bases
  </p>

  <button
    className="google-button"
    onClick={login}
  >
    Continue with Google
  </button>

  <p className="footer-text">
    Powered by RAG • Supabase • Groq
  </p>
</div>

export default Login; */}
import { useAuth } from "../context/AuthContext";
import "./Login.css";

function Login() {
  const { login } = useAuth();

  return (
    <div className="login-container">
      <div className="login-form">
        <div className="logo-circle">
          🔍
        </div>

        <h2>InsightURL</h2>

        <p className="login-subtitle">
          Turn websites into searchable AI knowledge bases
        </p>

        <button
          className="google-button"
          onClick={login}
        >
          Continue with Google
        </button>

        <p className="footer-text">
          Powered by RAG • Supabase • Groq
        </p>
      </div>
    </div>
  );
}

export default Login;