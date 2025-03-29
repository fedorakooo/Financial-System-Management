import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";

const Transfers = () => {
  const [searchParams] = useSearchParams();
  const accountId = searchParams.get("account_id");
  const [transfers, setTransfers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [newTransfer, setNewTransfer] = useState({
    amount: "",
    to_account_id: ""
  });

  // Загрузка переводов
  useEffect(() => {
    const fetchTransfers = async () => {
      try {
        setLoading(true);
        setError(null);
        
        if (!accountId || isNaN(accountId)) {
          throw new Error("Неверный идентификатор счета");
        }

        const token = localStorage.getItem("access_token");
        const response = await fetch(
          `http://localhost:8000/profile/accounts/transfers/?account_id=${accountId}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Ошибка загрузки переводов");
        }

        const data = await response.json();
        setTransfers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTransfers();
  }, [accountId]);

  // Создание перевода
  const handleCreateTransfer = async () => {
    try {
      if (!accountId || isNaN(accountId)) {
        throw new Error("Неверный идентификатор счета");
      }

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `http://localhost:8000/profile/accounts/transfers/?account_id=${accountId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: parseFloat(newTransfer.amount),
            to_account_id: parseInt(newTransfer.to_account_id)
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка создания перевода");
      }

      const data = await response.json();
      setTransfers([...transfers, data]);
      setIsCreating(false);
      setNewTransfer({ amount: "", to_account_id: "" });
      alert("Перевод успешно создан!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: "red" }}>Ошибка: {error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Переводы счета #{accountId}</h1>

      {/* Кнопка создания */}
      {!isCreating && (
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-500 text-white p-2 rounded-lg mb-4 hover:bg-blue-600"
        >
          Создать новый перевод
        </button>
      )}

      {/* Форма создания */}
      {isCreating && (
        <div className="mb-4 p-4 border border-gray-300 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">Новый перевод</h2>
          
          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Сумма перевода</label>
            <input
              type="number"
              step="0.01"
              value={newTransfer.amount}
              onChange={(e) => setNewTransfer({...newTransfer, amount: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите сумму"
            />
          </div>

          <div className="mb-3">
            <label className="block text-gray-700 mb-1">Целевой счет</label>
            <input
              type="number"
              value={newTransfer.to_account_id}
              onChange={(e) => setNewTransfer({...newTransfer, to_account_id: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg"
              placeholder="Введите ID целевого счета"
            />
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleCreateTransfer}
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

      {/* Список переводов */}
      <div className="space-y-4">
        {transfers.map((transfer) => (
          <div key={transfer.id} className="p-4 border border-gray-300 rounded-lg">
            <p><strong>ID перевода:</strong> {transfer.id}</p>
            <p><strong>Со счета:</strong> {transfer.from_account_id}</p>
            <p><strong>На счет:</strong> {transfer.to_account_id}</p>
            <p><strong>Сумма:</strong> {transfer.amount}</p>
            <p><strong>Статус:</strong> {transfer.status}</p>
            <p><strong>Дата создания:</strong> {new Date(transfer.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>

      {/* Сообщение при пустом списке */}
      {transfers.length === 0 && !isCreating && (
        <p className="text-gray-500">Нет переводов для этого счета</p>
      )}
    </div>
  );
};

export default Transfers;