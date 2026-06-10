// import { useState } from "react";
// import { signIn } from "../services/auth";

// function Login() {

//     const [email, setEmail] = useState("");
//     const [password, setPassword] = useState("");

//     const handleLogin = async () => {

//         const { error } =
//             await signIn(
//                 email,
//                 password
//             );

//         if(error){
//             alert(error.message);
//         }
//     };

//     return (
//         <div>

//             <input
//                 placeholder="Email"
//                 onChange={(e)=>
//                     setEmail(e.target.value)
//                 }
//             />

//             <input
//                 type="password"
//                 placeholder="Password"
//                 onChange={(e)=>
//                     setPassword(e.target.value)
//                 }
//             />

//             <button onClick={handleLogin}>
//                 Login
//             </button>

//         </div>
//     );
// }

// export default Login;import { useState } from "react";
// import { signIn } from "../services/auth";

// function Login() {

//     const [email, setEmail] = useState("");
//     const [password, setPassword] = useState("");

//     const handleLogin = async () => {

//         const { error } =
//             await signIn(
//                 email,
//                 password
//             );

//         if(error){
//             alert(error.message);
//         }
//     };

//     return (
//         <div>

//             <input
//                 placeholder="Email"
//                 onChange={(e)=>
//                     setEmail(e.target.value)
//                 }
//             />

//             <input
//                 type="password"
//                 placeholder="Password"
//                 onChange={(e)=>
//                     setPassword(e.target.value)
//                 }
//             />

//             <button onClick={handleLogin}>
//                 Login
//             </button>

//         </div>
//     );
// }

// export default Login;

import { useState } from "react";
import { signIn } from "../services/auth";
import { useAuth } from "../context/AuthContext";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { login } = useAuth();

  const handleLogin = async () => {
    const { error } = await signIn(
      email,
      password
    );

    if (error) {
      alert(error.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">

        <h2>InsightURL</h2>

        <input
          className="login-input"
          placeholder="Email"
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <input
          className="login-input"
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          className="login-button"
          onClick={handleLogin}
        >
          Login
        </button>

        <div className="divider">
          OR
        </div>

        <button
          className="google-button"
          onClick={login}
        >
          Continue with Google
        </button>

      </div>
    </div>
  );
}

export default Login;