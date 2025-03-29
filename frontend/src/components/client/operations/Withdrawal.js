import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";

const Withdrawals = () => {
  const [searchParams] = useSearchParams();
  const accountId = searchParams.get("account_id");
  const [withdrawals, setWithdrawals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newWithdrawal, setNewWithdrawal] = useState({
    amount: "",
    source: "CASH",
  });

  // Загрузка выводов
  useEffect(() => {
    const fetchWithdrawals = async () => {
      try {
        setLoading(true);
        setError(null);
        
        if (!accountId || isNaN(accountId)) {
          throw new Error("Неверный идентификатор счета");
        }

        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:8000/profile/accounts/withdrawals/?account_id=${accountId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка загрузки выводов");
        }

        const data = await response.json();
        setWithdrawals(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWithdrawals();
  }, [accountId]);

  // Создание вывода
  const handleCreateWithdrawal = async () => {
    try {
      if (!accountId || isNaN(accountId)) {
        throw new Error("Неверный идентификатор счета");
      }

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/profile/accounts/withdrawals/?account_id=${accountId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: parseFloat(newWithdrawal.amount),
            source: newWithdrawal.source,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка создания вывода");
      }

      const data = await response.json();
      setWithdrawals([...withdrawals, data]);
      setIsCreating(false);
      setNewWithdrawal({ amount: "", source: "CASH" });
      alert("Вывод успешно создан!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Выводы со счета #{accountId}</h1>

      {!isCreating && (
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white p-2 rounded-lg mb-4 hover:bg-blue-600"
        >
          Создать новый вывод
        </button>
      )}

      {isCreating && (
        <div className="mb-4 p-4 border border-gray-300 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">Новый вывод</h2>
          
          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Сумма</label>
            <input
              type="number"
              step="0.01"
              value={newWithdrawal.amount}
              onChange={(e) => setNewWithdrawal({ ...newWithdrawal, amount: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите сумму"
            />
          </div>

          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Источник</label>
            <select
              value={newWithdrawal.source}
              onChange={(e) => setNewWithdrawal({ ...newWithdrawal, source: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-lg"
            >
              <option value="CASH">Наличные</option>
              <option value="CARD_PAYMENT">Карта</option>
              <option value="CRYPTO">Криптовалюта</option>
              <option value="OTHER">Другое</option>
            </select>
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleCreateWithdrawal}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Создать
            </button>
            <button
              onClick={() => setIsCreating(false)}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
            >
              Отмена
            </button>
          </div>
        </div>
      )}

      <div className="space-y-4">
        {withdrawals.map((withdrawal) => (
          <div key={withdrawal.id} className="p-4 border border-gray-300 rounded-lg">
            <p><strong>ID:</strong> {withdrawal.id}</p>
            <p><strong>Сумма:</strong> {withdrawal.amount}</p>
            <p><strong>Источник:</strong> {withdrawal.source}</p>
            <p><strong>Дата создания:</strong> {new Date(withdrawal.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>

      {withdrawals.length === 0 && !isCreating && (
        <p className="text-gray-500">Нет выводов для этого счета</p>
      )}
    </div>
  );
};

export default Withdrawals;