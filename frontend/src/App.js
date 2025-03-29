import { lazy, Suspense } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Lazy load components
const GeneralBankList = lazy(() => import("./components/general/banks/BankList"));
const GeneralBank = lazy(() => import("./components/general/banks/Bank"));
const Login = lazy(() => import("./components/general/login/Login"));
const Registration = lazy(() => import("./components/general/registration/Registration"));
const Profile = lazy(() => import("./components/profile/Profile"));
const Accounts = lazy(() => import("./components/client/Account"));
const AccountDetails = lazy(() => import("./components/client/AccountDetail"));
const Additions = lazy(() => import("./components/client/operations/Addition"));
const Loans = lazy(() => import("./components/client/operations/Loan"));
const Transfers = lazy(() => import("./components/client/operations/Transfer"));
const CreateLoan = lazy(() => import("./components/client/operations/LoanCreate"));
const Withdrawals = lazy(() => import("./components/client/operations/Withdrawal"));
const LoanTransactions = lazy(() => import("./components/client/operations/LoanTransaction"));
const GetDepositAccount = lazy(() => import("./components/client/operations/getDepositAccount"));
const CreateDepositAccount = lazy(() => import("./components/client/operations/createDepositAccount"));
const EnterpriseSpecialistProfile = lazy(() => import("./components/client/operations/EnterpriseSpecialistProfile"));
const ApproveLoan = lazy(() => import("./components/client/operations/ApproveLoan"));
const TransferDetails = lazy(() => import("./components/client/operations/TransferDetailStaff"));
const AccountList = lazy(() => import("./components/client/operations/StaffAccountList"));
const GetEnterprise = lazy(() => import("./components/client/operations/GetEnterprisesStaff"));
const CreateEnterprise = lazy(() => import("./components/client/operations/CreateEnterprise"));

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
            <Route path="/profile/accounts/loan_accounts/:loanAccountId/transactions" element={<LoanTransactions />} />
            <Route path="/profile/accounts/loan_accounts/" element={<CreateLoan />} />
            <Route path="/profile/accounts/transfers/" element={<Transfers />} />
            <Route path="/profile/accounts/withdrawals/" element={<Withdrawals />} />
            <Route path="/profile/accounts" element={<Accounts />} />
            <Route path="/profile/accounts/:accountId" element={<AccountDetails />} />
            <Route path="/profile/accounts/deposit_accounts/:depositAccountId" element={<GetDepositAccount />} />
            <Route path="/profile/accounts/deposit_accounts/" element={<CreateDepositAccount />} />
            <Route path="/enterprises/specialists/profile/" element={<EnterpriseSpecialistProfile />} />
            <Route path="/staff/accounts/loans/:loanAccountID/" element={<ApproveLoan />} />
            <Route path="/staff/accounts/transfers/:transferID" element={<TransferDetails />} />
            <Route path="/staff/accounts/" element={<AccountList />} />
            <Route path="/staff/enterprises/:enterpriseID" element={<GetEnterprise />} />
            <Route path="/staff/enterprises/" element={<CreateEnterprise />} />


            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  );
}

export default App;