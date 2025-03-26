import { lazy, Suspense } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Lazy load components
const GeneralBankList = lazy(() => import("./components/general/banks/BankList"));
const GeneralBank = lazy(() => import("./components/general/banks/Bank"));
const Login = lazy(() => import("./components/general/login/Login"));
const Registration = lazy(() => import("./components/general/registration/Registration"));
const Profile = lazy(() => import("./components/profile/Profile"));
const Accounts = lazy(() => import("./components/client/Account"));
const Additions = lazy(() => import("./components/client/general/Addition"));
const Loans = lazy(() => import("./components/client/general/Loan"));
const Transfers = lazy(() => import("./components/client/general/Transfer"));
const CreateLoan = lazy(() => import("./components/client/general/LoanCreate"));

const Home = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold mb-4">Главная страница</h1>
    <p>Добро пожаловать в систему управления банками!</p>
  </div>
);

const NotFound = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold text-red-600">404 - Страница не найдена</h1>
  </div>
);

function App() {
  return (
    <Router>
      <div className="p-4">
        <Suspense fallback={<p>Загрузка компонента...</p>}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/banks" element={<GeneralBankList />} />
            <Route path="/banks/:bankId" element={<GeneralBank />} />
            <Route path="/login" element={<Login />} />
            <Route path="/registration" element={<Registration />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/profile/accounts/additions" element={<Additions />} />
            <Route path="/profile/accounts/loan_accounts/:loanAccountId" element={<Loans />} />
            <Route path="/profile/accounts/loan_accounts/:loanAccountId/transactions" element={<Loans />} />
            <Route path="/profile/accounts/loan_accounts/" element={<CreateLoan />} />
            <Route path="/profile/accounts/transfers/" element={<Transfers />} />
            <Route path="/profile/accounts" element={<Accounts />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  );
}

export default App;