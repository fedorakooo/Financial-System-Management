import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const GetDepositAccount = () => {
  const { depositAccountId } = useParams();
  const [depositAccount, setDepositAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDepositAccount = async () => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("access_token");
        const response = await fetch(`http://localhost:8000/profile/accounts/deposit_accounts/${depositAccountId}`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка загрузки данных");
        }

        const data = await response.json();
        setDepositAccount(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDepositAccount();
  }, [depositAccountId]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold">Депозитный счет #{depositAccount.id}</h1>
      <p><strong>Процентная ставка:</strong> {depositAccount.interest_rate}%</p>
      <p><strong>Исходный счет ID:</strong> {depositAccount.from_account_id}</p>
    </div>
  );
};

export default GetDepositAccount;
