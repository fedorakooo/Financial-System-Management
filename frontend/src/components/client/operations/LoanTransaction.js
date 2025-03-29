import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

const LoanTransactions = () => {
  const { loanAccountId } = useParams();
  const numericLoanAccountId = Number(loanAccountId);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newTransactionAmount, setNewTransactionAmount] = useState("");

  useEffect(() => {
    if (isNaN(numericLoanAccountId) || numericLoanAccountId <= 0) {
      setError("❌ Некорректный идентификатор кредита.");
      return;
    }

    const fetchTransactions = async () => {
      try {
        setLoading(true);
        setError(null);
        const token = localStorage.getItem("access_token");

        const response = await fetch(
          `http://localhost:8000/profile/accounts/loan_accounts/${numericLoanAccountId}/transactions`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error("Ошибка загрузки транзакций.");
        }

        const data = await response.json();
        setTransactions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [numericLoanAccountId]);

  const handleCreateTransaction = async () => {
    try {
      if (!newTransactionAmount || isNaN(parseFloat(newTransactionAmount))) {
        alert("⚠️ Введите корректную сумму.");
        return;
      }

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/profile/accounts/loan_accounts/${numericLoanAccountId}/transactions`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: parseFloat(newTransactionAmount),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Ошибка создания транзакции.");
      }

      const data = await response.json();
      setTransactions([...transactions, data]);
      setIsCreating(false);
      setNewTransactionAmount("");
      alert("✅ Транзакция успешно создана!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>⏳ Загрузка...</p>;
  if (error) return <p style={{ color: "red", fontWeight: "bold" }}>{error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">
        📜 Транзакции по кредиту #{numericLoanAccountId}
      </h1>
      <Link
        to={`/loans/${numericLoanAccountId}`}
        className="bg-gray-500 text-white p-2 rounded-lg hover:bg-gray-600 mb-4 block"
      >
        ⬅️ Назад к кредиту
      </Link>

      {/* Форма создания транзакции */}
      {isCreating ? (
        <div className="mb-4">
          <input
            type="number"
            className="border p-2 rounded mr-2"
            placeholder="Введите сумму"
            value={newTransactionAmount}
            onChange={(e) => setNewTransactionAmount(e.target.value)}
          />

          <button
            className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 mr-2"
            onClick={handleCreateTransaction}
          >
            ✅ Создать
          </button>
          <button
            className="bg-gray-400 text-white p-2 rounded hover:bg-gray-500"
            onClick={() => setIsCreating(false)}
          >
            ❌ Отмена
          </button>
        </div>
      ) : (
        <button
          className="bg-green-500 text-white p-2 rounded hover:bg-green-600 mb-4"
          onClick={() => setIsCreating(true)}
        >
          ➕ Создать новую транзакцию
        </button>
      )}

      {/* Список транзакций */}
      {transactions.length === 0 ? (
        <p>📭 Нет транзакций</p>
      ) : (
        <div className="mt-4">
          {transactions.map((t) => (
            <div key={t.id} className="border p-2 rounded mb-2">
              <strong>💰 Сумма:</strong> {t.amount} ₽
              <br />
              <strong>📅 Дата:</strong> {new Date(t.created_at).toLocaleString("ru-RU")}
              <br />
              <strong>🔹 Тип:</strong> {t.type === "CREDIT" ? "💰 Кредит" : "💳 Оплата"}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LoanTransactions;
