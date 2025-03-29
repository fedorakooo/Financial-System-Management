import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const LoanDetails = () => {
  const { loanAccountId } = useParams();
  const [loanAccount, setLoanAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLoanData = async () => {
      try {
        setLoading(true);
        setError(null);
        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:8000/profile/accounts/loan_accounts/${loanAccountId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Ошибка загрузки данных о кредите");
        }

        const data = await response.json();
        setLoanAccount(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLoanData();
  }, [loanAccountId]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Кредитный счёт #{loanAccountId}</h1>
      {loanAccount && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Информация о кредите</h2>
          <p><strong>Сумма кредита:</strong> {loanAccount.loan.amount}</p>
          <p><strong>Срок:</strong> {loanAccount.loan.term_months} месяцев</p>
          <p><strong>Процентная ставка:</strong> {loanAccount.loan.interest_rate}%</p>
          <p><strong>Статус:</strong> {loanAccount.status}</p>
        </div>
      )}
      <Link to={`./transactions`} className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600">
        Перейти к транзакциям
      </Link>
    </div>
  );
};

export default LoanDetails;